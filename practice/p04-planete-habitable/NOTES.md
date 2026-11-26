---
owner: lyam
status: solved
points: "33"
tags: "Moyen, Plus court chemin"
answer: "Terre,Eoseaion,Lunaaron,Helioisyx,Ceranon,Lyraeaus,Phosunion,Neptanos,Helioeaar,Astraisium,Lyraoris,Lunaunos,Orionisara,Cerosarae"
confidence: haute
---

# Notes — p04 A la recherche d'une nouvelle planète habitable (33 pts)

## Réponse

Flag à soumettre (copier-coller exact) :

```
Terre,Eoseaion,Lunaaron,Helioisyx,Ceranon,Lyraeaus,Phosunion,Neptanos,Helioeaar,Astraisium,Lyraoris,Lunaunos,Orionisara,Cerosarae
```

Coût total 701 (Terre→Phosunion 249, Phosunion→Neptanos 191, Neptanos→Cerosarae 261).

## Interprétation de l'énoncé

Contraintes tirées du message décodé de **p05** (challenge enchaîné, indispensable) :

| Consigne du message | Traduction |
|---|---|
| « arrivés sur la planète CEROSARAE » | cible = `Cerosarae` |
| « VEGAELUS ET ZORAORARA à éviter absolument » | nœuds interdits |
| « passer par PHOSUNION **puis** NEPTANOS » | waypoints obligatoires, dans cet ordre |
| « vous **pouvez** aller sur TARAISIS » | optionnel → non imposé |

- Départ : `Terre` (on est « chef sur Terre » dans p05, et l'exemple commence par Terre).
- Format : départ et arrivée inclus, séparés par `,` sans espace (cf. exemple
  `Terre,Zenoisium,Thalis`).

Alternatives calculées (`python -I solve.py --details`) :

| Variante | Coût | Commentaire |
|---|---|---|
| **Retenue** : waypoints dans l'ordre + évitement | **701** | |
| Waypoints sans évitement | 701 | même chemin → l'évitement ne change rien ici |
| Ordre inversé Neptanos→Phosunion | 718 | « puis » impose l'ordre |
| + Taraisis après Neptanos | 705 | `…,Neptanos,Cereaeus,Phosorrus,Taraisis,Vegaisrus,Argoarnia,Vegaeaon,Cerosarae` — seule alternative plausible si Taraisis était obligatoire |
| + Taraisis entre les deux waypoints | 792 | |
| + Taraisis avant Phosunion | 904 | |
| Évitement seul (sans waypoints) | 324 | |
| Aucune contrainte | 318 | passe par Vegaelus et Zoraorara : le piège visé par l'énoncé |

## Approche

1. Inspection du JSON : dict d'adjacence `{planète: {voisine: distance}}`, 2 501
   planètes, 128 528 arcs, **symétrique**, poids entiers > 0, pas de boucle. Même format
   que l'exemple.
2. Dijkstra par segments : Terre→Phosunion→Neptanos→Cerosarae, nœuds interdits retirés.
   Concaténation des segments.

## Ce qui a marché

- Dijkstra segment par segment (optimal car waypoints ordonnés et poids positifs).
- Mode `--details` qui calcule toutes les variantes d'interprétation d'un coup : en cas
  de doute, on voit tout de suite si l'ambiguïté change la réponse.

## Ce qui n'a pas marché / pièges

- Le vrai piège est **amont** : sans le message de p05, impossible de connaître cible et
  contraintes. Le chemin sans contrainte (318) passe justement par les deux planètes
  interdites.
- Risque théorique de la concaténation : une planète répétée entre deux segments (à
  vérifier si l'énoncé exige un chemin simple). Ici aucune répétition.
- Ex-aequo possibles avec des poids entiers : vérifiés, aucun.

## Vérifications faites

- Deuxième implémentation indépendante (`scipy.sparse.csgraph.dijkstra`) : mêmes
  distances 249 / 191 / 261.
- **Unicité** : 1 seul plus court chemin par segment (comptage des chemins sur les arcs
  serrés) → pas d'ambiguïté d'ex-aequo.
- Aucune planète interdite, aucune répétition, 14 planètes.

## Temps / difficulté réelle

~5 min une fois p05 décodé. Exécution < 1 s.

## Leçons pour le jour J

1. **Challenges enchaînés** : quand un énoncé cite un autre exercice, résoudre l'autre
   d'abord et lire **tout** son résultat (ici les contraintes étaient dans le message
   audio). Les deux doivent être tenus par la même personne ou communiqués vite.
2. Waypoints ordonnés = Dijkstra par segments ; nœuds interdits = les retirer du graphe.
   Si un ordre n'est pas imposé, tester les permutations.
3. Toujours vérifier unicité/ex-aequo quand les poids sont entiers : deux chemins de même
   coût = deux flags possibles.

## Journal

| Heure | Action | Résultat |
|---|---|---|
| 18:56 | Lecture du message p05 | cible + contraintes |
| 18:57 | Inspection JSON | symétrique, 2 501 nœuds |
| 18:59 | Dijkstra + variantes | coût 701 |
| 19:00 | Contre-vérif scipy + unicité | identique, chemin unique |
