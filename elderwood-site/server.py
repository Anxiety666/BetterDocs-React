#!/usr/bin/env python3
"""Serveur du site Elderwood protégé par mot de passe (HTTP Basic), sans dépendance.

Aucun fichier (page, données, recherche) n'est envoyé avant authentification.

Variables d'environnement :
  SITE_STAFF_PASSWORD    mot de passe « staff » : accès à TOUT le site (212 pages)             [obligatoire]
  SITE_STAFF_USER        identifiant staff (défaut : staff)
  SITE_PLAYER_PASSWORD   mot de passe « joueurs » : site SANS les pages staff (dist/joueurs)    [facultatif]
  SITE_PLAYER_USER       identifiant joueurs (défaut : joueurs)
  SITE_VAULT_KEY         clé du coffre chiffré (vault/*.bin) : requise dès que vault/staff.bin existe (24 caractères min.)
  PORT                   port d'écoute (fourni par Render ; défaut 8000)
  REQUIRE_HTTPS          1/0 : refuse l'HTTP en clair (défaut : 1 sur Render, 0 en local)
  TRUST_PROXY            1/0 : lit l'IP client dans X-Forwarded-For (défaut : 1 sur Render, 0 en local)

Génération d'un mot de passe robuste :  python3 server.py --generate

Protections : mots de passe forts exigés au démarrage, comparaison à temps constant, blocage temporaire des
adresses après des essais ratés, HTTPS imposé, en-têtes de sécurité (CSP stricte, HSTS, anti-framing…),
GET/HEAD uniquement, délais de socket, liste blanche de fichiers (content/, config/, scripts jamais servis).
Le site est servi depuis le coffre chiffré (vault/*.bin) déchiffré EN MÉMOIRE : aucun fichier sensible en clair sur le disque.
"""
import base64, hashlib, hmac, mimetypes, os, re, secrets, string, sys, threading, time
import vaultlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
ON_RENDER = bool(os.environ.get("RENDER"))
STAFF_PW = os.environ.get("SITE_STAFF_PASSWORD", "")
PLAYER_PW = os.environ.get("SITE_PLAYER_PASSWORD", "")
STAFF_USER = os.environ.get("SITE_STAFF_USER", "staff")
PLAYER_USER = os.environ.get("SITE_PLAYER_USER", "joueurs")
REQUIRE_HTTPS = os.environ.get("REQUIRE_HTTPS", "1" if ON_RENDER else "0") == "1"
TRUST_PROXY = os.environ.get("TRUST_PROXY", "1" if ON_RENDER else "0") == "1"
ALLOWED_TOP = {"index.html", "assets", "data"}
MAX_FAILS, WINDOW, LOCK = 5, 15 * 60, 15 * 60          # 5 échecs en 15 min => blocage de 15 min

CSP = ("default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: https://wiki.elderwood-rp.com; font-src 'self'; connect-src 'self'; "
       "base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'")

mimetypes.add_type("application/javascript", ".js")


# --------------------------------------------------------------------------- mots de passe
def password_problems(pw, user):
    """Liste des raisons pour lesquelles le mot de passe est refusé (vide = accepté)."""
    out = []
    if len(pw) < 16:
        out.append("au moins 16 caractères")
    classes = sum(bool(re.search(p, pw)) for p in (r"[a-z]", r"[A-Z]", r"\d", r"[^A-Za-z0-9]"))
    if classes < 3 and len(pw) < 24:
        out.append("au moins 3 types de caractères (minuscules, majuscules, chiffres, symboles) — ou 24 caractères et plus")
    if len(set(pw)) < 8:
        out.append("au moins 8 caractères différents")
    low = pw.lower()
    if user.lower() in low or "elderwood" in low or "password" in low or "motdepasse" in low or "azerty" in low or "qwerty" in low or "123456" in low:
        out.append("ne doit contenir ni l'identifiant, ni « elderwood », ni motif courant (123456, azerty, password…)")
    return out


def generate_password(n=24):
    alphabet = string.ascii_letters + string.digits + "-_.!#%+="
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(n))
        if not password_problems(pw, "staff") and pw[0].isalnum():
            return pw


