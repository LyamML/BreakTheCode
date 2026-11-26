"""Validateur indépendant p06 : vérifie une réponse et calcule son score.

Usage : python -I validate.py <fichier_reponse> [dossier_data]
"""
import csv
import sys
from pathlib import Path

SRC, DST, WMAX = "Nebulor", "Xevora", 100


def validate(answer_text: str, data: Path):
    edges = {tuple(r[:2]) for r in list(csv.reader(open(data / "Edges", encoding="utf-8")))[1:] if r}
    weapons = {r[0]: (r[1], int(r[2]), int(r[3]))
               for r in list(csv.reader(open(data / "Weapons", encoding="utf-8")))[1:] if r}
    lines = [l.strip() for l in answer_text.strip().splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("next planet"):
        lines = lines[1:]
    errors, here, taken, weight, score = [], SRC, set(), 0, 0
    for n, line in enumerate(lines, 1):
        parts = line.split(",", 1)
        planet = parts[0].strip()
        ids = [] if len(parts) == 1 or parts[1].strip() == "N/A" else [x.strip() for x in parts[1].split(";")]
        if (here, planet) not in edges:
            errors.append(f"ligne {n}: pas d'arête {here} -> {planet}")
        if planet == DST and n != len(lines):
            errors.append(f"ligne {n}: {DST} atteint avant la fin")
        for i in ids:
            if i not in weapons:
                errors.append(f"ligne {n}: arme {i} inconnue")
            elif weapons[i][0] != planet:
                errors.append(f"ligne {n}: arme {i} est sur {weapons[i][0]}, pas {planet}")
            elif i in taken:
                errors.append(f"ligne {n}: arme {i} déjà prise")
            else:
                taken.add(i)
                weight += weapons[i][2]
                score += weapons[i][1]
        if weight > WMAX:
            errors.append(f"ligne {n}: poids {weight} > {WMAX}")
        here = planet
    if here != DST:
        errors.append(f"arrivée sur {here}, pas {DST}")
    return errors, score, weight


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    ans = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "answer.txt"
    data = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "data"
    errors, score, weight = validate(ans.read_text(encoding="utf-8"), data)
    print("VALIDE" if not errors else "INVALIDE", f"score={score} poids={weight}")
    for e in errors:
        print("  -", e)
    sys.exit(1 if errors else 0)
