---
owner: kevin
status: solved
points: 39
tags: bonusmalus (malus si mauvaise réponse)
answer: MEET OK CROSSROADS SET OLD SIGN ACTIVE HOLD UNTIL NIGHT SHIFT
confidence: moyenne (déchiffrement certain, format du flag non spécifié)
---

# c22 — Attaque du train

## Interprétation
- Entrée : `telegraphe.png` (Western Union, Brownstown, Jackson County, Indiana, 30 sept. 1866, 8.50 PM),
  4 lignes de Morse ; `The_Plain_Dealer_Gazette.png` (journal du même jour).
- Journal : avis de recherche « members of the notorious **RENO GANG** » + encart
  « VIGENÈRE MANUSCRIPT DISCOVERED … polyalphabetic substitution » -> méthode = Vigenère, clé = RENO.
- Format du flag : **non donné** dans l'énoncé ni dans les images.
- Scanner : 0 alerte. Phrase « Ce n'est pas un ordre... pas une instruction directe » : narrative,
  rien à appliquer.

## Résolution
1. Morse extrait automatiquement (composantes connexes, largeur 4 px = point, 8-9 px = trait ;
   écarts 3-7 intra-lettre, 13-17 entre lettres, 35-37 entre mots) :
   `DIRH FO PFFWFFFEQG JIG CCH FWXR NQKMIS YSYR LRGWC RVUYX FVZJG`
2. Vigenère, clé RENO, clé continue sur les lettres (espaces ignorés) :
   **`MEET OK CROSSROADS SET OLD SIGN ACTIVE HOLD UNTIL NIGHT SHIFT`**
   (clé redémarrée à chaque mot -> charabia dès le 3e mot : la clé continue est la bonne).

## Vérifications
- Lecture Morse vérifiée visuellement sur crops agrandis (lignes 1-2) ; toutes les séquences
  sont des lettres valides ; aucun autre signe sur la page (3 taches de papier seulement), LSB ~0.5.
- Le texte clair est entièrement en anglais lisible -> clé et méthode confirmées.
- « OK » est bien chiffré `FO` = `..-. ---` (vérifié au zoom), donc ce n'est pas une erreur de lecture
  (« AT » donnerait `RX`).

## Variantes (format non spécifié)
1. `MEET OK CROSSROADS SET OLD SIGN ACTIVE HOLD UNTIL NIGHT SHIFT` (message complet, espaces)
2. `MEETOKCROSSROADSSETOLDSIGNACTIVEHOLDUNTILNIGHTSHIFT` (sans espaces)
3. Contexte historique (hors données) : 1re attaque de train du gang Reno, 6 oct. 1866 près de
   Seymour (Indiana) — seulement si la plateforme attend un lieu/date ; rien dans les données ne le donne.
- Aucun acrostiche trouvé (initiales MOCSOSAHUNS, finales TKSTDNEDLTT).

## Pièges
- Le mot-clé n'est pas « Jesse James » ni un nom de journal : c'est le surnom RENO (gang Reno).
- Malus possible : demander le format à l'humain / un essai sur la variante 1 en premier.
