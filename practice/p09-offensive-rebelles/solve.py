"""p09 — Les rebelles continuent leur offensive.

Chemin Xevora -> Crystar dans un DAG. Chaque trajet coûte du carburant : on consomme
des objets FUEL portés (somme des valeurs >= coût). Le poids porté (armes + carburants
pas encore consommés) ne doit jamais dépasser 100. Score = somme des valeurs des
WEAPON à l'arrivée. Le carburant 1 (valeur infinie, poids 0) paie le premier trajet.

Modèle ILP exact (scipy.optimize.milp / HiGHS, gap 0) :
  x_e      arête e empruntée
  y_i      arme i ramassée
  z_{i,e}  carburant i ramassé puis brûlé sur l'arête e (e part de la planète de i
           ou d'une planète atteignable depuis elle)
  poids à la planète v (après ramassage) = armes ramassées en amont de v
       + carburants ramassés en amont de v et brûlés sur une arête partant de v ou plus loin
Un carburant ramassé mais jamais brûlé n'apporte rien : on ne le modélise pas.

Usage : python -I solve.py [dossier_data]
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

SRC, DST, WMAX, START_FUEL = "Xevora", "Crystar", 100, "1"


def load(data: Path):
    edges = [(r[0], r[1], int(r[2])) for r in list(csv.reader(open(data / "Edges", encoding="utf-8")))[1:] if r]
    items = [(r[0], r[1], int(r[2]), int(r[3]), r[4].strip())
             for r in list(csv.reader(open(data / "Items", encoding="utf-8")))[1:] if r]
    return edges, items


def closure(adj, s):
    seen, st = {s}, [s]
    while st:
        for v in adj[st.pop()]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    return seen


def solve(data: Path):
    edges, items = load(data)
    succ, pred = defaultdict(list), defaultdict(list)
    for a, b, _ in edges:
        succ[a].append(b)
        pred[b].append(a)
    U = closure(succ, SRC) & closure(pred, DST)
    E = [e for e in edges if e[0] in U and e[1] in U]
    desc = {v: closure(succ, v) & U for v in U}  # v inclus
    anc = {v: closure(pred, v) & U for v in U}

    inner = U - {SRC, DST}  # pas de ramassage possible sur le départ ni l'arrivée
    weapons = [it for it in items if it[4] == "WEAPON" and it[1] in inner]
    fuels = [it for it in items if it[4] == "FUEL" and it[1] in inner]

    var = []  # descriptions des variables
    def new(desc_):
        var.append(desc_)
        return len(var) - 1

    xe = {k: new(("x", k)) for k in range(len(E))}
    yw = {w[0]: new(("y", w[0])) for w in weapons}
    zf = {}
    for f in fuels:
        for k, (a, b, c) in enumerate(E):
            if a != SRC and a in desc[f[1]]:
                zf[(f[0], k)] = new(("z", f[0], k))

    rows, lo, hi = [], [], []
    def add(c, l, h):
        rows.append(c); lo.append(l); hi.append(h)

    def on(v):  # expression "v est sur le chemin"
        return {} if v == SRC else {xe[k]: 1 for k, e in enumerate(E) if e[1] == v}

    for v in U:  # flot
        c = defaultdict(int)
        for k, (a, b, _) in enumerate(E):
            if a == v: c[xe[k]] += 1
            if b == v: c[xe[k]] -= 1
        rhs = 1 if v == SRC else -1 if v == DST else 0
        add(dict(c), rhs, rhs)
    for w in weapons:  # y_i <= on(planète)
        c = {yw[w[0]]: 1}
        for j, val in on(w[1]).items(): c[j] = -val
        add(c, -np.inf, 0)
    by_fuel = defaultdict(list)
    for (fid, k), j in zf.items():
        by_fuel[fid].append((k, j))
        add({j: 1, xe[k]: -1}, -np.inf, 0)  # z <= x_e
    for f in fuels:  # brûlé au plus une fois, et seulement si on passe sur sa planète
        if by_fuel[f[0]]:
            c = {j: 1 for _, j in by_fuel[f[0]]}
            for j, val in on(f[1]).items(): c[j] = c.get(j, 0) - val
            add(c, -np.inf, 0)
    fuel_val = {f[0]: f[2] for f in fuels}
    fuel_w = {f[0]: f[3] for f in fuels}
    fuel_planet = {f[0]: f[1] for f in fuels}
    for k, (a, b, cost) in enumerate(E):  # coût du trajet payé
        if a == SRC:
            continue  # payé par le carburant 1
        c = {j: fuel_val[fid] for (fid, kk), j in zf.items() if kk == k}
        c[xe[k]] = -cost
        add(c, 0, np.inf)
    for v in inner:  # poids à la planète v après ramassage, si v est sur le chemin
        c, big = {}, 0
        for w in weapons:
            if w[1] in anc[v]:
                c[yw[w[0]]] = w[3]; big += w[3]
        for (fid, k), j in zf.items():
            if fuel_planet[fid] in anc[v] and E[k][0] in desc[v]:
                c[j] = fuel_w[fid]; big += fuel_w[fid]
        M = max(0, big - WMAX)
        if not M:
            continue
        for j, val in on(v).items(): c[j] = c.get(j, 0) + M
        add(c, -np.inf, WMAX + M)

    n = len(var)
    A = lil_matrix((len(rows), n))
    for r, c in enumerate(rows):
        for j, val in c.items():
            A[r, j] = val
    obj = np.zeros(n)
    for w in weapons:
        obj[yw[w[0]]] = -w[2]
    res = milp(obj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(n),
               bounds=Bounds(0, 1), options={"mip_rel_gap": 0, "time_limit": 600})
    if res.x is None:
        raise SystemExit(f"pas de solution : {res.message}")
    sol = np.round(res.x).astype(int)

    nxt = {E[k][0]: E[k][1] for k in range(len(E)) if sol[xe[k]]}
    path = [SRC]
    while path[-1] != DST:
        path.append(nxt[path[-1]])
    used = defaultdict(list)   # (a,b) -> carburants brûlés
    picked = defaultdict(list)  # planète -> objets ramassés
    for (fid, k), j in zf.items():
        if sol[j]:
            used[E[k][:2]].append(fid)
            picked[fuel_planet[fid]].append(fid)
    for w in weapons:
        if sol[yw[w[0]]]:
            picked[w[1]].append(w[0])
    used[(SRC, path[1])] = [START_FUEL]
    return path, used, picked, round(-res.fun), res.message


def format_answer(path, used, picked):
    lines = ["next planet,fuel items to travel to next planet (separated by ;),items to pick on next planet(separated by ;)"]
    for a, b in zip(path, path[1:]):
        fuel = ";".join(sorted(used[(a, b)], key=int))
        if b == path[-1]:
            lines.append(f"{b},{fuel}")
        else:
            its = ";".join(sorted(picked[b], key=int)) or "N/A"
            lines.append(f"{b},{fuel},{its}")
    return "\n".join(lines)


if __name__ == "__main__":
    data = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "data"
    path, used, picked, score, msg = solve(data)
    print(format_answer(path, used, picked))
    print(f"# score={score} etapes={len(path) - 1} | {msg}", file=sys.stderr)
