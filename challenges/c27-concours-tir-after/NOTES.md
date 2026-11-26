---
owner: kevin
status: solved
points: 29
tags: simulation, visuel
answer: "Abraham Lincoln"
confidence: moyenne (image certaine, format du flag non specifie)
---

# c27 Concours de tir : After party

## Interpretation
- 126 archives (`bullets.N.txt` dans `data/bullets.data.zip`). Ligne 1 = `t`, puis `x y vx vy`.
- Regles de simulation identiques a c24 (position += vitesse ; si x<0 ou x>99, vx s'inverse ; idem y).
- "Combiner toutes ces simulations pour faire emerger une image d'ensemble".
- Aucun format de flag donne (pas de "Format du flag : MOT" contrairement a c16).
- `scan_traps.py` : 0 alerte, 0 avertissement. Pas de HTML cache dans l'enonce.

## Methode
- Lecture du zip en memoire (`zipfile`), rien d'execute.
- Pour chaque archive, simulation de chaque balle jusqu'a son `t`, position notee.
- 3209 balles -> 3209 positions **toutes distinctes** (aucune collision) : la construction
  est clairement "toutes les balles a t = un pixel de l'image". La notion de "cible" est
  un detour narratif : la tentative "garder seulement les positions jamais visitees avant t"
  donne la meme image, en plus bruitee (sous-ensemble).
- Rendu 100x100, ligne = y (y vers le bas, convention ecran) : `portrait.png`.
  Avec y vers le haut (`portrait_yup.png`) le portrait est a l'envers -> convention ecran retenue.
- Image : portrait de face/trois-quarts, cheveux sombres, barbe en collier sans moustache,
  col et noeud papillon : **Abraham Lincoln** (photo type Gardner/Brady, celle du billet de 5 $).
  Aucun texte dans l'image.

## Verifications
- Positions initiales seules (`init`) : nuage sans structure -> l'image vient bien de la simulation a t.
- Simulation verifiee sur les deux exemples de c24 (rebond (0,1)/(-1,3) -> (-1,4) -> (0,7) ; (98,99)/(3,3) -> (101,102) -> (98,99) -> (95,96)) : la boucle applique exactement cette regle.
- Unicite des 3209 positions = signature d'une image volontairement encodee.

## Variantes (format du flag inconnu)
1. `Abraham Lincoln` (nom complet, le plus probable)
2. `Lincoln`
3. `ABRAHAM LINCOLN` / `abraham lincoln` (CTFd souvent insensible a la casse si configure)

Malus sur mauvaise reponse : verifier sur la plateforme s'il y a un format affiche avant de soumettre.

## Pieges
- Aucune consigne cachee. Piege de sens : chercher "la" cible par archive (ambigu, ~20 candidats
  par archive) au lieu de tracer toutes les balles.
