"""Validateur indépendant p09 : simule le voyage, vérifie chaque règle, calcule le score.

Usage : python -I validate.py <fichier_reponse> [dossier_data]
"""
import csv
import sys
from pathlib import Path

SRC, DST, WMAX = "Xevora", "Crystar", 100


def validate(answer_text: str, data: Path):
    cost = {(r[0], r[1]): int(r[2]) for r in list(csv.reader(open(data / "Edges", encoding="utf-8")))[1:] if r}
    items = {r[0]: (r[1], int(r[2]), int(r[3]), r[4].strip())
             for r in list(csv.reader(open(data / "Items", encoding="utf-8")))[1:] if r}
    lines = [l.strip() for l in answer_text.strip().splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("next planet"):
        lines = lines[1:]
    inv = {"1": (SRC, float("inf"), 0, "FUEL")}  # carburant de départ
    errors, here, ever = [], SRC, set()
    ids = lambda s: [] if s.strip() in ("", "N/A") else [x.strip() for x in s.split(";")]
    for n, line in enumerate(lines, 1):
        parts = line.split(",")
        planet = parts[0].strip()
        fuel = ids(parts[1]) if len(parts) > 1 else []
        pick = ids(parts[2]) if len(parts) > 2 else []
        if len(parts) > 3:
            errors.append(f"ligne {n}: trop de champs")
        if (here, planet) not in cost:
            errors.append(f"ligne {n}: pas d'arête {here} -> {planet}")
        paid = 0
        for f in fuel:
            if f not in inv:
                errors.append(f"ligne {n}: carburant {f} pas dans l'inventaire")
            elif inv[f][3] != "FUEL":
                errors.append(f"ligne {n}: objet {f} n'est pas un carburant")
            else:
                paid += inv.pop(f)[1]
        if paid < cost.get((here, planet), 0):
            errors.append(f"ligne {n}: carburant {paid} < coût {cost.get((here, planet))}")
        here = planet
        if planet == DST and n != len(lines):
            errors.append(f"ligne {n}: {DST} atteint avant la fin")
        for i in pick:
            if i not in items:
                errors.append(f"ligne {n}: objet {i} inconnu")
            elif items[i][0] != planet:
                errors.append(f"ligne {n}: objet {i} est sur {items[i][0]}, pas {planet}")
            elif i in ever:
                errors.append(f"ligne {n}: objet {i} déjà ramassé")
            else:
                ever.add(i)
                inv[i] = items[i]
        weight = sum(v[2] for v in inv.values())
        if weight > WMAX:
            errors.append(f"ligne {n} ({planet}): poids {weight} > {WMAX}")
    if here != DST:
        errors.append(f"arrivée sur {here}, pas {DST}")
    score = sum(v[1] for v in inv.values() if v[3] == "WEAPON")
    return errors, score, sum(v[2] for v in inv.values())


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    ans = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "answer.txt"
    data = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "data"
    errors, score, weight = validate(ans.read_text(encoding="utf-8"), data)
    print("VALIDE" if not errors else "INVALIDE", f"score={score} poids_final={weight}")
    for e in errors:
        print("  -", e)
    sys.exit(1 if errors else 0)
