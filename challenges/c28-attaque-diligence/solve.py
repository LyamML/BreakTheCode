"""c28 - L'attaque de la diligence : simulation deterministe -> SHA256(journal).

Regles lues dans data/regles.png (voir NOTES.md). Lancer : python3 -I solve.py
Les options (variantes d'interpretation) servent a l'analyse de sensibilite.
"""
import hashlib
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "simulation2.txt"

MOD = 2 ** 32


def parse(text):
    cfg = {"bandits": []}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        key, val = line.split("=", 1)
        key, val = key.strip(), val.strip()
        if " " in key:
            kind, name = key.split(None, 1)
            if kind == "BANDIT":
                cfg["bandits"].append((name, int(val)))
            elif kind == "SHERIF":
                cfg["sherif"] = (name, int(val))
            elif kind == "CONDUCTEUR":
                cfg["conducteur"] = (name, int(val))
            else:
                raise ValueError(line)
        else:
            cfg[key] = int(val)
    return cfg


class P:
    def __init__(self, name, pos, pv, mun):
        self.name, self.pos, self.pv, self.mun = name, pos, pv, mun
        self.sacs = 0
        self.escaped = False
        self.disoriented = False

    @property
    def alive(self):
        return self.pv > 0 and not self.escaped


def simulate(cfg, ground_positional=False, flee_encumbered=True,
             x3_disorients=False, sheriff_reload_skip=1, zero_mode="none",
             global_turn_end=False):
    rng = cfg["SEED"] % MOD

    def nxt():
        nonlocal rng
        rng = (1664525 * rng + 1013904223) % MOD
        return rng

    sname, spos = cfg["sherif"]
    sh = P(sname, spos, 12, 12)
    reload_until = 0          # le sherif ne peut pas tirer tant que tour <= reload_until
    cname, cpos = cfg["conducteur"]
    _cond = P(cname, cpos, 10, 0)  # n'agit jamais
    bandits = sorted((P(n, p, 10, 6) for n, p in cfg["bandits"]), key=lambda b: b.name)
    dil_pos = cfg["DILIGENCE"]
    dil_sacs = cfg["OR"] // 5
    ground = {} if ground_positional else [0]
    stolen = 0
    log = []

    def ground_count(pos):
        if ground_positional:
            return ground.get(pos, 0)
        return ground[0]

    def ground_take(pos):
        if ground_positional:
            ground[pos] -= 1
        else:
            ground[0] -= 1

    def die(t, who):
        log.append(f"{t:04d};{who.name};DEATH;")
        if ground_positional:
            ground[who.pos] = ground.get(who.pos, 0) + who.sacs
        else:
            ground[0] += who.sacs
        who.sacs = 0

    def hit(t, target, dmg, disorient):
        target.pv -= dmg
        if disorient and target in bandits:
            target.disoriented = True
        if target.pv <= 0:
            die(t, target)

    def nearest_bandit(pos):
        alive = [b for b in bandits if b.alive]
        if not alive:
            return None
        return min(alive, key=lambda b: (abs(b.pos - pos), b.name))

    for t in range(1, cfg["DUREE"] + 1):
        # 1. Sherif
        if sh.alive:
            tgt = nearest_bandit(sh.pos)
            can_shoot = sh.mun > 0 and t > reload_until
            if tgt is not None and abs(tgt.pos - sh.pos) <= 3 and can_shoot:
                sh.mun -= 1
                log.append(f"{t:04d};{sh.name};SHOOT;{tgt.name}")
                reload_until = t + sheriff_reload_skip
                hit(t, tgt, 2, True)
            elif tgt is not None and (tgt.pos != sh.pos or zero_mode != "none"):
                if tgt.pos != sh.pos:
                    step = 1 if tgt.pos > sh.pos else -1
                else:
                    step = 0 if zero_mode == "stay" else -1
                np_ = sh.pos + step
                if 0 <= np_ <= 20:
                    sh.pos = np_
                    log.append(f"{t:04d};{sh.name};MOVE;{sh.pos}")
                elif global_turn_end:
                    continue
            elif global_turn_end:
                continue  # action impossible : tout le tour s'arrete (variante)
            # sinon : action impossible, aucune ligne
        # 2. Conducteur : aucune action
        # 3. Bandits (ordre alphabetique)
        stop_turn = False
        for b in bandits:
            if not b.alive:
                continue
            n_before = len(log)
            encumbered_block = (b.sacs >= 3 and t % 2 == 0)
            if b.pv <= 2 or b.sacs == 4:
                # FUIR vers 0
                if b.pos > 0 and not (flee_encumbered and encumbered_block):
                    b.pos -= 1
                    log.append(f"{t:04d};{b.name};MOVE;{b.pos}")
            elif b.pos == dil_pos and dil_sacs > 0:
                dil_sacs -= 1
                b.sacs += 1
                log.append(f"{t:04d};{b.name};STEAL;1")
            elif ground_count(b.pos) > 0:
                ground_take(b.pos)
                b.sacs += 1
                log.append(f"{t:04d};{b.name};PICKUP;1")
            elif (sh.alive and abs(sh.pos - b.pos) <= 3 and sh.pv <= 2
                  and not b.disoriented and b.mun > 0):
                b.mun -= 1
                log.append(f"{t:04d};{b.name};SHOOT;{sh.name}")
                hit(t, sh, 2, False)
            else:
                if b.pos != dil_pos and not encumbered_block:
                    b.pos += 1 if dil_pos > b.pos else -1
                    log.append(f"{t:04d};{b.name};MOVE;{b.pos}")
            b.disoriented = False
            if global_turn_end and len(log) == n_before:
                stop_turn = True
                break
            if b.alive and b.pos == 0 and b.sacs >= 1:
                log.append(f"{t:04d};{b.name};ESCAPE;{b.sacs}")
                stolen += b.sacs * 5
                b.sacs = 0
                b.escaped = True
        if stop_turn:
            continue
        # 4. Evenement special
        dil_stops = False
        if t % 23 == 0:
            r = nxt()
            x = r % 5
            log.append(f"{t:04d};RANDOM;RANDOM;{x}")
            if x == 1 and dil_sacs > 0:
                dil_sacs -= 1
            elif x == 2 and sh.mun > 0:
                sh.mun -= 1
            elif x == 3:
                alive = [b for b in bandits if b.alive]
                if alive:
                    v = min(alive, key=lambda b: b.name)
                    hit(t, v, 1, x3_disorients)
            elif x == 4:
                dil_stops = True
        # 5. Diligence
        if not dil_stops and dil_pos < 20:
            dil_pos += 1
    return log, stolen


def journal_bytes(log, sep="\n", final=True):
    s = sep.join(log) + (sep if final and log else "")
    return s.encode("utf-8")


def main():
    cfg = parse(DATA.read_text(encoding="utf-8"))
    log, stolen = simulate(cfg)
    h = hashlib.sha256(journal_bytes(log)).hexdigest()
    if "-v" in sys.argv:
        print("\n".join(log))
        print("lignes:", len(log), "or derobe:", stolen, file=sys.stderr)
        print("sans \\n final :", hashlib.sha256(journal_bytes(log, final=False)).hexdigest(), file=sys.stderr)
        for gp, fe, x3, rs, zm, ge in itertools.product([False, True], [True, False], [False], [1, 0],
                                                         ["none", "stay", "minus"], [False, True]):
            l2, _ = simulate(cfg, gp, fe, x3, rs, zm, ge)
            print(f"ground_pos={gp} flee_enc={fe} reload_skip={rs} zero={zm} global_end={ge}:",
                  hashlib.sha256(journal_bytes(l2)).hexdigest(), "identique" if l2 == log else "DIFFERENT",
                  file=sys.stderr)
    (HERE / "answer.txt").write_text(h + "\n", encoding="utf-8")
    print(h)


if __name__ == "__main__":
    main()
