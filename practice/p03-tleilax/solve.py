"""p03 — C'est une oeuvre d'un grand maître Tleilax

Usage : python -I solve.py data/R_Cest_une_oeuvre_de_masheikhs.txt
1. Retire la « pigmentation » a..e (I.) : seuls les 'X' sont le dessin.
2. Inverse les permutations cycliques : on cherche par force brute le décalage
   de lignes (II/III) et de colonnes qui rend les X les plus « collés »
   (score = nombre de voisins X horizontaux et verticaux).
3. Lit les glyphes 4x5 et affiche le texte.
"""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # chemins relatifs au dossier du challenge
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data/R_Cest_une_oeuvre_de_masheikhs.txt"
G = open(path, encoding="utf-8").read().splitlines()
H, W = len(G), len(G[0])


def shift_rows(g, s):  # ligne i décalée cycliquement vers la droite de s*i
    return ["".join(r[(j - s * i) % W] for j in range(W)) for i, r in enumerate(g)]


def shift_cols(g, s):  # colonne j décalée cycliquement vers le bas de s*j
    return ["".join(g[(i - s * j) % H][j] for j in range(W)) for i in range(H)]


def score(g):
    P = {(i, j) for i in range(H) for j in range(W) if g[i][j] == "X"}
    return sum(((i + 1, j) in P) + ((i, j + 1) in P) for i, j in P)


cands = []
for a in range(-5, 6):
    for b in range(-5, 6):
        cands.append((score(shift_cols(shift_rows(G, a), b)), f"rows {a} puis cols {b}",
                      shift_cols(shift_rows(G, a), b)))
        cands.append((score(shift_rows(shift_cols(G, b), a)), f"cols {b} puis rows {a}",
                      shift_rows(shift_cols(G, b), a)))
cands.sort(key=lambda c: -c[0])
best_score, label, img = cands[0]
print(f"meilleur : {label} (score {best_score}), suivant : {cands[1][1]} ({cands[1][0]})",
      file=sys.stderr)

img = ["".join("#" if c == "X" else "." for c in r) for r in img]
rows_used = [i for i, r in enumerate(img) if "#" in r]
cols_used = [j for j in range(W) if any(img[i][j] == "#" for i in range(H))]
for r in img[rows_used[0]:rows_used[-1] + 1]:
    print(r[cols_used[0]:cols_used[-1] + 1], file=sys.stderr)

# Découpage en glyphes : colonnes vides = séparateurs
band = img[rows_used[0]:rows_used[-1] + 1]
glyphs, cur = [], []
for j in range(cols_used[0], cols_used[-1] + 2):
    col = "".join(r[j] if j < W else "." for r in band)
    if "#" in col:
        cur.append(col)
    elif cur:
        glyphs.append(tuple(cur))
        cur = []

FONT = {  # glyphe stocké colonne par colonne (haut -> bas)
    ("#...#", "#.#.#", "#.#.#", "#####"): "3",
    ("####.", "...#.", "..###", "...#."): "4",
    ("###.#", "#.#.#", "#.#.#", "#.###"): "5",
    ("#####", "#.#.#", "#.#.#", "#####"): "8",
    ("#####", "..#..", "..#..", "#####"): "H",
    ("#.###", "#.#.#", "#.#.#", "###.#"): "2",
    ("#####", "#.#.#", "#.#.#", ".#.#."): "B",
}
answer = "".join(FONT.get(g, "?") for g in glyphs)
open("answer.txt", "w", encoding="utf-8").write(answer + "\n")
print(answer)
