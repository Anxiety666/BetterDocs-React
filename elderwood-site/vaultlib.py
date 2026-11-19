"""Coffre chiffré : chiffrement authentifié de bout en bout, bibliothèque standard uniquement.

Construction (chiffrer puis authentifier) :
  clé      = scrypt(phrase secrète, sel aléatoire, n=2^15, r=8, p=1) -> 64 octets : 32 de chiffrement + 32 d'authentification
  flux     = HMAC-SHA256(clé_chiffrement, nonce || compteur)  (mode compteur, HMAC comme fonction pseudo-aléatoire)
  chiffré  = zlib(données) XOR flux
  étiquette= HMAC-SHA256(clé_authentification, en-tête || sel || nonce || chiffré), vérifiée AVANT tout déchiffrement
Un fichier modifié ou une mauvaise clé sont refusés ; sel et nonce sont neufs à chaque scellement.
"""
import hashlib, hmac, io, os, tarfile, zlib

MAGIC = b"ELDRVLT1"
SCRYPT = dict(n=2 ** 15, r=8, p=1, maxmem=96 * 1024 * 1024, dklen=64)


class VaultError(Exception):
    pass


def _keys(secret, salt):
    k = hashlib.scrypt(secret.encode("utf-8"), salt=salt, **SCRYPT)
    return k[:32], k[32:]


def _stream(key, nonce, n):
    out = bytearray()
    c = 0
    while len(out) < n:
        out += hmac.new(key, nonce + c.to_bytes(8, "big"), hashlib.sha256).digest()
        c += 1
    return bytes(out[:n])


def _xor(a, b):
    return (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).to_bytes(len(a), "big")


def seal(data, secret):
    comp = zlib.compress(data, 9)
    salt, nonce = os.urandom(16), os.urandom(16)
    ek, mk = _keys(secret, salt)
    ct = _xor(comp, _stream(ek, nonce, len(comp)))
    tag = hmac.new(mk, MAGIC + salt + nonce + ct, hashlib.sha256).digest()
    return MAGIC + salt + nonce + ct + tag


def unseal(blob, secret):
    if len(blob) < len(MAGIC) + 16 + 16 + 32 or not blob.startswith(MAGIC):
        raise VaultError("fichier de coffre invalide")
    salt, nonce = blob[8:24], blob[24:40]
    ct, tag = blob[40:-32], blob[-32:]
    ek, mk = _keys(secret, salt)
    if not hmac.compare_digest(hmac.new(mk, MAGIC + salt + nonce + ct, hashlib.sha256).digest(), tag):
        raise VaultError("clé incorrecte ou fichier altéré")
    return zlib.decompress(_xor(ct, _stream(ek, nonce, len(ct))))


def pack(files):
    """{chemin: octets} -> archive tar en mémoire."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as t:
        for name in sorted(files):
            ti = tarfile.TarInfo(name)
            ti.size = len(files[name])
            ti.mtime = 0
            t.addfile(ti, io.BytesIO(files[name]))
    return buf.getvalue()


def unpack(blob):
    """archive tar -> {chemin: octets} (chemins relatifs validés)."""
    out = {}
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r") as t:
        for m in t.getmembers():
            if not m.isfile() or m.name.startswith("/") or ".." in m.name.split("/"):
                raise VaultError("entrée suspecte dans le coffre : %r" % m.name)
            out[m.name] = t.extractfile(m).read()
    return out