VAULT_DIR = ROOT / "vault"
USE_VAULT = (VAULT_DIR / "staff.bin").exists()
SITES = {}           # niveau -> {chemin: octets} (coffre déchiffré en mémoire)
LEVELS = []          # (identifiant, mot de passe, niveau)
if STAFF_PW:
    LEVELS.append((STAFF_USER, STAFF_PW, "staff"))
if PLAYER_PW:
    LEVELS.append((PLAYER_USER, PLAYER_PW, "joueurs"))


def load_vault():
    key = os.environ.get("SITE_VAULT_KEY", "")
    if len(key) < 24:
        sys.exit("SITE_VAULT_KEY (24 caractères minimum) est requise pour ouvrir le coffre chiffré vault/.")
    for level, fname in (("staff", "staff.bin"), ("joueurs", "joueurs.bin")):
        f = VAULT_DIR / fname
        if level == "joueurs" and not PLAYER_PW:
            continue
        try:
            SITES[level] = vaultlib.unpack(vaultlib.unseal(f.read_bytes(), key))
        except (OSError, vaultlib.VaultError) as e:
            sys.exit("Coffre %s illisible (%s) : mauvaise SITE_VAULT_KEY, ou coffre non rescellé après modification." % (fname, e))
        if "index.html" not in SITES[level]:
            sys.exit("Coffre %s incomplet." % fname)


def _h(s):
    return hashlib.sha256(s.encode("utf-8")).digest()


def authenticate(header):
    """Retourne le niveau à servir (« staff » / « joueurs »), ou None. Comparaison de hachages à temps constant (aucune fuite de longueur)."""
    if not header or not header.startswith("Basic ") or len(header) > 1024:
        return None
    try:
        user, _, pw = base64.b64decode(header[6:], validate=True).decode("utf-8").partition(":")
    except Exception:
        return None
    found = None
    for u, p, level in LEVELS:
        ok = hmac.compare_digest(_h(user), _h(u)) & hmac.compare_digest(_h(pw), _h(p))
        if ok:
            found = level
    return found


# --------------------------------------------------------------------------- blocage des essais
_fails = {}
_lock = threading.Lock()


def locked_for(ip):
    with _lock:
        rec = _fails.get(ip)
        if rec and rec["until"] > time.time():
            return int(rec["until"] - time.time()) + 1
    return 0


def register_failure(ip):
    now = time.time()
    with _lock:
        if len(_fails) > 5000:                                   # purge
            for k in [k for k, v in _fails.items() if v["until"] < now and now - v["first"] > WINDOW]:
                _fails.pop(k, None)
        rec = _fails.get(ip)
        if not rec or now - rec["first"] > WINDOW:
            rec = _fails[ip] = {"n": 0, "first": now, "until": 0}
        rec["n"] += 1
        if rec["n"] >= MAX_FAILS:
            rec["until"] = now + LOCK
            rec["n"] = 0
            rec["first"] = now


def register_success(ip):
    with _lock:
        _fails.pop(ip, None)


