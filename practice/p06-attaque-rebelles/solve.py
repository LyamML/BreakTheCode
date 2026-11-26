"""p06 — L'attaque surprise des rebelles.

Chemin orienté Nebulor -> Xevora + sac à dos (poids max 100) sur les armes des
planètes traversées. Le graphe est un DAG (vérifié) : DP exacte sur
(planète, poids exact porté) en ordre topologique, knapsack 0/1 à chaque planète.

Usage : python -I solve.py [dossier_data]   -> imprime la réponse au format attendu
"""
import csv
import sys
from collections import defaultdict
from graphlib import TopologicalSorter
from pathlib import Path

SRC, DST, WMAX = "Nebulor", "Xevora", 100
NEG = float("-inf")


def load(data: Path):
    edges = [tuple(r[:2]) for r in list(csv.reader(open(data / "Edges", encoding="utf-8")))[1:] if r]
    items = defaultdict(list)  # planet -> [(id, value, weight)]
    for r in list(csv.reader(open(data / "Weapons", encoding="utf-8")))[1:]:
        if r:
            items[r[1]].append((r[0], int(r[2]), int(r[3])))
    return edges, items


def useful_nodes(edges, src, dst):
    succ, pred = defaultdict(list), defaultdict(list)
    for a, b in edges:
        succ[a].append(b)
        pred[b].append(a)

    def reach(s, adj):
        seen, st = {s}, [s]
        while st:
            for v in adj[st.pop()]:
                if v not in seen:
                    seen.add(v)
                    st.append(v)
        return seen

    keep = reach(src, succ) & reach(dst, pred)
    return keep, pred


def solve(data: Path):
    edges, items = load(data)
    keep, pred = useful_nodes(edges, SRC, DST)
    order = list(TopologicalSorter({v: [u for u in pred[v] if u in keep] for v in keep}).static_order())

    best = {}       # v -> list[WMAX+1] : meilleure valeur en partant de v avec poids exact w
    arrive_from = {}  # v -> list[WMAX+1] : prédécesseur choisi pour ce poids
    take = {}       # v -> table knapsack pour reconstruire les objets pris
    for v in order:
        if v == SRC:
            arr = [0] + [NEG] * WMAX
            frm = [None] * (WMAX + 1)
        else:
            arr, frm = [NEG] * (WMAX + 1), [None] * (WMAX + 1)
            for u in pred[v]:
                if u in best:
                    for w in range(WMAX + 1):
                        if best[u][w] > arr[w]:
                            arr[w], frm[w] = best[u][w], u
        arrive_from[v] = (arr, frm)
        # knapsack 0/1 sur les objets de v (pas d'objet ramassable sur SRC ni sur DST)
        its = items[v] if v not in (SRC, DST) else []
        layers = [arr]
        cur = arr
        for _id, val, wt in its:
            nxt = cur[:]
            for w in range(wt, WMAX + 1):
                if cur[w - wt] != NEG and cur[w - wt] + val > nxt[w]:
                    nxt[w] = cur[w - wt] + val
            layers.append(nxt)
            cur = nxt
        best[v] = cur
        take[v] = (its, layers)

    arr, _ = arrive_from[DST]
    w_end = max(range(WMAX + 1), key=lambda w: arr[w])
    score = arr[w_end]

    # reconstruction
    path, picks = [DST], {DST: []}
    v, w = DST, w_end
    while v != SRC:
        u = arrive_from[v][1][w]
        its, layers = take[u]
        chosen = []
        for k in range(len(its), 0, -1):
            if layers[k][w] != layers[k - 1][w]:
                chosen.append(its[k - 1][0])
                w -= its[k - 1][2]
        picks[u] = chosen[::-1]
        path.append(u)
        v = u
    path.reverse()
    return path, picks, score, w_end


def format_answer(path, picks):
    lines = ["next planet,weapons to pick on next planet(separated by ;)"]
    for p in path[1:-1]:
        lines.append(f"{p},{';'.join(picks[p]) if picks[p] else 'N/A'}")
    lines.append(path[-1])
    return "\n".join(lines)


if __name__ == "__main__":
    data = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "data"
    path, picks, score, w = solve(data)
    print(format_answer(path, picks))
    print(f"# score={score} poids={w} etapes={len(path) - 1}", file=sys.stderr)
