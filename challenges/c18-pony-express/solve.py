import sys, heapq
from pathlib import Path
d = Path(__file__).parent
lines = (d/"data/input_rennes.txt").read_text().splitlines()
lines=[l.strip() for l in lines]
n = int(lines[0]); i = lines.index("---")
edges=[tuple(map(int,l.split(","))) for l in lines[i+1:] if l]
if len(sys.argv)>1 and sys.argv[1]=="ex":
    n=7; edges=[(1,2,100),(2,1,100),(2,3,120),(3,2,120),(4,5,6000),(5,4,6000),(6,7,200),(7,6,200)]
sys.setrecursionlimit(10**6)
adj=[[] for _ in range(n+1)]; radj=[[] for _ in range(n+1)]
for a,b,w in edges: adj[a].append((b,w)); radj[b].append(a)
# Kosaraju iteratif
seen=[False]*(n+1); order=[]
for s in range(1,n+1):
    if seen[s]: continue
    seen[s]=True; st=[(s,0)]
    while st:
        u,k=st.pop()
        if k<len(adj[u]):
            st.append((u,k+1)); v=adj[u][k][0]
            if not seen[v]: seen[v]=True; st.append((v,0))
        else: order.append(u)
comp=[-1]*(n+1); c=0
for s in reversed(order):
    if comp[s]!=-1: continue
    comp[s]=c; st=[s]
    while st:
        u=st.pop()
        for v in radj[u]:
            if comp[v]==-1: comp[v]=c; st.append(v)
    c+=1
members=[[] for _ in range(c)]
for v in range(1,n+1): members[comp[v]].append(v)
LIM=8*24*60
def dij(s):
    D={s:0}; h=[(0,s)]
    while h:
        d_,u=heapq.heappop(h)
        if d_>D[u]: continue
        for v,w in adj[u]:
            if comp[v]==comp[s] and d_+w<D.get(v,1e18): D[v]=d_+w; heapq.heappush(h,(d_+w,v))
    return D
res=[];sing=0;allc=[]
for m in members:
    if len(m)==1: sing+=1; allc.append(0); continue
    dd={u:dij(u) for u in m}
    L=max(dd[u][v]+dd[v][u] for u in m for v in m)
    allc.append(L)
    if L<=LIM: res.append(L)
res.sort()
print("nSCC",c,"singletons",sing,"multi",c-sing,"invalid",c-sing-len(res),file=sys.stderr)
a=f"{len(res)};"+";".join(map(str,res)); b=f"{len(res)+sing};"+";".join(map(str,sorted([x for x in allc if x<=LIM])))
print(a); print("variante singletons:",b[:80])
if len(sys.argv)==1: (d/"answer.txt").write_text(a)
