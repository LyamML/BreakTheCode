"""Télécharge tous les challenges d'une instance CTFd dans challenges/.

Pour chaque challenge : challenges/cNN-<slug>/ENONCE.md + data/<fichiers>.
Ne réécrit jamais un ENONCE.md ou un fichier déjà présent (relançable sans risque
pendant l'event pour récupérer les nouveaux challenges).

Usage :
    python3 scripts/fetch_ctfd.py https://<instance-ctfd>
    python3 scripts/fetch_ctfd.py https://<instance-ctfd> --out practice --prefix p

Authentification (si l'API demande d'être connecté) — l'humain fournit l'une des deux
variables d'environnement, jamais l'agent :
    CTFD_TOKEN    jeton d'API CTFd (Paramètres du compte > Access Tokens)
    CTFD_SESSION  valeur du cookie `session` du navigateur connecté
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:  # macOS : le Python de python.org n'a pas toujours les certificats système
    import certifi

    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()


def slugify(name: str, max_words: int = 3) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", s.lower())
    stop = {"a", "c", "d", "l", "de", "la", "le", "les", "un", "une", "des", "du", "est", "quoi"}
    kept = [w for w in words if w not in stop] or words
    return "-".join(kept[:max_words]) or "challenge"


class Client:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.headers = {"User-Agent": "ctfd-fetch", "Content-Type": "application/json"}
        if tok := os.environ.get("CTFD_TOKEN"):
            self.headers["Authorization"] = f"Token {tok}"
        if sess := os.environ.get("CTFD_SESSION"):
            self.headers["Cookie"] = f"session={sess}"

    def get(self, path: str) -> bytes:
        url = path if path.startswith("http") else self.base + path
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:  # suit les redirections
                return r.read()
        except urllib.error.URLError as e:
            if isinstance(e.reason, ssl.SSLCertVerificationError):
                sys.exit(
                    "Erreur de certificat SSL. Sur macOS (Python python.org) : lancer "
                    "'/Applications/Python 3.x/Install Certificates.command', ou "
                    "'pip install certifi'. Ne pas désactiver la vérification sans l'humain."
                )
            raise

    def api(self, path: str):
        raw = self.get("/api/v1" + path)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            sys.exit("Réponse non JSON : probablement pas connecté. Fournir CTFD_TOKEN ou CTFD_SESSION.")
        if not payload.get("success"):
            sys.exit(f"Erreur API sur {path} : {payload}")
        return payload["data"]


def render(d: dict) -> str:
    tags = ", ".join(t["value"] if isinstance(t, dict) else str(t) for t in d.get("tags", []))
    meta = [
        f"- **id CTFd** : {d['id']}",
        f"- **Catégorie** : {d.get('category')}",
        f"- **Points actuels** : {d.get('value')} (type `{d.get('type')}`)",
        f"- **Tags (indices de technique/difficulté)** : {tags or 'aucun'}",
        f"- **Essais max** : {d.get('max_attempts') or 'illimité'}",
        f"- **Connexion** : {d.get('connection_info') or '-'}",
        f"- **Fichiers** : {', '.join(Path(f.split('?')[0]).name for f in d.get('files', [])) or 'aucun'}",
    ]
    hints = d.get("hints") or []
    if hints:
        meta.append(f"- **Indices** : {len(hints)} (peuvent coûter des points, ne pas débloquer sans l'humain)")
    return f"# {d['name']}\n\n" + "\n".join(meta) + "\n\n---\n\n" + (d.get("description") or "") + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("base_url")
    ap.add_argument("--out", default="challenges")
    ap.add_argument("--prefix", default="c")
    args = ap.parse_args()

    cli = Client(args.base_url)
    out = ROOT / args.out
    out.mkdir(exist_ok=True)
    summary = []
    listing = sorted(cli.api("/challenges"), key=lambda c: (c.get("value") or 0, c["id"]))
    for c in listing:
        d = cli.api(f"/challenges/{c['id']}")
        existing = [p for p in out.glob(f"{args.prefix}*-*") if (p / ".ctfd_id").exists()
                    and (p / ".ctfd_id").read_text().strip() == str(d["id"])]
        if existing:
            folder = existing[0]
        else:
            n = len([p for p in out.glob(f"{args.prefix}[0-9][0-9]-*")]) + 1
            folder = out / f"{args.prefix}{n:02d}-{slugify(d['name'])}"
            folder.mkdir()
            (folder / ".ctfd_id").write_text(str(d["id"]))
        enonce = folder / "ENONCE.md"
        if not enonce.exists():
            enonce.write_text(render(d), encoding="utf-8")
        data = folder / "data"
        data.mkdir(exist_ok=True)
        for f in d.get("files", []):
            target = data / Path(f.split("?")[0]).name
            if not target.exists():
                target.write_bytes(cli.get(f))
        tags = ", ".join(t["value"] if isinstance(t, dict) else str(t) for t in d.get("tags", []))
        summary.append((folder.name, d.get("value"), d.get("category"), tags, d["name"]))

    print(f"{'dossier':32} {'pts':>4}  catégorie  tags")
    for name, val, cat, tags, title in summary:
        print(f"{name:32} {val!s:>4}  {cat!s:10} {tags}  [{title}]")


if __name__ == "__main__":
    main()
