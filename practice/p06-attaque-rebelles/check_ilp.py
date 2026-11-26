"""Contre-vérification p06 par ILP (scipy.optimize.milp = HiGHS), indépendante de la DP de solve.py.

Pas de dépendance hors scipy (PuLP >= 4 a cassé son API : éviter le jour J).
Usage : python -I check_ilp.py [dossier_data]
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

SRC, DST, WMAX = "Nebulor", "Xevora", 100

data = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "data"
edges = [tuple(r[:2]) for r in list(csv.reader(open(data / "Edges", encoding="utf-8")))[1:] if r]
weapons = [(r[0], r[1], int(r[2]), int(r[3])) for r in list(csv.reader(open(data / "Weapons", encoding="utf-8")))[1:] if r]
nodes = sorted({v for e in edges for v in e})

nE, nW = len(edges), len(weapons)
n = nE + nW  # variables : x_e (arête prise) puis y_i (arme prise)
rows, lo, hi = [], [], []


def add(coeffs, l, h):
    rows.append(coeffs)
    lo.append(l)
    hi.append(h)


for v in nodes:  # conservation de flot : un chemin SRC -> DST
    c = {}
    for k, (a, b) in enumerate(edges):
        if a == v:
            c[k] = c.get(k, 0) + 1
        if b == v:
            c[k] = c.get(k, 0) - 1
    rhs = 1 if v == SRC else -1 if v == DST else 0
    add(c, rhs, rhs)
for i, (_, planet, _, _) in enumerate(weapons):  # arme prise => on arrive sur sa planète
    c = {nE + i: 1}
    for k, (a, b) in enumerate(edges):
        if b == planet:
            c[k] = -1
    add(c, -np.inf, 0)
add({nE + i: w[3] for i, w in enumerate(weapons)}, -np.inf, WMAX)

A = lil_matrix((len(rows), n))
for r, c in enumerate(rows):
    for k, v in c.items():
        A[r, k] = v
cost = np.zeros(n)
cost[nE:] = [-w[2] for w in weapons]
res = milp(cost, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(n),
           bounds=Bounds(0, 1), options={"mip_rel_gap": 0})
print(res.message, "| score ILP =", round(-res.fun))
