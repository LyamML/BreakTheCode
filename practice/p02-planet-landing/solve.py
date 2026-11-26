"""p02 — Planet Landing

Usage : python -I solve.py data/landings_btc_rennes.csv [G]
Affiche le point de conoissage au format `Latitude°N;Longitude°E`.

Modèle retenu (voir NOTES.md) :
  F = G * M * m / (R + h)^2   < 93500 N   (force au démarrage, d = R + h)
  a = v0^2 / (2 * h)          < 0.015     (décélération uniforme jusqu'à 0)
  t = 2 * h / v0              < 2000 s    (durée d'une décélération uniforme)
puis le t minimal.
"""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # chemins relatifs au dossier du challenge
import csv
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data/landings_btc_rennes.csv"
G_MAIN = float(sys.argv[2]) if len(sys.argv) > 2 else 6.674e-11

M = 5.97e24      # kg
m = 10 * 1000    # 10 tonnes -> kg
R = 6500 * 1000  # 6500 km -> m
F_MAX, A_MAX, T_MAX = 93500, 0.015, 2000


def signed(raw: str) -> str:
    """'63.08712° N' -> '63.08712' ; '124.251353° W' -> '-124.251353' (texte d'origine conservé)."""
    value, hemi = raw.replace("°", "").split()
    return value if hemi in ("N", "E") else "-" + value


def best(rows, G):
    ok = []
    for r in rows:
        h = float(r["shuttle_distance"])
        v = float(r["descent_speed"])
        F = G * M * m / (R + h) ** 2
        a = v * v / (2 * h)
        t = 2 * h / v
        if F < F_MAX and a < A_MAX and t < T_MAX:
            ok.append((t, r, F))
    ok.sort(key=lambda x: x[0])
    return ok


rows = list(csv.DictReader(open(path, encoding="utf-8")))

# Sensibilité à la valeur de G : le jeu de données est calé sur la limite de 93500 N
for G in (6.67e-11, 6.674e-11, 6.6743e-11):
    ok = best(rows, G)
    t, r, F = ok[0]
    print(f"G={G:<10} {len(ok)} points valides -> {signed(r['latitude'])}°N;"
          f"{signed(r['longitude'])}°E (t={t:.2f}s, F={F:.1f}N)", file=sys.stderr)

t, r, F = best(rows, G_MAIN)[0]
answer = f"{signed(r['latitude'])}°N;{signed(r['longitude'])}°E"
open("answer.txt", "w", encoding="utf-8").write(answer + "\n")
print(answer)
