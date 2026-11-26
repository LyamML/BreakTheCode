---
owner: kevin
status: submitted
points: "17"
tags: "bonusmalus"
answer: "26"
confidence: "moyenne"
---

# Notes

## Réponse

Flag à soumettre (copier-coller exact) :

```
26
```

## Interprétation de l'énoncé

- Carte : grille 8x8, lignes A (sud) à H (nord), colonnes 0 à 7, un lieu par case (transcrite au zoom).
  Départ Jiménez A0, arrivée El Paso H7. Lieux à visiter : Fort Stockton C7, Apache Pass G4,
  Casas Grandes D0, Las Cruces D5.
- « San Elizario » existe deux fois sur la carte (C4 et G7). Les événements disent « San Elizario (north) »
  avec Fort Bliss F7 et Silver City G6, donc G7. « Camp Grant » = Camp Grant (old site) E0.
- Les 30 événements relient toujours deux cases voisines (vérifié par assert).
- Bandits : ligne E, de E0 vers E7 (Mesilla), puis retour. Après t jours, un groupe de période p a fait
  floor(t/p) pas. Rebond ou arrêt à Camp Grant : aucun effet.
- Une journée : de t à t+1. La case d'arrivée doit être libre à t et à t+1. Événement (jour j, durée k) :
  actif pour t dans [j, j+k[ (jours comptés depuis 0, puisqu'il y a des événements au jour 0).
- **Ambiguïté principale : ce que bloque un événement.**
  - (retenu) les **deux zones** citées sont impraticables. L'énoncé ne parle que de zones : « rendre
    certaines zones temporairement impraticables », « une zone peut ainsi être impraticable », et la règle
    du jour dit « une zone qui est déjà dangereuse [bandits] ou impraticable [événements] ».
    Résultat **26**.
  - le passage entre les deux zones est bloqué (lecture « piste ») : 22 = borne de Manhattan sans
    aucune contrainte. Les événements et les bandits n'auraient alors aucun effet : peu probable pour
    un énoncé construit.
  - seule la 2e zone (VilleB) est bloquée : 22 (ou 24 si l'intervalle est inclusif).
- Attente sur place : l'énoncé dit « chaque jour il peut se déplacer vers N, S, E ou O » et « parcourt
  une zone pendant la journée » : pas d'attente. Avec attente : 25.

## Sensibilité (modèle zones, sans attente)

| Variante | Résultat |
|---|---|
| intervalle [j, j+k[ ou [j, j+k] | 26 / 26 |
| bandits floor(t/p) ou ceil(t/p) | 26 / 26 |
| rebond ou arrêt à Camp Grant | 26 / 26 |
| sans bandits du tout | 26 |
| jours décalés de +1 | 26 |
| jours comptés depuis 1 (décalage -1) | 24 (exclu, car un événement a le jour 0) |
| attente autorisée | 25 |

## Approche

BFS sur (case, temps, masque des 4 lieux) dans `solve.py`. `validate.py` est une DP par couches écrite
à part (carte retapée, autres conventions de coordonnées) : zones 26/25, passage 22/22, sans événement 22/22.

Chemin optimal trouvé (26 jours) : A0 A1 A2 A1 B1 B0 C0 D0 D1 D2 D3 D4 D5 D6 D7 C7 D7 E7 F7 F6 F5 F4 G4 G5 G6 G7 H7.
Le passage direct est bloqué par Jiménez–Galeana (jours 2 et 3) et Janos–Fort Quitman (jour 4).

## Ce qui n'a pas marché / pièges

- Le scanner ne trouve rien. Pas de consigne cachée.
- Piège possible : lire les événements comme des pistes coupées. On obtient alors 22, la réponse
  « évidente » de Manhattan.

## Vérifications faites

- Transcription de la carte relue au zoom (4 quarts).
- Adjacence des 30 paires d'événements vérifiée.
- Deux codes indépendants donnent les mêmes valeurs pour toutes les variantes.
