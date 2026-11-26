"""Contre-vérification p09 par une méthode exacte indépendante de l'ILP.

DP en ordre topologique sur le DAG. État en arrivant sur une planète :
  (multiset des carburants portés (valeur, poids), poids des armes) -> meilleure valeur.
Front de Pareto par multiset : (poids armes plus faible, valeur plus haute) domine.
Sur chaque trajet on ne brûle que des sous-ensembles MINIMAUX couvrant le coût
(brûler en plus = ne pas avoir ramassé ce carburant, état déjà exploré et plus léger).

Usage : python -I check_dp.py [dossier_data]   (donne le score optimal seul)
"""
import csv
import sys
from collections import defaultdict
from graphlib import TopologicalSorter
from itertools import combinations
from pathlib import Path

SRC, DST, WMAX = "Xevora", "Crystar", 100

data = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "data"
E = [(r[0], r[1], int(r[2])) for r in list(csv.reader(open(data / "Edges", encoding="utf-8")))[1:] if r]
items = defaultdict(list)
for r in list(csv.reader(open(data / "Items", encoding="utf-8")))[1:]:
    if r:
        items[r[1]].append((int(r[2]), int(r[3]), r[4].strip()))
succ, pred = defaultdict(list), defaultdict(list)
for a, b, c in E:
    succ[a].append((b, c))
    pred[b].append(a)


def reach(s, adj):
    seen, st = {s}, [s]
    while st:
        for v in adj[st.pop()]:
            v = v[0] if isinstance(v, tuple) else v
            if v not in seen:
                seen.add(v)
                st.append(v)
    return seen


U = reach(SRC, succ) & reach(DST, pred)
order = list(TopologicalSorter({v: [u for u in pred[v] if u in U] for v in U}).static_order())
states = defaultdict(dict)  # planète -> {fuels(tuple trié): [(W, V), ...] Pareto}


def push(v, fuels, W, V):
    front = states[v].setdefault(fuels, [])
    for w2, v2 in front:
        if w2 <= W and v2 >= V:
            return
    front[:] = [(w2, v2) for w2, v2 in front if not (W <= w2 and V >= v2)] + [(W, V)]


def minimal_burns(fuels, cost):
    n = len(fuels)
    found = []
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            s = set(idx)
            if sum(fuels[i][0] for i in idx) >= cost and not any(f <= s for f in found):
                found.append(s)
    seen = set()
    for s in found:
        rest = tuple(sorted(fuels[i] for i in range(n) if i not in s))
        if rest not in seen:
            seen.add(rest)
            yield rest


best = None
for v in order:
    if v == SRC:
        cur = {(): [(0, 0)]}
    else:
        cur = states.pop(v, {})
    if v == DST:
        best = max((V for fr in cur.values() for _, V in fr), default=None)
        continue
    # ramassage sur v
    after = defaultdict(list)
    its = items[v] if v != SRC else []
    for fuels, front in cur.items():
        for W, V in front:
            base = sum(f[1] for f in fuels) + W
            # énumération des sous-ensembles d'objets (<= 10 objets par planète)
            for mask in range(1 << len(its)):
                add_w, add_v, nf = 0, 0, list(fuels)
                tot = base
                for i, (val, wt, typ) in enumerate(its):
                    if mask >> i & 1:
                        tot += wt
                        if typ == "WEAPON":
                            add_w += wt
                            add_v += val
                        else:
                            nf.append((val, wt))
                if tot <= WMAX:
                    after[tuple(sorted(nf))].append((W + add_w, V + add_v))
    # trajets
    for u, cost in succ[v]:
        if u not in U:
            continue
        for fuels, front in after.items():
            if v == SRC:
                rests = [fuels]  # carburant 1
            else:
                rests = list(minimal_burns(list(fuels), cost))
            for rest in rests:
                for W, V in front:
                    push(u, rest, W, V)

print("score optimal (DP exacte) =", best)
