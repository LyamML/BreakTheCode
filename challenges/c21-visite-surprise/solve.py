"""c21 Visite surprise : BFS sur (case, temps, masque de checkpoints).

Carte : grille 8x8, lignes A (sud) .. H (nord), colonnes 0 (ouest) .. 7 (est),
un lieu par case (transcrit a la main depuis data/carte.png, verifie au zoom).
Lancer : python3 -I solve.py
"""
from collections import deque
from itertools import product
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"

ROWS = "ABCDEFGH"
GRID = {
    "H": ["Fort Mason", "Fort Lowell", "Dragoon Springs", "Council Rocks",
          "Cochise Stronghold", "Fort Bowie", "San Simon", "El Paso"],
    "G": ["Safford", "San Pedro River Station", "Tubac", "Dragoon Mountains",
          "Apache Pass", "Hachita", "Silver City", "San Elizario (north)"],
    "F": ["Fort Apache", "Camp Crittenden", "Pinos Altos", "Naco",
          "Fairbank", "Fort Cummings", "Lordsburg", "Fort Bliss"],
    "E": ["Camp Grant (old site)", "Santa Rita del Cobre", "Animas", "Fort Grant",
          "Mimbres", "Fort Selden", "Deming", "Mesilla"],
    "D": ["Casas Grandes", "Ascensión", "Janos", "Fort Quitman",
          "Guadalupe Pass", "Las Cruces", "Lincoln", "Socorro"],
    "C": ["Buenaventura", "Santa Isabel", "Ojinaga", "Chihuahua",
          "San Elizario", "Fort Davis", "Pecos River Crossing", "Fort Stockton (St. Gall)"],
    "B": ["Galeana", "Cuauhtémoc", "Aldama", "Camargo",
          "Fort Lancaster", "Comanche Springs", "Van Horn Wells", "Horsehead Crossing"],
    "A": ["Jiménez", "Santa Bárbara", "Rosales", "Meoqui",
          "Santa Agustín Springs", "Sanderson", "Presidio", "Boquillas"],
}
POS = {}
for r, names in GRID.items():
    for c, n in enumerate(names):
        POS[n] = (ROWS.index(r), c)
# alias utilises dans les fichiers
POS["Camp Grant"] = POS["Camp Grant (old site)"]

START, GOAL = POS["Jiménez"], POS["El Paso"]
BANDIT_ROW = POS["Camp Grant (old site)"][0]
BANDIT_C0, BANDIT_C1 = POS["Camp Grant (old site)"][1], POS["Mesilla"][1]
PERIODS = (1, 3, 5)


def load():
    cps = [l.split(",")[0].strip() for l in (DATA / "checkpoints_voyage.txt").read_text("utf-8").splitlines() if l.strip()]
    evs = []
    for l in (DATA / "evenements_voyage.txt").read_text("utf-8").splitlines():
        if not l.strip() or l.startswith("#"):
            continue
        a, b, _typ, j, k = [x.strip() for x in l.split(",")]
        pa, pb = POS[a], POS[b]
        assert abs(pa[0] - pb[0]) + abs(pa[1] - pb[1]) == 1, (a, b)
        evs.append((pa, pb, int(j), int(k)))
    return [POS[c] for c in cps], evs


def bandit_col(t, p, bounce=True, offset=0):
    """Colonne du groupe de periode p apres t jours ecoules."""
    m = max(0, (t + offset) // p)
    L = BANDIT_C1 - BANDIT_C0  # 7 pas Camp Grant -> Mesilla
    if not bounce and m >= 2 * L:
        return BANDIT_C0
    m %= 2 * L
    return BANDIT_C0 + (m if m <= L else 2 * L - m)


def solve(wait=False, event_mode="zones", bounce=True, offset=0, ev_end="excl", tmax=400):
    cps, evs = load()
    cpidx = {p: i for i, p in enumerate(cps)}
    full = (1 << len(cps)) - 1

    def active(j, k, t):
        return j <= t < j + k if ev_end == "excl" else j <= t <= j + k

    def bandit_cells(t):
        return {(BANDIT_ROW, bandit_col(t, p, bounce, offset)) for p in PERIODS}

    def blocked_zone(cell, t):  # zone impraticable a l'instant t
        if cell in bandit_cells(t):
            return True
        if event_mode == "zones":
            return any(active(j, k, t) and cell in (a, b) for a, b, j, k in evs)
        if event_mode == "zoneB":
            return any(active(j, k, t) and cell == b for a, b, j, k in evs)
        return False

    def edge_blocked(u, v, t):
        if event_mode != "edge":
            return False
        return any((active(j, k, t) or active(j, k, t + 1)) and {u, v} == {a, b} for a, b, j, k in evs)

    m0 = 1 << cpidx[START] if START in cpidx else 0
    start = (START, m0)
    seen = {(START, m0, 0)}
    q = deque([(START, m0, 0, None)])
    parent = {}
    while q:
        u, m, t, _ = q.popleft()
        if u == GOAL and m == full:
            path = [(u, m, t)]
            while (path[-1]) in parent:
                path.append(parent[path[-1]])
            return t, path[::-1]
        if t >= tmax:
            continue
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] + ([(0, 0)] if wait else [])
        for dr, dc in moves:
            v = (u[0] + dr, u[1] + dc)
            if not (0 <= v[0] < 8 and 0 <= v[1] < 8):
                continue
            if blocked_zone(v, t) or blocked_zone(v, t + 1):
                continue
            if v != u and edge_blocked(u, v, t):
                continue
            nm = m | (1 << cpidx[v]) if v in cpidx else m
            # on ne peut rejoindre El Paso qu'apres tous les lieux : arriver plus tot ne compte pas
            st = (v, nm, t + 1)
            if st in seen:
                continue
            seen.add(st)
            parent[st] = (u, m, t)
            q.append((v, nm, t + 1, None))
    return 0, None


def name(p):
    return GRID[ROWS[p[0]]][p[1]]


if __name__ == "__main__":
    print("variantes :")
    for wait, mode, bounce, off, ee in product([False, True], ["edge", "zones", "zoneB", "none"], [True, False], [0, 1], ["excl", "incl"]):
        d, _ = solve(wait, mode, bounce, off, ee)
        print(f"  wait={wait!s:5} events={mode:5} bounce={bounce!s:5} offset={off} fin_evt={ee}: {d}")
    d, path = solve(wait=False, event_mode="zones")
    print("chemin (variante principale) :")
    for p, m, t in path:
        print(f"  t={t:2} {ROWS[p[0]]}{p[1]} {name(p)}  masque={m:04b}")
    print("REPONSE", d)
    (HERE / "answer.txt").write_text(f"{d}\n", encoding="utf-8")