# --------------------------------------------------------------------------- serveur
class Handler(BaseHTTPRequestHandler):
    server_version = "Elderwood"
    sys_version = ""
    timeout = 15                       # connexions lentes (slowloris) coupées
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, self.path.split("?")[0][:200]))   # jamais d'identifiants dans les logs

    def client_ip(self):
        if TRUST_PROXY:
            xff = self.headers.get("X-Forwarded-For", "")
            if xff:
                return xff.split(",")[-1].strip()[:64]       # entrée ajoutée par le proxy de Render (non falsifiable)
        return self.client_address[0]

    def secure_headers(self, cache="no-store"):
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=()")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")
        self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        self.send_header("Cache-Control", cache)

    def simple(self, code, text, extra=None):
        body = (text + "\n").encode("utf-8")
        self.send_response(code)
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.secure_headers()
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def deny(self, ip):
        register_failure(ip)
        time.sleep(1)                                   # freine les essais répétés
        self.simple(401, "Accès restreint : identifiant et mot de passe requis.",
                    {"WWW-Authenticate": 'Basic realm="Elderwood - acces restreint", charset="UTF-8"'})

    def respond(self):
        # HTTPS obligatoire : les identifiants ne doivent jamais circuler en clair
        if REQUIRE_HTTPS and self.headers.get("X-Forwarded-Proto", "https").lower() != "https":
            host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
            if host and re.fullmatch(r"[A-Za-z0-9.-]+", host):
                return self.simple(308, "HTTPS requis.", {"Location": "https://%s%s" % (host, urlsplit(self.path).path or "/")})
            return self.simple(403, "HTTPS requis.")
        ip = self.client_ip()
        wait = locked_for(ip)
        if wait:
            return self.simple(429, "Trop d'essais. Réessayez dans %d minute(s)." % (wait // 60 + 1), {"Retry-After": str(wait)})
        path = unquote(urlsplit(self.path).path)
        if path == "/deconnexion":                      # force le navigateur à oublier les identifiants
            return self.simple(401, "Déconnecté. Rechargez la page pour vous reconnecter.",
                               {"WWW-Authenticate": 'Basic realm="Elderwood - reconnexion", charset="UTF-8"'})
        level = authenticate(self.headers.get("Authorization"))
        if level is None:
            if not self.headers.get("Authorization"):
                time.sleep(0.05)
                return self.simple(401, "Accès restreint : identifiant et mot de passe requis.",
                                   {"WWW-Authenticate": 'Basic realm="Elderwood - acces restreint", charset="UTF-8"'})
            return self.deny(ip)
        register_success(ip)
        rel = path.lstrip("/") or "index.html"
        parts = [p for p in rel.split("/") if p]
        if not parts or ".." in parts or "\x00" in rel or parts[0] not in ALLOWED_TOP:
            return self.simple(404, "Introuvable.")
        name = "/".join(parts)
        if USE_VAULT:
            data = SITES[level].get(name)
            if data is None and name in ALLOWED_TOP and (name + "/index.html") in SITES[level]:
                name += "/index.html"; data = SITES[level][name]
            if data is None:
                return self.simple(404, "Introuvable.")
        else:                                           # développement local sans coffre : fichiers en clair
            root = ROOT if level == "staff" else ROOT / "dist" / "joueurs"
            target = (root / name).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                return self.simple(404, "Introuvable.")
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                return self.simple(404, "Introuvable.")
            data = target.read_bytes()
            name = target.name
        ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith(("text/", "application/javascript")) else ""))
        self.send_header("Content-Length", str(len(data)))
        self.secure_headers("private, max-age=300")      # contenu authentifié : cache du navigateur seulement, 5 min
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_GET(self):
        self.respond()

    def do_HEAD(self):
        self.respond()

    def _other(self):
        self.simple(405, "Méthode non autorisée.", {"Allow": "GET, HEAD"})
    do_POST = do_PUT = do_DELETE = do_PATCH = do_OPTIONS = _other


def check_config():
    if not LEVELS:
        sys.exit("SITE_STAFF_PASSWORD n'est pas défini : refus de démarrer un site sans mot de passe.")
    for user, pw, _root in LEVELS:
        bad = password_problems(pw, user)
        if bad:
            sys.exit("Mot de passe de « %s » trop faible : %s.\nGénérez-en un avec : python3 server.py --generate" % (user, " ; ".join(bad)))
    if len(LEVELS) == 2 and (LEVELS[0][1] == LEVELS[1][1] or LEVELS[0][0] == LEVELS[1][0]):
        sys.exit("Les deux niveaux doivent avoir des identifiants ET des mots de passe différents.")
    if USE_VAULT:
        load_vault()
    elif PLAYER_PW and not (ROOT / "dist" / "joueurs" / "index.html").exists():
        sys.exit("SITE_PLAYER_PASSWORD est défini mais dist/joueurs/ est absent : lancer `python3 build.py --all`.")


def main():
    if "--generate" in sys.argv:
        print(generate_password())
        return
    check_config()
    port = int(os.environ.get("PORT", "8000"))
    print("Elderwood protégé : %d niveau(x) d'accès, coffre chiffré : %s, HTTPS imposé : %s, port %d" % (len(LEVELS), USE_VAULT, REQUIRE_HTTPS, port), flush=True)
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    srv.daemon_threads = True
    srv.serve_forever()


if __name__ == "__main__":
    main()
