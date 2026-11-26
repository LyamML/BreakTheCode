---
id: c16
owner: kevin
status: submitted
points: 21
tags: [binaire, filtrage]
answer: BANDIT
confidence: haute
---
# c16 Le Duel Truque

## Interpretation
Format flag : MOT. 56 heures de tirs. 7 tirs parasites (millisecondes hors grille .200/.700) filtres, il reste 49 tirs.
Ecarts entre tirs : 1.0 s = bit 0, 1.5 s = bit 1. 48 bits = 6 octets ASCII = BANDIT.
Scan pieges : aucune consigne dans l'enonce ni les donnees.

## Verifications
Mot coherent, 48 bits (multiple de 8), ASCII majuscules.

## Ce qui n'a pas marche
Comptage de tirs par groupes (2,5,3,6,...) : pas de mot lisible. Morse non necessaire.

## Variantes
Inversion des bits (0 et 1 echanges) : caracteres non lisibles.
