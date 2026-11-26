"""c26 - L'artefact mysterieux, premier message.

Decodage en couches de la grille 10x10 de ENONCE.md, puis recherche du message
horizontalement / verticalement dans la grille finale.
"""
import ast
from pathlib import Path

HERE = Path(__file__).parent


def load_grid():
    text = (HERE / "ENONCE.md").read_text(encoding="utf-8")
    return [ast.literal_eval(l) for l in text.splitlines() if l.startswith("['")]


def layer(cell):
    # '--' separe les groupes, '-' separe les codes ASCII decimaux d'un groupe
    return "".join("".join(chr(int(x)) for x in g.split("-")) for g in cell.split("--"))


def decode_cell(cell):
    l1 = layer(cell)  # '53-53--53-53' -> '5555'
    l2 = "".join(chr(int(l1[i:i + 2])) for i in range(0, len(l1), 2))  # '5555' -> '77'
    return chr(int(l2))  # '77' -> 'M'


def main():
    raw = load_grid()
    assert len(raw) == 10 and all(len(r) == 10 for r in raw)
    G = [[decode_cell(c) for c in r] for r in raw]
    print("Grille decodee :")
    for r in G:
        print("  " + " ".join(r))
    rows = ["".join(r) for r in G]
    cols = ["".join(G[r][c] for r in range(10)) for c in range(10)]
    print("Colonnes :")
    for i, c in enumerate(cols):
        print(f"  C{i}: {c}")
    # Seule suite de lettres formant un mot : colonne 5 (0-indexee), lignes 1 a 8.
    col5 = cols[5]
    letters = col5[1:9]
    assert letters.isalpha()
    target = letters.upper()
    print("Message vertical colonne 5, lignes 1-8 :", target)
    (HERE / "answer.txt").write_text(target + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
