"""Verification independante : DP par couches de temps (ensembles d'etats), code separe de solve.py.
Coordonnees (x=colonne 0..7, y=ligne A=0..H=7). Lancer : python3 -I validate.py
"""
from pathlib import Path

D = Path(__file__).parent / "data"
CARTE = """H|Fort Mason|Fort Lowell|Dragoon Springs|Council Rocks|Cochise Stronghold|Fort Bowie|San Simon|El Paso
G|Safford|San Pedro River Station|Tubac|Dragoon Mountains|Apache Pass|Hachita|Silver City|San Elizario (north)
F|Fort Apache|Camp Crittenden|Pinos Altos|Naco|Fairbank|Fort Cummings|Lordsburg|Fort Bliss
E|Camp Grant|Santa Rita del Cobre|Animas|Fort Grant|Mimbres|Fort Selden|Deming|Mesilla
D|Casas Grandes|Ascensión|Janos|Fort Quitman|Guadalupe Pass|Las Cruces|Lincoln|Socorro
C|Buenaventura|Santa Isabel|Ojinaga|Chihuahua|San Elizario|Fort Davis|Pecos River Crossing|Fort Stockton (St. Gall)
B|Galeana|Cuauhtémoc|Aldama|Camargo|Fort Lancaster|Comanche Springs|Van Horn Wells|Horsehead Crossing
A|Jiménez|Santa Bárbara|Rosales|Meoqui|Santa Agustín Springs|Sanderson|Presidio|Boquillas"""
P = {}
for line in CARTE.splitlines():
    r, *ns = line.split("|")
    for x, n in enumerate(ns):
        P[n] = (x, "ABCDEFGH".index(r))
P["Camp Grant (old site)"] = P["Camp Grant"]

cps = [P[l.split(",")[0]] for l in (D / "checkpoints_voyage.txt").read_text("utf-8").splitlines() if l.strip()]
evs = []
for l in (D / "evenements_voyage.txt").read_text("utf-8").splitlines():
    if l.strip() and not l.startswith("#"):
        f = l.split(",")
        evs.append((P[f[0]], P[f[1]], int(f[3]), int(f[4])))


def bandits(t):
    out = set()
    for p in (1, 3, 5):
        m = (t // p) % 14
        out.add((m if m <= 7 else 14 - m, P["Mesilla"][1]))
    return out


def bad_zone(z, t, mode):
    if z in bandits(t):
        return True
    if mode == "zones":
        return any(j <= t < j + k and z in (a, b) for a, b, j, k in evs)
    return False


def bad_edge(u, v, t, mode):
    return mode == "edge" and any((j <= t < j + k or j <= t + 1 < j + k) and {u, v} == {a, b} for a, b, j, k in evs)


def run(mode, wait):
    goal, full = P["El Paso"], (1 << len(cps)) - 1
    layer = {(P["Jiménez"], 0)}
    for t in range(200):
        if any(z == goal and m == full for z, m in layer):
            return t
        nxt = set()
        for (x, y), m in layer:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] + ([(0, 0)] if wait else []):
                v = (x + dx, y + dy)
                if not (0 <= v[0] < 8 and 0 <= v[1] < 8):
                    continue
                if bad_zone(v, t, mode) or bad_zone(v, t + 1, mode) or bad_edge((x, y), v, t, mode):
                    continue
                nxt.add((v, m | (1 << cps.index(v)) if v in cps else m))
        layer = nxt
    return 0


for mode in ("zones", "edge", "none"):
    for wait in (False, True):
        print(f"{mode:5} attente={wait}: {run(mode, wait)}")
