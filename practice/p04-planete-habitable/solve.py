"""p04 — A la recherche d'une nouvelle planète habitable.

Plus court chemin Terre -> Cerosarae dans planets_graph.json en respectant le
message décodé de p05 :
  - éviter absolument Vegaelus et Zoraorara (champ d'astéroïdes)
  - passer par Phosunion PUIS Neptanos (trou noir)
  - Taraisis : optionnel ("vous pouvez"), donc non imposé.

Usage : python -I solve.py [chemin/vers/planets_graph.json] [--details]
"""
import heapq
import json
import sys
from pathlib import Path

START = "Terre"
TARGET = "Cerosarae"
AVOID = {"Vegaelus", "Zoraorara"}
WAYPOINTS = ["Phosunion", "Neptanos"]


def dijkstra(g, src, dst, banned):
    dist = {src: 0}
    prev = {}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            break
        if d > dist[u]:
            continue
        for v, w in g[u].items():
            if v in banned:
                continue
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dst not in dist:
        return float("inf"), None
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    return dist[dst], path[::-1]


def route(g, stops, avoid):
    total, full = 0, [stops[0]]
    for a, b in zip(stops, stops[1:]):
        d, p = dijkstra(g, a, b, avoid)
        if p is None:
            return float("inf"), None
        total += d
        full += p[1:]
    return total, full


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = Path(args[0]) if args else Path(__file__).parent / "data" / "planets_graph.json"
    g = json.loads(path.read_text(encoding="utf-8"))

    stops = [START, *WAYPOINTS, TARGET]
    cost, best = route(g, stops, AVOID)
    answer = ",".join(best)
    print(answer)
    (Path(__file__).parent / "answer.txt").write_text(answer + "\n", encoding="utf-8")

    if "--details" in sys.argv:
        print(f"\ncoût={cost}  étapes={len(best)}  planètes répétées={len(best) - len(set(best))}")
        print("contient une planète interdite :", bool(AVOID & set(best)))
        variants = {
            "sans contrainte": ([START, TARGET], set()),
            "évitement seul": ([START, TARGET], AVOID),
            "waypoints sans évitement": (stops, set()),
            "ordre inversé Neptanos->Phosunion": ([START, "Neptanos", "Phosunion", TARGET], AVOID),
            "+ Taraisis avant Phosunion": ([START, "Taraisis", *WAYPOINTS, TARGET], AVOID),
            "+ Taraisis entre Phosunion et Neptanos": ([START, "Phosunion", "Taraisis", "Neptanos", TARGET], AVOID),
            "+ Taraisis après Neptanos": ([START, *WAYPOINTS, "Taraisis", TARGET], AVOID),
        }
        for name, (s, av) in variants.items():
            c, p = route(g, s, av)
            print(f"- {name}: coût={c} -> {','.join(p)}")


if __name__ == "__main__":
    main()
