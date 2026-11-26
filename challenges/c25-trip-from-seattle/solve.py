from pathlib import Path
from PIL import Image, ImageDraw
d=Path(__file__).parent
L=(d/'data'/'data.txt').read_text().split('\n')
L=[l.strip() for l in L if l.strip()]
lat,lon=map(float,L[0].split(','))
P=[(lat,lon)]
for l in L[1:]:
    a,b=l.split(',')
    dy=float(a[:-1])*(1 if a[-1]=='N' else -1)
    dx=float(b[:-1])*(1 if b[-1]=='E' else -1)
    lat+=dy;lon+=dx;P.append((lat,lon))
print(len(P),P[-1])
xs=[p[1] for p in P];ys=[p[0] for p in P]
S=150;m=40
W=int((max(xs)-min(xs))*S)+2*m;H=int((max(ys)-min(ys))*S)+2*m
im=Image.new('RGB',(W,H),'white');dr=ImageDraw.Draw(im)
pt=[(m+(x-min(xs))*S,m+(max(ys)-y)*S) for x,y in zip(xs,ys)]
dr.line(pt,fill='black',width=3)
im.save(d/'path.png')
(d/'answer.txt').write_text('WWWEST\n')
print('WWWEST')
