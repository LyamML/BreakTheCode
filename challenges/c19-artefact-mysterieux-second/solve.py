"""c19 - L'artefact mysterieux, second message.
Grille 10x10 recopiee de ENONCE.md (pas de fichier data/).
Methode : decalage de Cesar sur les 95 ASCII imprimables (32..126), toutes les
valeurs de decalage, sur chaque ligne et colonne (endroit et miroir). On garde les
lectures qui contiennent 8 majuscules consecutives ou plus.
"""
import ast
import re
from pathlib import Path

HERE = Path(__file__).parent
txt = (HERE / "ENONCE.md").read_text(encoding="utf-8")
block = re.search(r"```txt\n(.*?)```", txt, re.S).group(1)
G = [ast.literal_eval(l) for l in block.strip().splitlines()]
assert len(G) == 10 and all(len(r) == 10 for r in G)


def shift(s, k):
    return "".join(chr((ord(c) - 32 + k) % 95 + 32) for c in s)


lines = {}
for i in range(10):
    lines[f"ligne {i}"] = "".join(G[i])
    lines[f"colonne {i}"] = "".join(G[r][i] for r in range(10))
for k in list(lines):
    lines[k + " miroir"] = lines[k][::-1]

for name, s in lines.items():
    for k in range(95):
        t = shift(s, k)
        m = re.search(r"[A-Z]{8,}", t)
        if m:
            print(f"{name:20s} decalage {k - 95 if k > 47 else k:+3d} : {t}")

print("\nGrille entiere decalee de -8 :")
for r in G:
    print("  " + shift("".join(r), -8))

row7 = shift("".join(G[7]), -8)
assert row7 == "NANNAPOLIS"
answer = "ANNAPOLIS"  # 1er caractere = bruit, comme K...F autour de GLOOSCAP (c26)
print("\nligne 7 decalee de -8 :", row7)
print("Flag :", answer)
(HERE / "answer.txt").write_text(answer + "\n", encoding="utf-8")
