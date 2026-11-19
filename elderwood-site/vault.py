#!/usr/bin/env python3
"""Gère le coffre chiffré (vault/*.bin) : seul contenu sensible versionné dans le dépôt.

    export SITE_VAULT_KEY='…'            # phrase secrète, 24 caractères minimum (python3 vault.py generate)
    python3 vault.py seal                # build complet puis chiffrement -> vault/staff.bin, joueurs.bin, sources.bin
    python3 vault.py open                # déchiffre sources.bin -> content/, pages.json, config/ (poste du mainteneur)
    python3 vault.py verify              # contrôle que les 3 coffres s'ouvrent avec la clé
    python3 vault.py rekey NOUVELLE_CLE  # rechiffre les 3 coffres avec une nouvelle clé (ancienne clé dans SITE_VAULT_KEY)

staff.bin    = site complet (index.html, assets/, data/)         servi au niveau « staff »
joueurs.bin  = site sans pages staff (dist/joueurs)               servi au niveau « joueurs »
sources.bin  = sources éditables (content/, pages.json, config/)  pour reconstruire le site
"""
import os, secrets, string, subprocess, sys
from pathlib import Path

import vaultlib

ROOT = Path(__file__).resolve().parent
VAULT = ROOT / "vault"


def key():
    k = os.environ.get("SITE_VAULT_KEY", "")
    if len(k) < 24:
        sys.exit("SITE_VAULT_KEY (24 caractères minimum) est requis. Génération : python3 vault.py generate")
    return k


def collect(base, tops):
    files = {}
    for top in tops:
        p = base / top
        if p.is_file():
            files[top] = p.read_bytes()
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    files[f.relative_to(base).as_posix()] = f.read_bytes()
    return files


def seal():
    k = key()
    subprocess.run([sys.executable, str(ROOT / "build.py"), "--all", "--check"], check=True, cwd=ROOT)
    VAULT.mkdir(exist_ok=True)
    jobs = [
        ("staff.bin", collect(ROOT, ["index.html", "assets", "data"])),
        ("joueurs.bin", collect(ROOT / "dist" / "joueurs", ["index.html", "assets", "data"])),
        ("sources.bin", collect(ROOT, ["content", "pages.json", "config"])),
    ]
    for name, files in jobs:
        blob = vaultlib.seal(vaultlib.pack(files), k)
        (VAULT / name).write_bytes(blob)
        print("%-12s %4d fichiers -> %6.2f Mo chiffrés" % (name, len(files), len(blob) / 1e6))


def read(name, k):
    try:
        return vaultlib.unpack(vaultlib.unseal((VAULT / name).read_bytes(), k))
    except vaultlib.VaultError as e:
        sys.exit("%s : %s" % (name, e))


def open_sources():
    for rel, data in read("sources.bin", key()).items():
        f = ROOT / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
    print("Sources restaurées. Étapes suivantes : modifier, puis `python3 vault.py seal`.")


def verify():
    k = key()
    for name in ("staff.bin", "joueurs.bin", "sources.bin"):
        print("%-12s OK (%d fichiers)" % (name, len(read(name, k))))


def rekey(new):
    if len(new) < 24:
        sys.exit("La nouvelle clé doit faire 24 caractères minimum.")
    old = key()
    for name in ("staff.bin", "joueurs.bin", "sources.bin"):
        data = vaultlib.pack(read(name, old))
        (VAULT / name).write_bytes(vaultlib.seal(data, new))
        print(name, "rechiffré")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "generate":
        print("".join(secrets.choice(string.ascii_letters + string.digits + "-_.!#%+=") for _ in range(40)))
    elif cmd == "seal":
        seal()
    elif cmd == "open":
        open_sources()
    elif cmd == "verify":
        verify()
    elif cmd == "rekey" and len(sys.argv) > 2:
        rekey(sys.argv[2])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
