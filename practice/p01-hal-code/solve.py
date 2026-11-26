"""p01 — Hal, c'est quoi le code ?

Usage : python -I solve.py data/rahaha_le_code_est_la.txt
Affiche le code de 3 lettres qui apparaît le plus souvent.
"""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # chemins relatifs au dossier du challenge
import re
import sys
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "data/rahaha_le_code_est_la.txt"
s = open(path, encoding="utf-8").read().strip()

# Fenêtre glissante = comptage AVEC chevauchements
counts = Counter(s[i:i + 3] for i in range(len(s) - 2))
top = counts.most_common(5)
best, n = top[0]

# Contrôles : égalité en tête ? même résultat sans chevauchement ?
ties = [w for w, c in counts.items() if c == n]
non_overlap = len(re.findall(re.escape(best), s))
print(f"top5 (avec chevauchement) : {top}", file=sys.stderr)
print(f"égalités en tête : {ties} ; '{best}' sans chevauchement = {non_overlap}", file=sys.stderr)

open("answer.txt", "w", encoding="utf-8").write(best + "\n")
print(best)
