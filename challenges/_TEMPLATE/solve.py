"""Usage : python -I challenges/<dossier>/solve.py

Lit les fichiers de data/ et imprime la réponse finale, au format exact attendu.
"""
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def solve() -> str:
    # TODO
    return ""


if __name__ == "__main__":
    answer = solve()
    print(answer)
    (Path(__file__).resolve().parent / "answer.txt").write_text(answer + "\n", encoding="utf-8")
