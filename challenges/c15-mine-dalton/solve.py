"""c15 La mine des Dalton : BFS exact par couches de temps sur l'etat (case, masque pepites).

Grille transcrite depuis data/salle_D.png (couleurs echantillonnees par Pillow, voir
NOTES.md) ; temps des 30 batons lus sur un agrandissement.
"""
from pathlib import Path

HERE = Path(__file__).parent

GRID = [
    "E..#........D..#...",
    "##.#.###D#####.#.#.",
    ".#...#...#...#.#.#.",
    ".#.#.#...###.#.#D#.",
    "...#.#.....#...#.#D",
    ".#######.#.#D###.#.",
    ".#....D....#.......",
    "D#.###.#####...###D",
    ".#.#...D..D#...D...",
    ".#.#D###.#3#.#.###.",
    "...#..8.D#.#.#D#D..",
    "##.#.###7#.#.#.###.",
    "....D.D#...#.#.#D..",
    "6#D###5###D#.#.#.#.",
    "D#.#.#.9D1.#.#.#.#.",
    ".#.#.#####.#.#.#D#.",
    ".#D#......D#.#DD4#.",
    ".#.#########.#####.",
    ".#.............2.#X",
]
# batons : (r, c) -> t  (les cases 3, 8, 6 portent aussi un baton)
STICKS = {
    (0, 12): 186, (1, 8): 48, (3, 16): 148, (4, 18): 104, (5, 12): 96,
    (6, 6): 161, (7, 0): 111, (7, 18): 139, (8, 7): 168, (8, 10): 98,
    (8, 15): 11, (9, 4): 21, (9, 10): 94, (10, 6): 30, (10, 8): 71,
    (10, 14): 55, (10, 16): 136, (12, 4): 151, (12, 6): 91, (12, 16): 87,
    (13, 0): 112, (13, 2): 106, (13, 10): 89, (14, 0): 70, (14, 8): 120,
    (15, 16): 101, (16, 2): 10, (16, 10): 131, (16, 14): 122, (16, 15): 143,
}

EXAMPLE = (["E.....X", "###.###", ".......", "###.###", "...1..."], {(1, 3): 12}, 1)

INF = 10 ** 9


def solve(grid, sticks, pass_through_x=False, tmax=1200):
    R, C = len(grid), len(grid[0])
    assert all(len(row) == C for row in grid), [len(r) for r in grid]
    col = [[INF] * C for _ in range(R)]
    for (r, c), t in sticks.items():
        for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < R and 0 <= cc < C:
                col[rr][cc] = min(col[rr][cc], t)
    nug = {}
    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch == 'E':
                start = (r, c)
            elif ch == 'X':
                exit_ = (r, c)
            elif ch.isdigit():
                nug[(r, c)] = int(ch)
    def bit(p):
        return (1 << (nug[p] - 1)) if p in nug else 0
    best = -1
    if col[start[0]][start[1]] <= 0:
        return best
    layer = {(start, bit(start))}
    seen_static = set()
    last_change = max(list(sticks.values()) + [0])
    for t in range(tmax):
        nxt = set()
        for (r, c), m in layer:
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr, cc = r + dr, c + dc
                if not (0 <= rr < R and 0 <= cc < C):
                    continue
                if grid[rr][cc] == '#' or t + 1 >= col[rr][cc]:
                    continue
                m2 = m | bit((rr, cc))
                if (rr, cc) == exit_:
                    best = max(best, bin(m2).count('1'))
                    if not pass_through_x:
                        continue
                nxt.add(((rr, cc), m2))
        layer = nxt
        if not layer:
            break
        if t > last_change + 2:
            # graphe statique : on arrete quand les couches deviennent periodiques
            key = frozenset(layer)
            if key in seen_static:
                break
            seen_static.add(key)
    return best


def main():
    g, s, exp = EXAMPLE
    got = solve(g, s)
    print("exemple :", got, "(attendu", exp, ")")
    assert got == exp
    assert solve(g, {(1, 3): 11}) == 0  # reglage 11 : le detour tue (enonce)
    assert len(GRID) == 19 and all(len(r) == 19 for r in GRID)
    grid = [row.replace('D', '.') for row in GRID]
    # verif coherence : chaque 'D' du plan = un baton
    ds = {(r, c) for r in range(19) for c in range(19) if GRID[r][c] == 'D'}
    assert ds <= set(STICKS) and len(STICKS) == 30
    assert sum(ch.isdigit() for row in grid for ch in row) == 9
    a = solve(grid, STICKS)
    b = solve(grid, STICKS, pass_through_x=True)
    print("reponse (X termine) :", a, "| variante (on peut repasser par X) :", b)
    (HERE / "answer.txt").write_text(f"{a}\n")


if __name__ == "__main__":
    main()
