---
owner: kevin
status: wip
points: 23
tags: SCC, Dijkstra
confidence: haute
---
# c18 Pony Express
## Interprétation
SCC (Kosaraju), longueur = max d(u,v)+d(v,u) dans la SCC, valide si <= 11520 min. Format `N;l1;...` trié. Scan : 0 alerte (CRLF seulement).
## Résultat
5903 SCC dont 5879 singletons et 24 SCC multi-villages, toutes <= 11520. Réponse : voir answer.txt (24 zones). Exemple reproduit : 2;400;440.
## Variantes
Singletons comptés (longueur 0) : 5903;0;0;... peu plausible (pas de groupe ni d'aller-retour).
## Vérification
scipy connected_components + dijkstra global : mêmes 24 valeurs.
## Ce qui n'a pas marché
Rien.
