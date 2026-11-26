"""p08 — Sauts de Constellations.

Usage : python -I solve.py data/dataset.txt          -> imprime la réponse
        python -I solve.py data/dataset.txt --render -> régénère les PNG de chaque étape

L'identification de l'étoile visée par chaque instruction a été faite visuellement
sur les rendus de `sky.py` (voir NOTES.md). Le script encode ces choix, puis vérifie
automatiquement qu'ils sont cohérents avec le dataset :
  - l'étoile choisie appartient bien à la constellation citée (sauf étape 4, voir NOTES),
  - les segments qui justifient le choix existent,
  - l'étoile est visible (<= 1000 al) depuis la position courante.
"""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # chemins relatifs au dossier du challenge
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sky import parse, render_all_sky, render_constellation  # noqa: E402

MAX_DIST = 1000.0

# (constellation, étoile choisie, segments qui justifient le choix)
STEPS = [
    # 1. « entre les deux yeux de Marvin » : yeux = triangles 517-534-489 et 563-608-326,
    #    reliés par le pont 534-285-563 ; 285 est aussi l'étoile la plus proche du milieu
    #    des centres des deux yeux en projection.
    ("Marvin", 285, [(285, 534), (285, 563), (489, 517), (489, 534), (517, 534),
                     (326, 563), (326, 608), (563, 608)]),
    # 2. « liaison entre l'oeil du Dalek et sa tige » : oeil = triangle 352-374-515 au bout
    #    de la tige 515-593 qui part du dôme (593-115-599-30-151).
    ("Dalek", 515, [(352, 515), (374, 515), (352, 374), (515, 593)]),
    # 3. « pointe de l'Epée de Damoclès » : sommet de la lame 493 (582-493, 47-493) ;
    #    le pommeau en losange est 34-471-507 à l'autre bout.
    ("Epee de Damocles", 493, [(493, 582), (47, 493)]),
    # 4. « l'oeil du dino » : le dinosaure n'a pas d'oeil dans sa liste. L'étoile 108 est
    #    la SEULE étoile du dataset qui n'appartient à aucune constellation, et elle se
    #    projette exactement au milieu de la tête -> c'est l'oeil « perdu ».
    ("Dinosaure", 108, []),
]


def check(stars, consts):
    by_name = {c["name"]: c for c in consts}
    pos = np.zeros(3)
    for name, star, edges in STEPS:
        c = by_name[name]
        es = {tuple(sorted(e)) for e in c["edges"]}
        for e in edges:
            assert tuple(sorted(e)) in es, (name, e)
        if name != "Dinosaure":
            assert star in c["ids"], (name, star)
        d = np.linalg.norm(stars[star - 1] - pos)
        assert d <= MAX_DIST, (name, star, d)
        vis = (np.linalg.norm(stars[np.array(c["ids"]) - 1] - pos, axis=1) <= MAX_DIST).sum()
        assert vis >= len(c["ids"]) - 1, (name, "constellation pas visible", vis)
        pos = stars[star - 1]
    in_any = set().union(*(set(c["ids"]) for c in consts))
    free = sorted(set(range(1, len(stars) + 1)) - in_any)
    assert free == [108], free


def main():
    ds = sys.argv[1] if len(sys.argv) > 1 else "data/dataset.txt"
    instr, stars, consts = parse(ds)
    assert len(instr) == len(STEPS)
    check(stars, consts)
    if "--render" in sys.argv:
        out = Path(__file__).resolve().parent / "renders"
        pos = np.zeros(3)
        for i, (name, star, _) in enumerate(STEPS, 1):
            d = out / f"step{i}"
            d.mkdir(parents=True, exist_ok=True)
            render_all_sky(stars, pos, consts, d / "all_sky.png", MAX_DIST)
            c = next(c for c in consts if c["name"] == name)
            render_constellation(stars, pos, c, d / f"{name.replace(' ', '_')}.png", MAX_DIST)
            pos = stars[star - 1]
    ans = " ".join(str(s) for _, s, _ in STEPS)
    print(ans)
    (Path(__file__).resolve().parent / "answer.txt").write_text(ans + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
