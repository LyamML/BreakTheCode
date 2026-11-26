"""Reimplementation independante (structure differente) de l'interpretation principale.
Compare le hash avec answer.txt. Lancer : python3 -I validate.py"""
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
txt = (HERE / "data" / "simulation2.txt").read_text(encoding="utf-8")
kv = dict(re.findall(r"^(DUREE|DILIGENCE|OR|SEED)=(\d+)$", txt, re.M))
ents = re.findall(r"^(SHERIF|CONDUCTEUR|BANDIT) (\w+)=(\d+)$", txt, re.M)

N, D, G, seed = int(kv["DUREE"]), int(kv["DILIGENCE"]), int(kv["OR"]) // 5, int(kv["SEED"])
S = next({"n": n, "x": int(p), "hp": 12, "am": 12} for k, n, p in ents if k == "SHERIF")
B = {n: {"x": int(p), "hp": 10, "am": 6, "bag": 0, "gone": False, "dis": False}
     for k, n, p in ents if k == "BANDIT"}
names = sorted(B)
ground = 0
cool = False       # rechargement
cool_set_turn = -1
out = []


def live():
    return [n for n in names if B[n]["hp"] > 0 and not B[n]["gone"]]


def emit(t, a, act, d):
    out.append("%04d;%s;%s;%s" % (t, a, act, d))


for t in range(1, N + 1):
    # sherif
    L = live()
    if L:
        tg = sorted(L, key=lambda n: (abs(B[n]["x"] - S["x"]), n))[0]
        dist = abs(B[tg]["x"] - S["x"])
        if dist <= 3 and S["am"] > 0 and not cool:
            S["am"] -= 1
            emit(t, S["n"], "SHOOT", tg)
            cool, cool_set_turn = True, t
            B[tg]["hp"] -= 2
            B[tg]["dis"] = True
            if B[tg]["hp"] <= 0:
                emit(t, tg, "DEATH", "")
                ground += B[tg]["bag"]
                B[tg]["bag"] = 0
        elif dist > 0:
            S["x"] += 1 if B[tg]["x"] > S["x"] else -1
            emit(t, S["n"], "MOVE", S["x"])
    # bandits
    for n in names:
        b = B[n]
        if b["hp"] <= 0 or b["gone"]:
            continue
        canmove = not (b["bag"] >= 3 and t % 2 == 0)
        if b["hp"] <= 2 or b["bag"] == 4:
            if b["x"] > 0 and canmove:
                b["x"] -= 1
                emit(t, n, "MOVE", b["x"])
        elif b["x"] == D and G > 0:
            G -= 1; b["bag"] += 1
            emit(t, n, "STEAL", 1)
        elif ground > 0:
            ground -= 1; b["bag"] += 1
            emit(t, n, "PICKUP", 1)
        elif abs(S["x"] - b["x"]) <= 3 and S["hp"] <= 2 and not b["dis"] and b["am"] > 0 and S["hp"] > 0:
            b["am"] -= 1; S["hp"] -= 2
            emit(t, n, "SHOOT", S["n"])
            if S["hp"] <= 0:
                emit(t, S["n"], "DEATH", "")
        elif b["x"] != D and canmove:
            b["x"] += 1 if D > b["x"] else -1
            emit(t, n, "MOVE", b["x"])
        b["dis"] = False
        if b["x"] == 0 and b["bag"] > 0:
            emit(t, n, "ESCAPE", b["bag"])
            b["gone"] = True
    # evenement
    stop = False
    if t % 23 == 0:
        seed = (1664525 * seed + 1013904223) & 0xFFFFFFFF
        X = seed % 5
        emit(t, "RANDOM", "RANDOM", X)
        if X == 1 and G > 0:
            G -= 1
        elif X == 2 and S["am"] > 0:
            S["am"] -= 1
        elif X == 3 and live():
            v = live()[0]
            B[v]["hp"] -= 1
            if B[v]["hp"] <= 0:
                emit(t, v, "DEATH", "")
                ground += B[v]["bag"]; B[v]["bag"] = 0
        elif X == 4:
            stop = True
    if not stop:
        D = min(20, D + 1)
    # fin de tour : le rechargement pose a un tour precedent est leve
    if cool and cool_set_turn < t:
        cool = False

journal = "".join(line + "\n" for line in out)
h = hashlib.sha256(journal.encode("utf-8")).hexdigest()
ans = (HERE / "answer.txt").read_text().strip()
print(len(out), "lignes")
print("validate :", h)
print("answer   :", ans)
print("ACCORD" if h == ans else "DESACCORD")
