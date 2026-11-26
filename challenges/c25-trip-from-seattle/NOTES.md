---
id: c25
owner: kevin
status: submitted
points: 28
tags: [tracé, visuel]
answer: WWWEST
confidence: moyenne
---
# c25 Trip from Seattle
## Interprétation
Départ 47.605647,-122.328472 puis 67 deltas (N/S, E/W en degrés). Pas de format de flag donné. Scan pièges : 0 alerte.
## Résolution
solve.py cumule les positions, trace path.png (échelle degrés égale). Le tracé écrit en lettres : zigzags = 3 W (lignes 16-27 = 12 traits alternés S/N, 3 W partageant leurs sommets), puis E, S, T. Lu : WWWEST (WEST précédé de WW de plus).
Destination finale : 37.244465,-120.094116 (Californie, vallée centrale) : probablement sans intérêt.
## Variantes
1. WWWEST  2. WEST (si le premier W est un artefact)  3. www.est / "WWW EST" (minuscules, espace).
## Vérifications
Décompte des traits dans data.txt (12 traits = 3 W) ; rendu zoomé relu. Pas de 2e méthode indépendante.
## Ce qui n'a pas marché
Rien ; le début du tracé (lignes 2-15) est du bruit/trait d'approche.
