#!/usr/bin/env python3
"""Serveur du site Elderwood protégé par mot de passe (HTTP Basic), sans dépendance.

Aucun fichier (page, données, recherche) n'est envoyé avant authentification.

Variables d'environnement :
  SITE_STAFF_PASSWORD    mot de passe « staff » : donne accès à TOUT le site (212 pages)        [obligatoire]
  SITE_STAFF_USER        identifiant staff (défaut : staff)
  SITE_PLAYER_PASSWORD   mot de passe « joueurs » : site SANS les pages staff (dist/joueurs)     [facultatif]
  SITE_PLAYER_USER       identifiant joueurs (défaut : joueurs)
  PORT                   port d'écoute (fourni par Render ; défaut 8000)

Seuls index.html, assets/ et data/ (ou dist/joueurs/…) sont servis : content/, config/, build.py… restent privés.
"""
import base64, hmac, mimetypes, os, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
STAFF_PW = os.environ.get("SITE_STAFF_PASSWORD", "")
PLAYER_PW = os.environ.get("SITE_PLAYER_PASSWORD", "")
STAFF_USER = os.environ.get("SITE_STAFF_USER", "staff")
PLAYER_USER = os.environ.get("SITE_PLAYER_USER", "joueurs")
ALLOWED_TOP = {"index.html", "assets", "data"}

LEVELS = []          # (identifiant, mot de passe, dossier servi)
if STAFF_PW:
    LEVELS.append((STAFF_USER, STAFF_PW, ROOT))
if PLAYER_PW:
    LEVELS.append((PLAYER_USER, PLAYER_PW, ROOT / "dist" / "joueurs"))

mimetypes.add_type("application/javascript", ".js")


def authenticate(header):
    """Retourne le dossier à servir, ou None. Comparaisons à temps constant."""
    if not header or not header.startswith("Basic "):
        return None
    try:
        user, _, pw = base64.b64decode(header[6:]).decode("utf-8").partition(":")
    except Exception:
        return None
    found = None
    for u, p, root in LEVELS:
        ok = hmac.compare_digest(user.encode(), u.encode()) & hmac.compare_digest(pw.encode(), p.encode())
        if ok:
            found = root
    return found


class Handler(BaseHTTPRequestHandler):
    server_version = "Elderwood"
    sys_version = ""

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, self.path.split("?")[0]))   # pas d'identifiants dans les logs

    def deny(self):
        time.sleep(1)                      # freine les essais répétés
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Elderwood - acces restreint", charset="UTF-8"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write("Accès restreint : identifiant et mot de passe requis.\n".encode())

    def respond(self, head_only):
        root = authenticate(self.headers.get("Authorization"))
        if root is None:
            return self.deny()
        rel = unquote(urlsplit(self.path).path).lstrip("/") or "index.html"
        parts = [p for p in rel.split("/") if p]
        if not parts or ".." in parts or parts[0] not in ALLOWED_TOP:
            return self.not_found()
        target = (root / "/".join(parts)).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            return self.not_found()
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            return self.not_found()
        data = target.read_bytes()
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith(("text/", "application/javascript")) else ""))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "private, max-age=300")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(b"Introuvable.\n")

    def do_GET(self):
        self.respond(False)

    def do_HEAD(self):
        self.respond(True)


def main():
    if not LEVELS:
        sys.exit("SITE_STAFF_PASSWORD n'est pas défini : refus de démarrer un site sans mot de passe.")
    if PLAYER_PW and not (ROOT / "dist" / "joueurs" / "index.html").exists():
        sys.exit("SITE_PLAYER_PASSWORD est défini mais dist/joueurs/ est absent : lancer `python3 build.py --audience joueurs` et le commiter.")
    port = int(os.environ.get("PORT", "8000"))
    print("Elderwood protégé : %d niveau(x) d'accès, port %d" % (len(LEVELS), port), flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
