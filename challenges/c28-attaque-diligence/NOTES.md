---
owner: kevin
status: solved
points: "53"
tags: "bonusmalus"
answer: "70109e48139744f248ec94bea01769b8130d22c5e49b327c0694319734b7ce3d"
confidence: moyenne
---

# Notes

## Réponse

Flag à soumettre (copier-coller exact) :

```
70109e48139744f248ec94bea01769b8130d22c5e49b327c0694319734b7ce3d
```

Le journal fait 168 lignes, chacune terminée par `\n` (y compris la dernière). Or dérobé : 40 kg (Adam et Alan s'échappent au tour 59 avec 4 sacs chacun).

## Interprétation de l'énoncé

Règles lues dans `data/regles.png` (1536x1024), section par section après un zoom x2.
- Entrée `simulation2.txt` : DUREE=100, DILIGENCE=5, OR=500 (100 sacs), SEED=42, shérif Wyatt=20,
  conducteur Hank=5, bandits Aaron/Abel/Adam/Alan=5.
- Stats : shérif PV 12 / mun 12 ; bandit PV 10 / mun 6 ; conducteur PV 10, sans action.
- Ordre d'un tour : shérif, conducteur, bandits (ordre alphabétique), événement (tours multiples de 23), diligence +1 (plafond 20).
- PRNG : `state = (1664525*state + 1013904223) mod 2^32`, et next() renvoie le nouvel état. Au tour 23, R=1083814273 et X=3.
- Journal : `TOUR;ACTEUR;ACTION;DETAIL`, TOUR sur 4 chiffres (`0001`), DEATH avec un détail vide
  (`0016;Aaron;DEATH;`), RANDOM écrit `TOUR;RANDOM;RANDOM;X`. Encodage UTF-8, LF, pas de CR, « pas de ligne
  vide sauf la dernière » : chaque ligne finit donc par `\n`.

Choix retenus pour les ambiguïtés (hash de chaque variante, avec un `\n` final) :

| Hypothèse | Retenu | Hash si on inverse le choix |
|---|---|---|
| Sol = réserve globale (PICKUP sans condition de position, comme écrit dans la section 2) | oui | sol par position : 14128dee… |
| Encombrement (3-4 sacs, tour pair) bloque aussi la fuite | oui | sans blocage : 1780f667… |
| Rechargement : le shérif ne tire pas au tour qui suit un tir, et le drapeau est levé à la fin de ce tour | oui | aucun effet : 7753589b… |
| Shérif à distance 0 de sa cible et ne pouvant pas tirer : action impossible, pas de ligne (tour 33) | oui | MOVE sur place : 0ab6f8cd… ; pas de -1 : 21635664… |
| « Le tour se termine » ne concerne que le personnage | oui | tout le tour s'arrête : 5546a67e… |
| Sans `\n` final | non | 1bc8ef964ce38a07f04d7ef243a19f0219b25e2b753d1f48997cc253657b0bc4 |
| Le X=3 désoriente-t-il ? | sans effet | identique |

Les bandits ne tirent jamais, car il faudrait que le shérif ait au plus 2 PV et il n'est jamais touché. La désorientation et les munitions des bandits ne changent donc rien.

## Approche

`solve.py` lance la simulation directe, avec des options pour chaque variante (`-v` affiche le journal et le tableau des variantes).
`validate.py` est une seconde implémentation écrite autrement (regex, dictionnaires, rechargement levé en fin de tour) : elle donne le même hash (ACCORD).

## Ce qui n'a pas marché / pièges

- Le hash d'exemple de la section 13 (`e3b0c442…b855`) est le SHA256 de la chaîne vide : c'est un leurre, et il ne
  sert pas à valider une implémentation.
- L'exemple de la section 10 (DUREE=1000, OR=5000…) et la ligne `0001;Tom;MOVE;5` ne montrent que le format : ce ne sont pas les données.
- Dans la section 3, le bandeau gris sous « Bandits (IA) » est du faux texte illisible : ignoré.
- Le scanner ne trouve rien (0 alerte), et l'énoncé ne contient pas de consigne cachée.
