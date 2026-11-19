#!/usr/bin/env python3
"""Resynchronise les pages « wiki-* » depuis l'API publique du wiki.

    python3 sync_wiki.py                # télécharge et met à jour content/wiki-*.md + pages.json
    python3 sync_wiki.py --dry-run      # affiche ce qui changerait, sans écrire
    python3 sync_wiki.py --base URL     # autre adresse (tests)

Puis : python3 build.py --check   (régénère data/ et l'index de recherche).

API : GET {base}/api/nav (arborescence) et GET {base}/api/pages/<chemin> (champs `markdown`, `updated_at`).
Les fichiers produits ont le même format que ceux de content/ : en-tête, « --- », « # Titre », « URL: … », texte.
Les pages disparues du wiki sont signalées, jamais supprimées automatiquement.
"""
import argparse, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CAT = "Wiki officiel WikiWood (public)"
CANON = "https://wiki.elderwood-rp.com"      # adresse inscrite dans les pages (indépendante de --base)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "elderwood-site-sync/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def walk(nodes, out):
    """Aplatit l'arborescence : accepte [{path|slug|url, title, children|pages|items}, …]."""
    for n in nodes or []:
        if not isinstance(n, dict):
            continue
        path = n.get("path") or n.get("slug") or n.get("url") or ""
        path = path.strip("/")
        if "path" in n or "slug" in n or "url" in n:
            out.append((path, n.get("title") or n.get("name") or path.split("/")[-1]))
        for key in ("children", "pages", "items"):
            if isinstance(n.get(key), list):
                walk(n[key], out)


def key_of(path):
    return "wiki-" + (path.replace("/", "--") if path else "accueil")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://wiki.elderwood-rp.com")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    nav = get(a.base + "/api/nav")
    nodes = nav if isinstance(nav, list) else (nav.get("nav") or nav.get("pages") or nav.get("items") or [])
    flat = []
    walk(nodes, flat)
    if not flat:
        sys.exit("Arborescence vide ou format inattendu : vérifier %s/api/nav" % a.base)
    pj_path = ROOT / "pages.json"
    pages = json.loads(pj_path.read_text(encoding="utf-8"))
    by_key = {p["k"]: p for p in pages}
    seen, changed, added = set(), 0, 0
    for path, title in flat:
        k = key_of(path)
        seen.add(k)
        data = get("%s/api/pages/%s" % (a.base, path))
        md = (data.get("markdown") or "").replace("\r\n", "\n").strip("\n")
        title = data.get("title") or title
        # le markdown de l'API peut déjà commencer par « # Titre » : on n'ajoute l'en-tête que s'il manque
        body = md if re.match(r"^#\s", md) else "# %s\n%s" % (title, md)
        if not re.search(r"^URL:", body, re.M):
            lines = body.split("\n", 1)
            body = "%s\nURL: %s/%s\n%s" % (lines[0], CANON, path, lines[1] if len(lines) > 1 else "")
        text = "# %s\n\n- Catégorie : %s\n\n---\n\n%s\n" % (title, CAT, body)
        f = ROOT / "content" / (k + ".md")
        old = f.read_text(encoding="utf-8") if f.exists() else None
        if old != text:
            changed += 1 if old else 0
            added += 0 if old else 1
            print(("MAJ  " if old else "NEW  ") + k)
            if not a.dry_run:
                f.write_text(text, encoding="utf-8")
        if k not in by_key:
            pages.append({"k": k, "cat": CAT, "title": title, "id": None, "m": {}, "n": len(text)})
        else:
            by_key[k]["title"], by_key[k]["n"] = title, len(text)
    gone = [k for k in by_key if k.startswith("wiki-") and k not in seen]
    for k in gone:
        print("ABSENT du wiki (conservé) : " + k)
    if not a.dry_run:
        pj_path.write_text(json.dumps(pages, ensure_ascii=False, indent=1), encoding="utf-8")
    print("%d nouvelle(s), %d modifiée(s), %d absente(s)" % (added, changed, len(gone)))


if __name__ == "__main__":
    main()
