from pathlib import Path

def step(x, y, vx, vy):
    x += vx; y += vy
    b = 0
    if x < 0 or x > 99: vx = -vx; b = 1
    if y < 0 or y > 99: vy = -vy; b = 1
    return x, y, vx, vy, b

def trajectory(s, n):
    x, y, vx, vy = s
    out = []
    for t in range(n):
        out.append((t, x, y))
        x, y, vx, vy, _ = step(x, y, vx, vy)
    return out

# tests exemples énoncé
assert trajectory((0,1,-1,3),3)[1:] == [(1,-1,4),(2,0,7)]
assert trajectory((98,99,3,3),4)[1:] == [(1,101,102),(2,98,99),(3,95,96)]

rows = [list(map(int, l.split())) for l in (Path(__file__).parent/"data/bullets.data.txt").read_text().splitlines() if l.strip()]
xc, yc = rows[0]; bullets = rows[1:]
N = 200000
best = {}  # variante -> (t, idx)
for i, (x, y, vx, vy) in enumerate(bullets):
    bounced = False
    for t in range(N):
        if x == xc and y == yc:
            for k, ok in (("all", True), ("bounced", bounced)):
                if ok and (k not in best or t < best[k][0]): best[k] = (t, i)
            if k == "all": pass
        x, y, vx, vy, b = step(x, y, vx, vy)
        bounced |= bool(b)
print(len(bullets), "balles; cible", xc, yc, best)
# t=0 présent ?
print("t=0 sur cible:", [i for i,r in enumerate(bullets) if r[0]==xc and r[1]==yc])
ans = best["bounced"][0]
print(ans)
(Path(__file__).parent/"answer.txt").write_text(str(ans)+"\n")
