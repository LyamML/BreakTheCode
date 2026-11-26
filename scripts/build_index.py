"""Génère challenges/INDEX.md et practice/INDEX.md (tableau de bord).

Sources, par dossier de challenge :
- ENONCE.md : titre, points, tags (écrits par fetch_ctfd.py)
- NOTES.md  : frontmatter YAML simple (owner, status, answer, confidence)

Usage : python3 scripts/build_index.py
Ne jamais éditer INDEX.md à la main ; en cas de conflit git dessus, relancer ce script.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS_ICON = {"todo": "⬜", "wip": "🟡", "solved": "🟢", "submitted": "✅", "failed": "🔴", "skipped": "⏭️"}


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def field(enonce: str, label: str) -> str:
    m = re.search(rf"\*\*{label}[^*]*\*\* : (.+)", enonce)
    return m.group(1).strip() if m else ""


def row(folder: Path) -> list[str]:
    enonce = (folder / "ENONCE.md").read_text(encoding="utf-8") if (folder / "ENONCE.md").exists() else ""
    notes = (folder / "NOTES.md").read_text(encoding="utf-8") if (folder / "NOTES.md").exists() else ""
    fm = frontmatter(notes)
    title = enonce.splitlines()[0].lstrip("# ").strip() if enonce else folder.name
    points = fm.get("points") or field(enonce, "Points").split(" ")[0]
    tags = fm.get("tags") or field(enonce, "Tags")
    status = fm.get("status", "todo")
    answer = fm.get("answer", "")
    if len(answer) > 40:
        answer = answer[:37] + "..."
    return [
        f"[{folder.name}]({folder.name}/)",
        title.replace("|", "/"),
        points,
        tags.replace("|", "/"),
        fm.get("owner", ""),
        f"{STATUS_ICON.get(status, '')} {status}",
        f"`{answer}`" if answer else "",
        fm.get("confidence", ""),
    ]


def build(section: str, heading: str) -> None:
    base = ROOT / section
    if not base.exists():
        return
    folders = sorted(p for p in base.iterdir() if p.is_dir() and re.match(r"[a-z]\d\d-", p.name))
    head = ["Dossier", "Challenge", "Pts", "Tags", "Qui", "Statut", "Réponse", "Confiance"]
    lines = [
        f"# {heading}",
        "",
        "<!-- Fichier généré par scripts/build_index.py : ne pas éditer à la main. -->",
        "",
        "| " + " | ".join(head) + " |",
        "|" + "---|" * len(head),
    ]
    lines += ["| " + " | ".join(row(f)) + " |" for f in folders]
    if not folders:
        lines.append("| _aucun challenge pour l'instant : `python3 scripts/fetch_ctfd.py <url>`_ |" + " |" * 7)
    (base / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{section}/INDEX.md : {len(folders)} challenge(s)")


if __name__ == "__main__":
    build("challenges", "Challenges du jour J")
    build("practice", "Entraînement (archive Break the Code)")
