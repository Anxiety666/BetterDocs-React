#!/usr/bin/env python3
"""Génère les données du site Elderwood à partir de content/*.md et pages.json.

Usage :
    python3 build.py                      # build complet (toutes les pages) dans data/
    python3 build.py --audience joueurs   # build sans les pages « staff » (dans dist/joueurs/)
    python3 build.py --audience public    # build ne contenant que les pages « public » (dans dist/public/)
    python3 build.py --check              # génère + vérifie, code de sortie ≠ 0 en cas d'écart

Ne dépend que de la bibliothèque standard Python 3.8+.
"""
import argparse, csv, html, io, json, re, shutil, sys, unicodedata
import wikimd
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
LEVELS = ["public", "joueurs", "staff"]          # du plus ouvert au plus restreint

# --------------------------------------------------------------------------- utilitaires
def fold(s):
    s = unicodedata.normalize("NFD", s.casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("œ", "oe").replace("æ", "ae")

def slugify(s, fallback="section"):
    s = re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")
    return s[:60] or fallback

def tokens(s):
    return re.findall(r"[^\W_]+", s.casefold())

def esc(s):
    return html.escape(s, quote=False)

URL_RE = re.compile(r"(https?://[^\s<>\"]+[^\s<>\".,;:!?)\]»”])")

def inline(s):
    """Texte brut -> HTML inline (échappement, **gras**, __souligné__, liens)."""
    s = re.sub(r"\\([\[\]*_#>~`|])", r"\1", s)
    out, pos = [], 0
    for m in URL_RE.finditer(s):
        out.append(fmt_inline(s[pos:m.start()]))
        u = m.group(1)
        out.append('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (html.escape(u, quote=True), esc(u)))
        pos = m.end()
    out.append(fmt_inline(s[pos:]))
    return "".join(out)

def fmt_inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)
    return s

# --------------------------------------------------------------------------- confidentialité
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
GDOC_RE = re.compile(r"https?://(?:docs|drive)\.google\.com/[^\s<>\"|]+")

def redact_text(text, cfg, log):
    def mail(m):
        # Les adresses de groupe (ex. « @rrp-srp@googlegroups.com ») restent des données internes : on les masque aussi.
        log.append(("e-mail", m.group(0)))
        return cfg["redactions"]["email"]
    text = EMAIL_RE.sub(mail, text)
    params = set(cfg["redactions"]["url_params"])

    def clean_url(m):
        u = m.group(0)
        if "?" not in u:
            return u
        base, q = u.split("?", 1)
        keep = [p for p in q.split("&") if p.split("=")[0] not in params]
        if len(keep) != len(q.split("&")):
            log.append(("paramètres d'URL", q))
        return base + ("?" + "&".join(keep) if keep else "")
    return GDOC_RE.sub(clean_url, text)

HANDLES = set()

def compact(v):
    return re.sub(r"[^a-z0-9]", "", fold(v))

def collect_handles(cfg, pages_src):
    """Pseudos Discord connus : cellules de colonnes « Discord » dans les tableaux bien alignés."""
    cols = set(cfg["redactions"]["table_columns"])
    for p in pages_src:
        if not p["k"].startswith("sheet-"):
            continue
        _m, body = load_page(p["k"])
        for typ, val in split_sheet_sections(body, cfg, []):
            if typ != "t":
                continue
            hdr = val[0]
            idx = [i for i, h in enumerate(hdr) if fold(h).strip(" :") == "discord"]
            for r in val[1:]:
                for i in idx:
                    if len([c for c in r if c.strip()]) >= len(hdr) - 2 and i < len(r) and r[i].strip():
                        HANDLES.add(compact(r[i]))

def looks_like_handle(v, cfg):
    t = v.strip()
    if not t or t.startswith("["):
        return False
    f = fold(t).strip(". ")
    if f in set(cfg["redactions"]["keep_values"]):
        return False
    if compact(t) in HANDLES:
        return True
    parts = [compact(x) for x in re.split(r"[/,;]", t) if x.strip()]
    if len(t.split()) <= 4 and parts and any(p in HANDLES for p in parts):
        return True
    if "/" in t and all(re.match(r"^[\w.\-]+$", x.strip()) for x in t.split("/") if x.strip()):
        return True                      # « Blade / ayuutsu »
    return bool(re.match(r"^[\w.\-]+$", t))

def redact_rows(rows, cfg, log):
    """Masque les pseudos/contacts des colonnes « Discord » et « Contact » (rows[0] = en-tête)."""
    if not rows:
        return rows
    wanted = set(cfg["redactions"]["table_columns"])
    cols = {i: fold(h).strip(" :") for i, h in enumerate(rows[0]) if fold(h).strip(" :") in wanted}
    if not cols:
        return rows
    out = [rows[0]]
    for r in rows[1:]:
        r = list(r)
        for i, name in cols.items():
            if i < len(r) and r[i].strip() and looks_like_handle(r[i], cfg):
                log.append(("colonne « %s »" % rows[0][i].strip(), r[i]))
                r[i] = cfg["redactions"]["column"]
        out.append(r)
    return out

# --------------------------------------------------------------------------- tableaux
def _sig(c):
    c = c.strip()
    if not c:
        return "E"
    if re.match(r"^\d+$", c):
        return "I"
    if re.match(r"^[IVXLC]{1,7}$", c):
        return "R"
    if re.match(r"^[A-Z]{1,3}\d+$", c):
        return "C"
    if re.search(r"\d", c) and len(c) <= 14:
        return "D"
    w = len(c.split())
    return "S" if w <= 2 else "M" if w <= 6 else "L" if w <= 18 else "X"

def _entropy(vals):
    import math
    n = len(vals)
    h = 0.0
    for v in set(vals):
        p = vals.count(v) / n
        h -= p * math.log2(p)
    return h

def _score(cells, N, drop=0):
    m = len(cells) - drop
    if N < 1 or m % N or m // N < 2:
        return None
    rows = m // N
    body = [_sig(c) for c in cells[N:m]]
    hs = [_entropy([body[r * N + j] for r in range(rows - 1)]) for j in range(N)]
    sc = sum(hs) / N
    hdr = cells[:N]
    if sum(len(c.split()) for c in hdr) / N > 5:
        sc += 0.6
    if any(c.rstrip().endswith(".") for c in hdr):
        sc += 0.6
    if any(not c.strip() for c in hdr):
        sc += 0.8
    # un en-tête est fait de libellés courts (pas de nombres, pas de longs textes)
    sc += 0.8 * sum(1 for c in hdr if _sig(c) not in ("S", "M"))
    if m > 8 and rows - 1 < 3:
        sc += 0.35 * (3 - (rows - 1))
    return sc + 0.45 * drop + 0.06 * N

def _best_single(cells):
    best = None
    for drop in range(0, 3):
        for N in range(2, min(9, (len(cells) - drop) // 2) + 1):
            sc = _score(cells, N, drop)
            if sc is not None and (best is None or sc < best[0] - 1e-9):
                best = (sc, N, drop)
    return best

def _header_like(cs):
    return all(c and _sig(c) in ("S", "M") and re.match(r"^[^\W\d_]", c) and not re.search(r"\d", c) and len(c) <= 40 for c in cs)

def infer_segments(cells):
    """Découpe une suite de cellules en un ou plusieurs tableaux : [(debut, fin, ncols)]."""
    n = len(cells)
    if n < 4:
        return [(0, n, max(1, n), 0)]
    whole = _best_single(cells)
    cand = None
    if whole is None or whole[0] > 1.0:
        for p in range(4, n - 3):
            if not _header_like(cells[p:p + 3]):
                continue
            for N1 in range(2, 9):
                if p % N1:
                    continue
                s1 = _score(cells[:p], N1)
                if s1 is None:
                    continue
                b2 = _best_single(cells[p:])
                if b2 is None:
                    continue
                tot = (s1 * p + b2[0] * (n - p)) / n
                if cand is None or tot < cand[0]:
                    cand = (tot, p, N1, b2)
        if cand and (whole is None or cand[0] < whole[0] - 0.4):
            _t, p, N1, b2 = cand
            return [(0, p, N1, 0), (p, n - b2[2], b2[1], 0 if not b2[2] else 0)] if not b2[2] else [(0, p, N1, 0), (p, n - b2[2], b2[1], b2[2])]
    if whole is None:
        return [(0, n, 1, 0)]
    return [(0, n - whole[2], whole[1], whole[2])]

def infer_ncols(cells):
    seg = infer_segments(cells)
    return (seg[0][2], seg[0][3]) if len(seg) == 1 else None

def table_html(rows, cls="", header=True):
    if not rows:
        return ""
    w = max(len(r) for r in rows)
    rows = [list(r) + [""] * (w - len(r)) for r in rows]
    h = ['<div class="tbl-wrap"><table class="%s">' % cls]
    body = rows
    if header:
        h.append("<thead><tr>" + "".join("<th scope=\"col\">%s</th>" % cell_html(c) for c in rows[0]) + "</tr></thead>")
        body = rows[1:]
    h.append("<tbody>")
    for r in body:
        h.append("<tr>" + "".join("<td>%s</td>" % cell_html(c) for c in r) + "</tr>")
    h.append("</tbody></table></div>")
    return "".join(h)

def cell_html(c):
    return "<br>".join(inline(p) for p in c.split("\n")) if c.strip() else ""

def rows_text(rows):
    return "\n".join(" | ".join(c.replace("\n", " ") for c in r if c.strip()) for r in rows)

# --------------------------------------------------------------------------- analyse des documents « texte »
BULLET_RE = re.compile(r"^(\s*)([*\-•·▪◦●○‣⁃])\s+(\S.*)$")
NUM_RE = re.compile(r"^(\s*)(\d{1,3})([.)])\s+(\S.*)$")
RULE_RE = re.compile(r"^\s*(?:[_=\-─━–—]{3,}|[-+ ]{6,}|\*{3,}|[~·•\s]{6,})\s*$")
EMOJI_RE = re.compile(r"^[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2190-\u21FF✦✧☰]")
ROMAN_RE = re.compile(r"^(?:[IVXLC]+)\.\s+\S")
STRONG_KEYWORD = re.compile(r"^(?:Chapitre|Partie|Section|Titre|Annexe|Livre|Acte|Phase|Étape|Etape|Article|Loi|Classe|Palier|Niveau|Tier|Trame|Bloc|Principe|Premier principe|Second principe|Troisième principe|Quatrième principe|Cinquième principe)\s+[\dIVXLCivxlc]+\b.{0,100}$")
LEADER_RE = re.compile(r"^(.+?\S)\s{3,}(\d{1,4})$")

KICKERS = {"TRANSVERSAL", "LORE ANTIQUE", "LORE MODERNE", "ELDERWOOD"}

def indent_of(line):
    w = 0
    for ch in line:
        if ch == "\t":
            w += 4
        elif ch == " ":
            w += 1
        else:
            break
    return w

def strong_level(s):
    """Retourne un niveau de titre (2-4) si la ligne est très clairement un titre, sinon 0."""
    if len(s) > 110 or LEADER_RE.match(s) or s.endswith("·") or s in KICKERS:
        return 0
    if re.match(r"^#{1,6}\s", s):
        return 0  # géré à part
    letters = [c for c in s if c.isalpha()]
    if re.match(r"^[-–]\s+\S.*\S\s+[-–](?:\s*\(.*\))*\s*(?:\(.*\))?$", s) and len(s) < 90:
        return 3
    if s.endswith((".", ";", ",")) and not re.match(r"^(Article\s+\d+|\d+(\.\d+)*)\.?$", s.rstrip()) and not re.match(r"^(?:Article|Loi|Classe)\s+[\dIVXLC]+\.$", s):
        # « Article 1. » est un titre malgré le point final ; « 1.1. L'Écho » aussi
        if not re.match(r"^\d+(\.\d+)+\.\s+\S", s) and not re.match(r"^(?:Article|Loi|Classe)\s+[\dIVXLC]+\.\s*$", s):
            return 0
    if re.match(r"^§\s*\d+\s*[—–-]\s+\S", s) and not s.endswith("."):
        return 2
    if len(letters) >= 4 and sum(c.isupper() for c in letters) / len(letters) >= 0.85 and len(s) <= 90 and not s.endswith(":"):
        return 2
    if re.match(r"^Article\s+\d+\.?\s*$", s):
        return 3
    if STRONG_KEYWORD.match(s) and not s.endswith(":") and len(s) <= 100:
        return 3 if re.match(r"^(?:Article|Loi|Classe|Niveau|Palier|Tier|Étape|Etape|Bloc)\b", s) else 2
    if ROMAN_RE.match(s) and len(s) <= 100:
        return 2
    m = re.match(r"^§?\s*(\d+(?:\.\d+)*)[.)]?\s+[A-ZÀ-ÖØ-Þ0-9«“\"'(\[\U0001F300-\U0001FAFF]", s)
    if m and len(s) <= 100 and not s.endswith("?") or (m and s.endswith("?") and len(s) <= 100):
        depth = m.group(1).count(".") + 1
        if re.match(r"^§", s):
            return 0
        return 2 if depth == 1 else 3
    if EMOJI_RE.match(s) and len(s) <= 90 and len(s.split()) >= 2:
        return 3
    return 0

def weak_ok(s):
    """Ligne courte, sans ponctuation finale : titre probable (à confirmer par le contexte)."""
    if s.endswith("·") or s in KICKERS:
        return False
    if len(s) > 80 or len(s) < 3:
        return False
    if len(s.split()) > 12:
        return False
    if s[-1] in ".;,!»”\"…)" and not s.endswith("...)"):
        if s[-1] != ")":
            return False
    if not (s[0].isupper() or s[0].isdigit() or EMOJI_RE.match(s) or s[0] in "«“\"'‘’(["):
        return False
    if re.search(r"\s:\s+\S", s) or re.search(r"\S:\s+\S", s):
        return False   # « Label : valeur »
    if re.match(r"^[\d\s/.,:\-–—+±%xX×]+$", s):
        return False
    if LEADER_RE.match(s):
        return False
    return True

class Doc:
    """Convertit un texte brut (export Google Docs / pandoc) en blocs HTML + texte brut."""

    def __init__(self, title):
        self.title = title
        self.html = []
        self.text = []
        self.toc = []
        self.ids = Counter()
        self.table_notes = []

    # -- ancres
    def anchor(self, text):
        base = slugify(text)
        self.ids[base] += 1
        return base if self.ids[base] == 1 else "%s-%d" % (base, self.ids[base])

    def heading(self, level, text, cls=""):
        text = text.strip()
        hid = self.anchor(text)
        level = max(2, min(5, level))
        self.html.append('<h%d id="%s"%s>%s</h%d>' % (level, hid, (' class="%s"' % cls) if cls else "", inline(text), level))
        self.text.append("\n" + text)
        if level <= 3 and not cls:
            self.toc.append({"id": hid, "t": re.sub(r"\*\*|__", "", text), "l": level})

    def para(self, text, cls=""):
        self.html.append("<p%s>%s</p>" % ((' class="%s"' % cls) if cls else "", inline(text.strip())))
        self.text.append(text.strip())

def extract_tab_table(lines, i):
    """Table aplatie par l'export Google Docs : 1re cellule sans tabulation, suivantes préfixées par \\t.
    Retourne (cells, next_index) ou None."""
    if i + 1 >= len(lines):
        return None
    first = lines[i]
    if not first.strip() or first.startswith("\t") or not lines[i + 1].startswith("\t"):
        return None
    # une liste imbriquée (puces avec tabulation) n'est pas un tableau
    probe = lines[i + 1].lstrip("\t").strip()
    if BULLET_RE.match(lines[i + 1].lstrip("\t")) or NUM_RE.match(lines[i + 1].lstrip("\t")) or re.match(r"^[*\-•·]\s*$", probe):
        return None
    if RULE_RE.match(first) or first.lstrip().startswith("|"):
        return None
    cells = [[first.strip()]]
    j = i + 1
    ended = False
    while j < len(lines):
        ln = lines[j]
        if ln.startswith("\t"):
            if ln == "\t" and (j + 1 >= len(lines) or not lines[j + 1].startswith("\t")):
                ended = True
                j += 1
                break
            cells.append([ln[1:].strip()])
            j += 1
            continue
        if not ln.strip():
            # ligne vide : continue seulement si une cellule suit
            k = j + 1
            while k < len(lines) and not lines[k].strip():
                k += 1
            if k < len(lines) and lines[k].startswith("\t") and k - j <= 2:
                j = k
                continue
            break
        if RULE_RE.match(ln):
            break
        # ligne sans tabulation : suite de la cellule précédente si une cellule suit juste après
        k = j + 1
        while k < len(lines) and lines[k].strip() and not lines[k].startswith("\t"):
            k += 1
        if k < len(lines) and lines[k].startswith("\t") and k - j <= 4:
            for t in range(j, k):
                cells[-1].append(lines[t].strip())
            j = k
            continue
        break
    flat = ["\n".join(p for p in c if p) for c in cells]
    return flat, j

def md_table_block(lines, i):
    """Lignes commençant par « | » (pandoc). Retourne (rows|None, callout_lines, next_index)."""
    j = i
    raw = []
    while j < len(lines) and lines[j].lstrip().startswith("|"):
        raw.append(lines[j].strip())
        j += 1
    rows, sep = [], False
    multi = False
    for r in raw:
        if re.match(r"^\|[\s:\-|+]+\|?$", r) and "-" in r:
            sep = True
            continue
        if r.endswith("|") and len(r) > 1:
            cells = [c.strip() for c in r.strip("|").split("|")]
            rows.append(cells)
            if len(cells) > 1:
                multi = True
        else:
            rows.append([r.lstrip("|").strip()])
    if multi and (sep or len(rows) >= 2):
        w = max(len(r) for r in rows)
        return [r + [""] * (w - len(r)) for r in rows], None, j
    return None, [r[0] if len(r) == 1 else " | ".join(c for c in r if c) for r in rows if any(c.strip() for c in r)], j

TERMINAL = ".!?:;»”…)\"'"

def reflow(lines, aggressive=False):
    """Recolle les lignes coupées par l'export (retours à la ligne PDF, mots en gras/lien isolés)."""
    out = []
    n = len(lines)
    for idx, ln in enumerate(lines):
        s = ln.strip()
        if out and s and not ln.startswith("\t") and not s.startswith("|"):
            prev = out[-1]
            ps = prev.strip()
            if ps and not prev.startswith("\t") and not RULE_RE.match(prev) and not ps.startswith("|") and not re.match(r"^#{1,6}\s", ps):
                cont = bool(re.match(r"^[,.;:)»\]]", s))
                low = bool(re.match(r"^[a-zàâäçéèêëîïôöùûüœæ]", s)) and not BULLET_RE.match(ln) and not NUM_RE.match(ln)
                if cont:
                    out[-1] = prev.rstrip() + s
                    continue
                if low and ps[-1] not in TERMINAL and len(ps) >= 3:
                    out[-1] = prev.rstrip() + " " + s
                    continue
                if aggressive:
                    nxt = lines[idx + 1].strip() if idx + 1 < n else ""
                    protected = bool(strong_level(ps) or strong_level(s) or re.match(r"^(?:Section|Annexe|Chapitre)\b", ps))
                    # « Fondateur : » + « Eldric Falcon. »
                    if not protected and ps.endswith(":") and len(ps) <= 40 and len(s) <= 160 and not s.endswith(":") and not BULLET_RE.match(ln):
                        out[-1] = prev.rstrip() + " " + s
                        continue
                    # mot en gras / lien isolé au milieu d'une phrase : « …nommé le » + « Premier Murmure » + «, moment… »
                    if (not protected and len(ps) >= 25 and ps[-1] not in TERMINAL and not BULLET_RE.match(prev) and not NUM_RE.match(prev)
                            and len(s) <= 45 and s[-1] not in TERMINAL and re.match(r"^([,.;:)»]|[a-zàâäçéèêëîïôöùûüœæ])", nxt)):
                        out[-1] = prev.rstrip() + " " + s
                        continue
        out.append(ln)
    return out

AGGRESSIVE_REFLOW = {"bible-du-lore"}

def parse_doc(body, title, key=""):
    d = Doc(title)
    lines = reflow(body.replace("\r", "").split("\n"), aggressive=key in AGGRESSIVE_REFLOW)
    items = []   # (kind, payload...)
    i = 0
    # --- passe préalable : cohérence entre tableaux d'un même document ayant le même en-tête
    scan, k0 = {}, 0
    while k0 < len(lines):
        tt0 = extract_tab_table(lines, k0)
        if tt0:
            c0 = list(tt0[0])
            while c0 and not c0[-1].strip() and len(c0) > 1:
                c0.pop()
            scan[k0] = (c0, tt0[1])
            k0 = tt0[1]
        else:
            k0 += 1
    groups = {}
    for k0, (c0, _j) in scan.items():
        if len(c0) >= 4:
            sg = infer_segments(c0)
            if len(sg) == 1:
                groups.setdefault((c0[0], c0[1]), []).append((k0, sg[0][2]))
    forced = {}
    for gk, mem in groups.items():
        if len(mem) >= 3:
            mode = Counter(n_ for _k, n_ in mem).most_common(1)[0]
            if mode[1] >= 2:
                for k0, _n in mem:
                    forced[k0] = mode[0]
    while i < len(lines):
        ln = lines[i].rstrip()
        # tableau aplati
        t = extract_tab_table(lines, i)
        if t:
            cells, j = t
            while cells and not cells[-1].strip() and len(cells) > 1:
                cells.pop()
            if len(cells) <= 3:
                # trop court pour être un tableau : encadré (1 cellule) ou simples paragraphes
                if len(cells) == 1 or not any(c.strip() for c in cells[1:]):
                    for sub in cells[0].split("\n"):
                        items.append(("callout", sub))
                else:
                    for c in cells:
                        for sub in c.split("\n"):
                            if sub.strip():
                                items.append(("text", sub.strip(), 0))
                i = j
                continue
            segs = infer_segments(cells)
            if i in forced and len(cells) >= 4 and len(segs) == 1 and forced[i] != segs[0][2] and len(cells) // forced[i] >= 2:
                fn = forced[i]
                segs = [(0, len(cells) - len(cells) % fn, fn, len(cells) % fn)]
            for (a0, a1, ncols, drop) in segs:
                part = cells[a0:a1]
                while len(part) % ncols:
                    part.append("")
                rows = [part[r:r + ncols] for r in range(0, len(part), ncols)]
                items.append(("table", rows, ncols))
                if drop:
                    for tr in cells[a1:a1 + drop]:
                        for sub in tr.split("\n"):
                            items.append(("text", sub, 0))
            i = j
            continue
        if ln.lstrip().startswith("|"):
            rows, callout, j = md_table_block(lines, i)
            if rows:
                items.append(("table", rows, len(rows[0])))
            else:
                for c in callout:
                    items.append(("callout", c))
            i = j
            continue
        if not ln.strip():
            items.append(("blank",))
        elif RULE_RE.match(ln):
            items.append(("rule", ln))
        else:
            m = re.match(r"^(#{1,6})\s+(.*)$", ln)
            if m:
                items.append(("mdh", len(m.group(1)), m.group(2)))
            else:
                mb = BULLET_RE.match(ln.replace("\t", "    "))
                mn = NUM_RE.match(ln.replace("\t", "    "))
                if mb and not re.match(r"^\s*[-–]\s+\S.*\S\s+[-–]\s*$", ln) :
                    items.append(("bullet", indent_of(ln), mb.group(3)))
                elif mn and (mn.group(4).rstrip().endswith((".", ";", ",", ":")) or len(mn.group(4)) > 70):
                    items.append(("num", indent_of(ln), mn.group(2) + mn.group(3), mn.group(4)))
                else:
                    items.append(("text", ln.strip(), indent_of(ln)))
        i += 1

    # ---- classification des titres
    n = len(items)
    cand = [0] * n          # 0 : non ; 2..4 : niveau
    kind = [None] * n       # 'strong' | 'weak' | 'label'
    def next_nonblank(k):
        k += 1
        while k < n and items[k][0] == "blank":
            k += 1
        return k
    def prev_nonblank(k):
        k -= 1
        while k >= 0 and items[k][0] == "blank":
            k -= 1
        return k
    for k, it in enumerate(items):
        if it[0] == "mdh":
            cand[k], kind[k] = min(4, it[1] + 1), "md"
        elif it[0] == "text":
            s = it[1]
            lv = strong_level(s)
            if lv:
                cand[k], kind[k] = lv, "strong"
            elif s.endswith(":") and len(s) <= 70 and (s[0].isupper() or s[0].isdigit() or EMOJI_RE.match(s)):
                cand[k], kind[k] = 4, "label"
            elif weak_ok(s):
                cand[k], kind[k] = 3, "weak"
    # numérotés courts sans ponctuation finale : titres forts
    # suites de candidats (sommaire / listes de noms) : on les rétrograde
    k = 0
    while k < n:
        if cand[k] and kind[k] != "md":
            run = [k]
            m = next_nonblank(k)
            while m < n and cand[m] and kind[m] != "md":
                run.append(m)
                m = next_nonblank(m)
            if len(run) >= 4:
                for r in run:
                    cand[r] = 0
                    items[r] = ("tocline", items[r][1])
            elif len(run) >= 2:
                for pos_, r in enumerate(run[:-1]):
                    if kind[r] in ("weak", "label"):
                        nx_ = run[pos_ + 1]
                        if kind[r] == "weak" and kind[nx_] == "strong" and cand[nx_] == 3 and re.match(r"^\d+\.\d+", items[nx_][1]):
                            cand[r] = 2        # titre de section au-dessus de ses sous-sections numérotées
                        else:
                            cand[r] = 0
                # le dernier n'est un titre que s'il est suivi d'un corps de texte
                last = run[-1]
                if kind[last] == "weak":
                    nx = next_nonblank(last)
                    if nx >= n or items[nx][0] in ("rule",):
                        cand[last] = 0
            k = m if m > k else k + 1
        else:
            k += 1
    # zones de sommaire : longues suites de lignes courtes sans ponctuation finale contenant plusieurs titres
    def tocish(k):
        it = items[k]
        if it[0] == "tocline":
            return True
        if it[0] != "text":
            return False
        if cand[k] and kind[k] != "md":
            return True
        t = it[1]
        return len(t) <= 70 and t[-1] not in ".!?»”" and not (re.search(r"\s:\s+\S", t))
    k = 0
    while k < n:
        if items[k][0] == "text" and tocish(k):
            run = [k]
            m = next_nonblank(k)
            while m < n and tocish(m):
                run.append(m)
                m = next_nonblank(m)
            if len(run) >= 6 and sum(1 for r in run if cand[r] and kind[r] != "md") >= 3:
                for r in run:
                    cand[r] = 0
                    if items[r][0] == "text":
                        items[r] = ("tocline", items[r][1])
            k = m if m > k else k + 1
        else:
            k += 1
    # titres faibles isolés : exiger un corps à la suite et un contexte (ligne vide / début / titre avant)
    for k in range(n):
        if cand[k] and kind[k] in ("weak",):
            nx = next_nonblank(k)
            pv = prev_nonblank(k)
            if nx >= n or items[nx][0] in ("rule",):
                cand[k] = 0
                continue
            blank_before = k == 0 or items[k - 1][0] == "blank"
            after_head = pv >= 0 and cand[pv] and items[pv][0] != "tocline"
            after_rule = pv >= 0 and items[pv][0] == "rule"
            nxt_len = len(items[nx][1]) if items[nx][0] == "text" else 999
            next_is_list = items[nx][0] in ("bullet", "num", "table")
            if not (blank_before or after_head or after_rule or (next_is_list and len(items[k][1]) <= 60)):
                cand[k] = 0
                continue
            if items[nx][0] == "text" and nxt_len < len(items[k][1]) and not blank_before:
                cand[k] = 0
        if cand[k] and kind[k] == "label":
            nx = next_nonblank(k)
            if nx >= n:
                cand[k] = 0

    # ---- rendu
    k = 0
    first_text_done = False
    tt = fold(title)
    while k < n:
        it = items[k]
        typ = it[0]
        if typ == "blank":
            k += 1
        elif typ == "rule":
            d.html.append("<hr>")
            k += 1
        elif typ == "table":
            rows = it[1]
            d.html.append(table_html(rows, "doc-table"))
            d.text.append(rows_text(rows))
            d.table_notes.append((len(rows), it[2]))
            k += 1
        elif typ == "callout":
            grp = []
            while k < n and items[k][0] == "callout":
                grp.append(items[k][1])
                k += 1
            d.html.append('<div class="callout">%s</div>' % "".join("<p>%s</p>" % inline(g) for g in grp))
            d.text.extend(grp)
        elif typ in ("bullet", "num"):
            # liste (avec imbrication)
            seq = []
            while k < n and items[k][0] in ("bullet", "num", "blank"):
                if items[k][0] == "blank":
                    nx = k + 1
                    while nx < n and items[nx][0] == "blank":
                        nx += 1
                    if nx < n and items[nx][0] in ("bullet", "num") and not cand[nx]:
                        k = nx
                        continue
                    break
                seq.append(items[k])
                k += 1
            render_list(d, seq)
        elif typ == "tocline":
            grp = []
            while k < n and items[k][0] in ("tocline", "blank"):
                if items[k][0] == "tocline":
                    grp.append(items[k][1])
                k += 1
            d.html.append('<div class="doc-toc">%s</div>' % "".join("<p>%s</p>" % inline(g) for g in grp))
            d.text.extend(grp)
        elif typ == "mdh":
            d.heading(cand[k], it[2])
            k += 1
        elif typ == "text":
            s = it[1]
            if cand[k]:
                if (not first_text_done) and fold(s).strip(" .:-") and (tt.startswith(fold(s).strip(" .:-")) or fold(s).strip(" .:-") in tt) and len(s) > 3:
                    d.heading(2, s, cls="doc-title")
                else:
                    d.heading(cand[k], s)
            else:
                m = LEADER_RE.match(s)
                if m:
                    d.html.append('<p class="leader"><span>%s</span><b>%s</b></p>' % (inline(m.group(1)), m.group(2)))
                    d.text.append(s)
                else:
                    d.para(s)
            first_text_done = True
            k += 1
        else:
            k += 1
    return d

def render_list(d, seq):
    """seq : éléments ('bullet'|'num', indent, ...). Génère des <ul>/<ol> imbriquées."""
    out = []
    stack = []   # [(indent, tag)]
    first = True
    def open_list(tag, ind):
        cls = ' class="lit"' if tag == "ol" else ""
        out.append("<%s%s>" % (tag, cls))
        stack.append((ind, tag))
    texts = []
    for it in seq:
        typ, ind = it[0], it[1]
        tag = "ol" if typ == "num" else "ul"
        if not stack:
            open_list(tag, ind)
        else:
            while len(stack) > 1 and ind < stack[-1][0]:
                out.append("</li></%s>" % stack.pop()[1])
            if ind > stack[-1][0]:
                open_list(tag, ind)
            else:
                out.append("</li>")
                if stack[-1][1] != tag and len(stack) == 1:
                    out.append("</%s>" % stack.pop()[1])
                    open_list(tag, ind)
        if typ == "num":
            out.append('<li><span class="n">%s</span> %s' % (esc(it[2]), inline(it[3])))
            texts.append(it[2] + " " + it[3])
        else:
            out.append("<li>%s" % inline(it[2]))
            texts.append(it[2])
    while stack:
        out.append("</li></%s>" % stack.pop()[1])
    d.html.append("".join(out))
    d.text.append("\n".join("• " + t for t in texts))

# --------------------------------------------------------------------------- feuilles de calcul
SHEET_MARK = re.compile(r"^#{5}\s*(?:FEUILLE|ONGLET)\s*:\s*(.*?)\s*#*\s*$")

def split_sheet_sections(body, cfg, log):
    """Retourne une liste de ('h', nom d'onglet) | ('p', texte) | ('t', rows). Un onglet = un tableau."""
    lines = body.replace("\r", "").split("\n")
    tabs, name, cur = [], None, []
    for ln in lines:
        m = SHEET_MARK.match(ln)
        if m:
            if cur or name is not None:
                tabs.append((name, cur))
            name, cur = m.group(1), []
        else:
            cur.append(ln)
    tabs.append((name, cur))
    sections = []
    for name, tl in tabs:
        if name is not None:
            sections.append(("h", name))
        if not any(t.strip() for t in tl):
            continue
        if any(" | " in l for l in tl):
            rows = [[c.strip() for c in l.split(" | ")] if l.strip() else [] for l in tl]
        else:                              # onglet exporté en CSV (virgules)
            rows = [r for r in csv.reader(io.StringIO("\n".join(tl)))]
        sections.extend(sheet_rows_to_sections(rows, cfg, log))
    return sections

def sheet_rows_to_sections(rows, cfg, log):
    """Regroupe les lignes : lignes à 1 cellule = texte, suites de lignes à ≥2 cellules = tableau.
    Un en-tête isolé (ligne seule suivie d'un intertitre puis de données) est rattaché au tableau suivant."""
    sections = []
    tbl = []
    pending = None

    def norm(t):
        w = max(len(r) for r in t)
        t = [r + [""] * (w - len(r)) for r in t]
        keep = [j for j in range(w) if any(r[j].strip() for r in t)]
        return [[r[j] for j in keep] for r in t]

    def emit_pending_as_text():
        nonlocal pending
        if pending:
            sections.append(("p", " — ".join(c for c in pending if c.strip())))
            pending = None

    def flush():
        nonlocal tbl, pending
        if not tbl:
            return
        t = tbl
        tbl = []
        if pending and len(t) >= 1 and abs(len([c for c in pending if c.strip()]) - max(len(r) for r in t)) <= 2:
            t = [pending] + t
            pending = None
        elif pending:
            emit_pending_as_text()
        if len(t) == 1 and sum(1 for c in t[0] if c.strip()) >= 3:
            pending = t[0]           # en-tête seul : on attend les données
            return
        if len(t) == 1 and sum(1 for c in t[0] if c.strip()) <= 2:
            sections.append(("p", " — ".join(c for c in t[0] if c.strip())))
            return
        sections.append(("t", redact_rows(norm(t), cfg, log)))

    gap = 0
    for r in rows:
        nz = [c for c in r if c.strip()]
        if not nz:
            gap += 1
            if gap >= 2 or not tbl:
                flush()
                if gap >= 2:
                    emit_pending_as_text()
            continue
        gap = 0
        if len(nz) >= 2:
            tbl.append(list(r))
        elif tbl and (len(r) >= 3 or len(tbl) >= 2):
            tbl.append(list(r))      # ligne dont une seule cellule est remplie, au sein d'un tableau
        else:
            flush()
            sections.append(("p", nz[0]))
    flush()
    emit_pending_as_text()
    return sections

def parse_sheet(body, title, cfg, log):
    d = Doc(title)
    secs = split_sheet_sections(body, cfg, log)
    open_tab = False
    for typ, val in secs:
        if typ == "h":
            if open_tab:
                d.html.append("</div>")
            d.html.append('<div class="sheet-tab" data-tab="%s">' % html.escape(val, quote=True))
            open_tab = True
            d.heading(2, val)
        elif typ == "p":
            d.para(val)
        else:
            d.html.append(table_html(val, "data-table"))
            d.text.append(rows_text(val))
    if open_tab:
        d.html.append("</div>")
    if not secs:
        d.para("Aucune donnée dans la source (non documenté).")
    return d

# --------------------------------------------------------------------------- lecture des sources
def load_page(key):
    t = (CONTENT / (key + ".md")).read_text(encoding="utf-8")
    head, _, body = t.partition("\n---\n")
    meta = {}
    for l in head.split("\n")[1:]:
        m = re.match(r"- ([^:]+?) : ?(.*)$", l)
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()
    return meta, body.strip("\n")

STATUS_NORM = {
    "validé": "Validé",
    "possibilité de modifier": "Possibilité de modifier",
    "en cours de rédaction": "En cours de rédaction",
    "à modifier": "À modifier",
}

def build(args):
    cfg = json.loads((ROOT / "config" / "site.json").read_text(encoding="utf-8"))
    pages_src = json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))
    src_keys = [p["k"] for p in pages_src]
    files = sorted(p.stem for p in CONTENT.glob("*.md"))
    errors = []
    if sorted(src_keys) != files:
        errors.append("pages.json et content/*.md ne correspondent pas : %s / %s" % (sorted(set(src_keys) - set(files)), sorted(set(files) - set(src_keys))))
    # --- wiki : chemin d'origine de chaque page (champ « URL: »), ordre = ordre des renvois de l'accueil puis arborescence
    wcfg = cfg.get("wiki", {})
    wiki_path = {}
    for p_ in pages_src:
        if p_["k"].startswith("wiki-") and (CONTENT / (p_["k"] + ".md")).exists():
            u_, _l = wikimd.parse_page(load_page(p_["k"])[1])
            if u_:
                wiki_path[p_["k"]] = u_.split(wcfg.get("base", wikimd.WIKI_BASE) + "/", 1)[-1].strip("/")
    path_to_key = {v: k for k, v in wiki_path.items()}
    tops = []
    if "wiki-accueil" in wiki_path:
        _u, acc_lines = wikimd.parse_page(load_page("wiki-accueil")[1])
        tops = [m_.group(1).strip("/") for m_ in re.finditer(r'content-ref url="([^"]+)"', "\n".join(acc_lines))]
    def wrank(k):
        segs = wiki_path.get(k, "").split("/")
        t = segs[0]
        return (-1 if k == "wiki-accueil" else (tops.index(t) if t in tops else len(tops)), segs)
    cats = cfg["categories"]
    wcat = wcfg.get("category")
    if wcat:
        cfg["order"][wcat] = sorted(wiki_path, key=wrank)
    order = {}
    for c in cats:
        o = cfg["order"].get(c, [])
        extra = sorted(p["k"] for p in pages_src if p["cat"] == c and p["k"] not in o)
        order[c] = [k for k in o if any(p["k"] == k and p["cat"] == c for p in pages_src)] + extra
    for p in pages_src:
        if p["cat"] not in cats:
            cats.append(p["cat"]); order[p["cat"]] = [x["k"] for x in pages_src if x["cat"] == p["cat"]]
    rank = {k: (ci, i) for ci, c in enumerate(cats) for i, k in enumerate(order[c])}
    pages_src.sort(key=lambda p: rank[p["k"]])

    acc_cfg = cfg["access"]
    def access_of(k):
        if any(k.startswith(pref) for pref in acc_cfg.get("prefix_public", [])):
            return "public"
        if k in acc_cfg["public"]:
            return "public"
        if k in acc_cfg["joueurs"]:
            return "joueurs"
        return acc_cfg.get("default", "staff")

    collect_handles(cfg, pages_src)
    manifest_pages, search_docs, page_files = [], [], {}
    report = {"redactions": [], "checks": [], "tables": []}
    for p in pages_src:
        k = p["k"]
        meta, body = load_page(k)
        m = p.get("m") or {}
        title = p["title"]
        status = m.get("red", "").strip()
        status_label = STATUS_NORM.get(fold(status), status) if status else ""
        log = []
        withheld = cfg["withheld"].get(k)
        is_sheet = k.startswith("sheet-")
        is_wiki = k in wiki_path
        if is_wiki:
            body_r = redact_text(body, cfg, log)
            _u, wlines = wikimd.parse_page(body_r)
            wk = wikimd.Wiki(path_to_key, wcfg.get("base", wikimd.WIKI_BASE))
            w_html = wk.render(wlines)
            d = Doc(title)
            d.html.append(w_html); d.text.extend(wk.text); d.toc = wk.toc
            if wk.unknown:
                errors.append("%s : balises GitBook non gérées : %s" % (k, wk.unknown[:3]))
            exp = tokens(wikimd.expected_tokens(wlines))
            got = tokens(html.unescape(re.sub(r"<[^>]+>", " ", w_html)))
            if exp != got:
                idx = next((i for i, (a, b) in enumerate(zip(exp, got)) if a != b), min(len(exp), len(got)))
                errors.append("%s : écart de contenu au mot #%d (source %r / rendu %r) ; %d vs %d mots" % (k, idx, exp[idx:idx + 5], got[idx:idx + 5], len(exp), len(got)))
            check = ("wiki", len(exp), len(got))
        elif withheld:
            body_r = ""
            d = Doc(title)
            d.html.append('<div class="callout withheld"><p><strong>Contenu non publié.</strong> %s</p></div>' % esc(withheld))
            d.text.append(withheld)
            check = ("withheld", 0, 0)
        else:
            body_r = redact_text(body, cfg, log)
            d = parse_sheet(body_r, title, cfg, log) if is_sheet else parse_doc(body_r, title, k)
            # --- contrôle d'intégrité : tous les mots de la source se retrouvent dans la page rendue
            rendered = re.sub(r"<[^>]+>", " ", "".join(d.html))
            rendered = html.unescape(rendered)
            exp = tokens(re.sub(r"^#{5}\s*(?:FEUILLE|ONGLET)\s*:|#{5}\s*$", "", re.sub(r"\\([\[\]*_#>~`|])", r"\1", body_r), flags=re.M))
            got = tokens(rendered)
            if is_sheet:
                # feuilles : comparaison en multiensemble, hors cellules volontairement masquées
                red_tokens = Counter(t for kind, v in log if kind.startswith("colonne") for t in tokens(v))
                diff = Counter(exp) - Counter(got) - red_tokens
                check = ("sheet", len(exp), len(got), sum(diff.values()))
                if diff:
                    errors.append("%s : mots manquants dans le rendu (feuille) : %s" % (k, list(diff.elements())[:10]))
            else:
                if exp != got:
                    # localise le premier écart
                    idx = next((i for i, (a, b) in enumerate(zip(exp, got)) if a != b), min(len(exp), len(got)))
                    errors.append("%s : écart de contenu au mot #%d (source %r / rendu %r) ; %d vs %d mots" % (k, idx, exp[idx:idx + 5], got[idx:idx + 5], len(exp), len(got)))
                check = ("doc", len(exp), len(got))
        for kind, v in log:
            report["redactions"].append((k, kind, v if kind != "e-mail" else v[:2] + "…@" + v.split("@")[-1]))
        text = "\n".join(d.text)
        html_body = "".join(d.html)
        words = len(tokens(text))
        access = access_of(k)
        entry = {
            "k": k, "t": title, "c": p["cat"], "s": status_label, "a": access,
            "kw": m.get("kw", "").strip(" ,"), "res": m.get("res", "").strip(),
            "resp": m.get("resp", "").strip(), "rem": m.get("rem", "").strip(),
            "dom": m.get("dom", "").strip(), "acc_src": m.get("acc", "").strip(),
            "meta": bool(m), "w": words,
            "arch": k in cfg["archives"], "withheld": bool(withheld), "sheet": is_sheet,
        }
        if is_wiki:
            entry["wiki"] = True
            entry["u"] = wiki_path[k]
        manifest_pages.append(entry)
        search_docs.append({"k": k, "x": text})
        page_files[k] = {"html": html_body, "toc": d.toc}
        report["checks"].append((k,) + tuple(check))
        for rows, nc in d.table_notes:
            report["tables"].append((k, rows, nc))

    manifest = {
        "title": cfg["title"], "subtitle": cfg["subtitle"], "snapshot": cfg["snapshot"],
        "categories": [{"name": c, "slug": slugify(c), "keys": order[c]} for c in cats],
        "groups": cfg["groups"], "levels": cfg["access_levels"],
        "pages": manifest_pages, "count": len(manifest_pages),
    }
    return cfg, manifest, search_docs, page_files, report, errors

def cite_text(texts, c):
    """Extrait exact d'un texte source : de c['from'] jusqu'à c['to'] (ou la fin de la phrase). None si introuvable."""
    flat = texts.get(c["k"])
    if flat is None:
        return None
    i = flat.find(c["from"])
    if i < 0:
        return None
    if c.get("to"):
        j = flat.find(c["to"], i)
        if j < 0:
            return None
        seg = flat[i:j + len(c["to"])]
    else:
        seg = flat[i:]
        m = re.search(r"(?<=[.!?»])\s|\n", seg)
        seg = seg[:m.start()] if m else seg
    return re.sub(r"\s*\n\s*", " · ", seg).strip().replace("• ", "")

def resolve_contradictions(entries, texts, pages, errors):
    out = []
    for e in entries:
        items = []
        for c in e.get("sources", []):
            t = cite_text(texts, c)
            if t is None:
                errors.append("contradictions : citation introuvable dans %s : %r" % (c["k"], c["from"]))
                continue
            items.append({"k": c["k"], "a": pages[c["k"]]["a"], "text": t})
        links = [{"k": k, "a": pages[k]["a"]} for k in e.get("links", []) if k in pages]
        out.append({"titre": e["titre"], "note": e.get("note", ""), "check": e.get("check", ""), "items": items, "links": links})
    return out

def resolve_glossary(entries, texts, pages, errors):
    """Chaque définition est une citation exacte du texte source (aucune reformulation)."""
    out = []
    for g in entries:
        c = g["cite"]
        txt = texts.get(c["k"])
        if txt is None:
            errors.append("glossaire : source introuvable pour %r (%s)" % (g["term"], c["k"]))
            continue
        flat = txt
        i = flat.find(c["from"])
        if i < 0:
            errors.append("glossaire : citation introuvable pour %r dans %s : %r" % (g["term"], c["k"], c["from"]))
            continue
        if c.get("to"):
            j = flat.find(c["to"], i)
            if j < 0:
                errors.append("glossaire : fin de citation introuvable pour %r : %r" % (g["term"], c["to"]))
                continue
            seg = flat[i:j + len(c["to"])]
        else:
            seg = flat[i:]
            m = re.search(r"(?<=[.!?»])\s|\n", seg)
            seg = seg[:m.start()] if m else seg
        seg = re.sub(r"\s*\n\s*", " · ", seg).strip()
        seg = seg.replace("• ", "")
        out.append({"id": slugify(g["term"]), "term": g["term"], "aliases": g.get("aliases", []), "cat": g.get("cat", ""),
                    "def": seg, "auto": g.get("auto", True), "k": c["k"], "a": pages[c["k"]]["a"], "pages": g.get("pages", [c["k"]])})
    return sorted(out, key=lambda x: fold(x["term"]))

def write_js(path, var, obj, extra=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    path.write_text("window.EW=window.EW||{pages:{}};%s%s;\n" % (var, data) if not extra else extra % data, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audience", choices=LEVELS, default="staff", help="niveau maximal inclus (public < joueurs < staff)")
    ap.add_argument("--out", help="dossier de sortie (défaut : . pour staff, dist/<audience> sinon)")
    ap.add_argument("--all", action="store_true", help="génère le site complet (data/) ET dist/joueurs/ (hébergement protégé)")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    if args.all:
        import subprocess
        for extra in ([], ["--audience", "joueurs"]):
            r = subprocess.run([sys.executable, str(Path(__file__).resolve())] + extra + (["--check"] if args.check else []))
            if r.returncode:
                sys.exit(r.returncode)
        return
    cfg, manifest, search_docs, page_files, report, errors = build(args)

    search_all = {x["k"]: x["x"] for x in search_docs}
    manifest_all = {p["k"]: p for p in manifest["pages"]}
    maxlvl = LEVELS.index(args.audience)
    keep = {p["k"] for p in manifest["pages"] if LEVELS.index(p["a"]) <= maxlvl}
    manifest["pages"] = [p for p in manifest["pages"] if p["k"] in keep]
    for c in manifest["categories"]:
        c["keys"] = [k for k in c["keys"] if k in keep]
    manifest["categories"] = [c for c in manifest["categories"] if c["keys"]]
    manifest["count"] = len(manifest["pages"])
    manifest["audience"] = args.audience
    search_docs = [s for s in search_docs if s["k"] in keep]

    out = Path(args.out) if args.out else (ROOT if args.audience == "staff" else ROOT / "dist" / args.audience)
    out = out if out.is_absolute() else Path.cwd() / out
    if out != ROOT:
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        for f in ["index.html"]:
            shutil.copy2(ROOT / f, out / f)
        shutil.copytree(ROOT / "assets", out / "assets")
    data = out / "data"
    if data.exists():
        shutil.rmtree(data)
    (data / "pages").mkdir(parents=True)
    cpath = ROOT / "config" / "contradictions.json"
    contra = resolve_contradictions(json.loads(cpath.read_text(encoding="utf-8")) if cpath.exists() else [], search_all, manifest_all, errors)
    for c_ in contra:
        c_["items"] = [i_ for i_ in c_["items"] if i_["k"] in keep]
        c_["links"] = [l_ for l_ in c_["links"] if l_["k"] in keep]
    write_js(data / "contradictions.js", "window.EW.contradictions=", contra)
    glossary_path = ROOT / "config" / "glossary.json"
    glossary = resolve_glossary(json.loads(glossary_path.read_text(encoding="utf-8")) if glossary_path.exists() else [], search_all, manifest_all, errors)
    keep_g = []
    for g in glossary:
        if g["k"] in keep:
            g["pages"] = [k for k in g["pages"] if k in keep]
            keep_g.append(g)
    glossary = keep_g
    for e_ in errors:
        pass
    write_js(data / "manifest.js", "window.EW.manifest=", manifest)
    write_js(data / "glossary.js", "window.EW.glossary=", glossary)
    write_js(data / "search.js", "window.EW.search=", search_docs)
    for k in keep:
        write_js(data / "pages" / (k + ".js"), "window.EW.pages[%s]=" % json.dumps(k), page_files[k])

    # ------------------------------------------------------------------ rapport
    print("Pages dans pages.json      : %d" % len(json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))))
    print("Fichiers content/*.md      : %d" % len(list(CONTENT.glob("*.md"))))
    print("Pages générées (%-8s)   : %d" % (args.audience, len(keep)))
    lv = Counter(p["a"] for p in manifest["pages"])
    print("Répartition accès          :", dict(lv))
    print("Redactions appliquées      : %d" % len(report["redactions"]))
    for r in report["redactions"]:
        print("   -", r)
    nb_bad = len(errors)
    print("Contrôle d'intégrité       : %s" % ("OK (aucun mot manquant)" if not nb_bad else "%d ERREUR(S)" % nb_bad))
    for e in errors:
        print("   !", e)
    if args.verbose:
        for k, rows, nc in report["tables"]:
            print("table", k, rows, "x", nc)
    if args.check and (errors or len(keep) == 0):
        sys.exit(1)

if __name__ == "__main__":
    main()
