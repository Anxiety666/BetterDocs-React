"""Conversion des pages du wiki WikiWood (Markdown GitBook) en HTML.

Gère : titres, listes imbriquées, tableaux, encadrés {% hint %}, renvois {% content-ref %},
liens internes (résolus vers les pages du site), images, <br>, <mark>, <u>, **gras**, *italique*, `code`.
Le texte n'est jamais modifié ; seules les balises de mise en forme sont interprétées.
"""
import html
import re

WIKI_BASE = "https://wiki.elderwood-rp.com"
TAG_RE = re.compile(r"\{%\s*(\w[\w-]*)\s*([^%]*?)\s*%\}")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
ALLOWED = re.compile(r"<(/?)(br|u|mark|p|img)((?:\s+[a-z-]+=\"[^\"]*\")*)\s*/?>", re.I)


def esc(s):
    return html.escape(s, quote=False)


class Wiki:
    def __init__(self, path_to_key, base=WIKI_BASE):
        self.map = path_to_key          # "bestiaire/rang-a" -> clé de page
        self.base = base
        self.toc = []
        self.ids = {}
        self.text = []
        self.unknown = []

    # ------------------------------------------------------------ liens
    def link(self, url):
        """Retourne (href, interne?)"""
        if url.startswith(("http://", "https://")):
            if url.startswith(self.base + "/") and not url.startswith(self.base + "/media/"):
                path = url[len(self.base):]
                k = self.map.get(path.strip("/").split("#")[0])
                if k:
                    return "#/p/" + k, True
            return url, False
        if url.startswith("/media/"):
            return self.base + url, False
        if url.startswith("/"):
            k = self.map.get(url.strip("/").split("#")[0].split("?")[0])
            if k:
                return "#/p/" + k, True
        return None, False

    # ------------------------------------------------------------ en ligne
    def inline(self, s):
        holders = []

        def hold(h):
            holders.append(h)
            return "\u0000%d\u0000" % (len(holders) - 1)

        # balises HTML autorisées
        def tag(m):
            close, name, attrs = m.group(1), m.group(2).lower(), m.group(3) or ""
            if name == "br":
                return hold("<br>")
            if name in ("u",):
                return hold("</u>" if close else "<u>")
            if name == "p":
                return hold("")      # <p align="center"> : enveloppe seule
            if name == "mark":
                if close:
                    return hold("</mark>")
                col = re.search(r'color:\s*([a-z]+)', attrs)
                return hold('<mark class="mk-%s">' % (col.group(1) if col else "yellow"))
            if name == "img":
                src = re.search(r'src="([^"]+)"', attrs)
                w = re.search(r'width="(\d+)"', attrs)
                if not src:
                    return ""
                href, _ = self.link(src.group(1))
                return hold('<img class="wimg" loading="lazy" src="%s" alt=""%s>' % (html.escape(href or src.group(1), quote=True), (' style="max-width:%spx"' % w.group(1)) if w else ""))
            return ""
        s = ALLOWED.sub(tag, s)
        # images Markdown
        def img(m):
            href, _ = self.link(m.group(2))
            return hold('<img class="wimg" loading="lazy" src="%s" alt="%s">' % (html.escape(href or m.group(2), quote=True), html.escape(m.group(1), quote=True)))
        s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)", img, s)
        # liens
        def lnk(m):
            href, internal = self.link(m.group(2).strip())
            label = self.inline(m.group(1))
            if href is None:
                return label            # cible inconnue : le texte reste visible
            if internal:
                return hold('<a href="%s">%s</a>' % (html.escape(href, quote=True), label))
            return hold('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (html.escape(href, quote=True), label))
        s = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", lnk, s)
        s = esc(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)([^*]+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
        s = re.sub(r"(?<![\w_])_(?!\s)([^_]+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", s)
        s = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>~])", r"\1", s)
        s = re.sub(r"\u0000(\d+)\u0000", lambda m: holders[int(m.group(1))], s)
        return s

    def plain(self, s):
        s = ALLOWED.sub(" ", s)
        s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\(([^)\s]+)[^)]*\)", r"\1", s)
        s = re.sub(r"\*\*|`", "", s)
        s = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>~])", r"\1", s)
        return re.sub(r"\s+", " ", s).strip()

    def anchor(self, text):
        import unicodedata
        base = unicodedata.normalize("NFD", text.lower())
        base = "".join(c for c in base if not unicodedata.combining(c))
        base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")[:60] or "section"
        n = self.ids.get(base, 0) + 1
        self.ids[base] = n
        return base if n == 1 else "%s-%d" % (base, n)

    # ------------------------------------------------------------ blocs
    def render(self, lines):
        out = []
        i, n = 0, len(lines)
        para = []

        def flush():
            if para:
                txt = "\n".join(para)
                out.append("<p>%s</p>" % self.inline(txt).replace("\n", " "))
                self.text.append(self.plain(txt))
                para.clear()

        while i < n:
            ln = lines[i]
            s = ln.strip()
            if not s:
                flush(); i += 1; continue
            m = TAG_RE.fullmatch(s)
            if m:
                flush()
                name, arg = m.group(1), m.group(2)
                if name == "hint":
                    style = (re.search(r'style="(\w+)"', arg) or [None, "info"])[1]
                    j = i + 1
                    inner = []
                    while j < n and not re.fullmatch(r"\{%\s*endhint\s*%\}", lines[j].strip()):
                        inner.append(lines[j]); j += 1
                    sub = Wiki(self.map, self.base); sub.ids = self.ids
                    inner_html = sub.render(inner)
                    self.text.extend(sub.text)
                    out.append('<div class="hint hint-%s" role="note">%s</div>' % (style, inner_html))
                    i = j + 1; continue
                if name == "content-ref":
                    j = i + 1
                    inner = []
                    while j < n and not re.fullmatch(r"\{%\s*endcontent-ref\s*%\}", lines[j].strip()):
                        inner.append(lines[j]); j += 1
                    body = " ".join(x.strip() for x in inner if x.strip())
                    out.append('<p class="ref">%s</p>' % self.inline(body))
                    self.text.append(self.plain(body))
                    i = j + 1; continue
                if name.startswith("end"):
                    i += 1; continue
                self.unknown.append(s)
                i += 1; continue
            if s.startswith("```"):
                flush()
                j = i + 1; code = []
                while j < n and not lines[j].strip().startswith("```"):
                    code.append(lines[j]); j += 1
                out.append("<pre><code>%s</code></pre>" % esc("\n".join(code)))
                self.text.append("\n".join(code))
                i = j + 1; continue
            mh = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", s)
            if mh:
                flush()
                lvl = min(5, len(mh.group(1)) + 1)
                txt = self.plain(mh.group(2))
                hid = self.anchor(txt)
                out.append('<h%d id="%s">%s</h%d>' % (lvl, hid, self.inline(mh.group(2)), lvl))
                self.text.append("\n" + txt)
                if lvl <= 3:
                    self.toc.append({"id": hid, "t": txt, "l": lvl})
                i += 1; continue
            if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s):
                flush(); out.append("<hr>"); i += 1; continue
            if s.startswith("|"):
                flush()
                j = i
                rows = []
                while j < n and lines[j].strip().startswith("|"):
                    rows.append(lines[j].strip()); j += 1
                tab = [r for r in rows if not SEP_RE.match(r)]
                cells = []
                for r in tab:
                    r = r.strip()
                    if r.startswith("|"):
                        r = r[1:]
                    if r.endswith("|") and not r.endswith("\\|"):
                        r = r[:-1]
                    cells.append([c.strip() for c in re.split(r"(?<!\\)\|", r)])
                w = max(len(c) for c in cells)
                cells = [c + [""] * (w - len(c)) for c in cells]
                has_head = any(SEP_RE.match(r) for r in rows)
                h = ['<div class="tbl-wrap"><table class="doc-table">']
                body = cells
                if has_head and cells:
                    h.append("<thead><tr>%s</tr></thead>" % "".join("<th scope=\"col\">%s</th>" % self.inline(c) for c in cells[0]))
                    body = cells[1:]
                h.append("<tbody>")
                for r in body:
                    h.append("<tr>%s</tr>" % "".join("<td>%s</td>" % self.inline(c) for c in r))
                h.append("</tbody></table></div>")
                out.append("".join(h))
                self.text.append("\n".join(" | ".join(self.plain(c) for c in r if c.strip()) for r in cells))
                i = j; continue
            if s.startswith(">"):
                flush()
                j = i; q = []
                while j < n and lines[j].strip().startswith(">"):
                    q.append(re.sub(r"^\s*>\s?", "", lines[j])); j += 1
                sub = Wiki(self.map, self.base); sub.ids = self.ids
                out.append("<blockquote>%s</blockquote>" % sub.render(q))
                self.text.extend(sub.text)
                i = j; continue
            ml = LIST_RE.match(ln.replace("\t", "    "))
            if ml:
                flush()
                items = []
                j = i
                while j < n:
                    l2 = lines[j].replace("\t", "    ")
                    m2 = LIST_RE.match(l2)
                    if m2:
                        items.append([len(m2.group(1)), m2.group(2), m2.group(3)])
                        j += 1
                    elif l2.strip() and items and l2.startswith(" ") and not TAG_RE.fullmatch(l2.strip()):
                        items[-1][2] += "\n" + l2.strip(); j += 1
                    elif not l2.strip() and j + 1 < n and LIST_RE.match(lines[j + 1].replace("\t", "    ")) and items:
                        j += 1
                    else:
                        break
                out.append(self.list_html(items))
                i = j; continue
            para.append(ln.strip())
            i += 1
        flush()
        return "".join(out)

    def list_html(self, items):
        out, stack = [], []
        for ind, mark, txt in items:
            tag = "ol" if mark[0].isdigit() else "ul"
            if not stack:
                out.append("<%s>" % tag); stack.append((ind, tag))
            else:
                while len(stack) > 1 and ind < stack[-1][0]:
                    out.append("</li></%s>" % stack.pop()[1])
                if ind > stack[-1][0]:
                    out.append("<%s>" % tag); stack.append((ind, tag))
                else:
                    out.append("</li>")
            out.append("<li>%s" % self.inline(txt).replace("\n", " "))
            self.text.append("• " + self.plain(txt))
        while stack:
            out.append("</li></%s>" % stack.pop()[1])
        return "".join(out)


def parse_page(body):
    """Sépare l'en-tête (# Titre, URL: …) du corps. Retourne (url|None, lignes_du_corps)."""
    lines = body.replace("\r", "").split("\n")
    url = None
    k = 0
    while k < len(lines) and not lines[k].strip():
        k += 1
    if k < len(lines) and re.match(r"^#\s+", lines[k]):
        k += 1
        while k < len(lines) and not lines[k].strip():
            k += 1
    if k < len(lines) and lines[k].startswith("URL:"):
        url = lines[k][4:].strip()
        k += 1
    return url, lines[k:]


def expected_tokens(lines):
    """Mots que la page rendue doit contenir (syntaxe GitBook exclue)."""
    out = []
    for ln in lines:
        s = ln.strip()
        if TAG_RE.fullmatch(s):
            continue
        s = ALLOWED.sub(" ", s)
        s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\(([^)\s]+)[^)]*\)", r"\1", s)
        out.append(s)
    return "\n".join(out)
