---
owner: lyam
status: solved
points: "47"
tags: "Facile, Audio, Encodage"
answer: "Cerosarae"
confidence: haute
---

# Notes — p05 Un message codé (47 pts)

## Réponse

Flag à soumettre (copier-coller exact) :

```
Cerosarae
```

Variante de casse si refusé : `CEROSARAE` (le Morse n'a pas de casse ; `Cerosarae` est
l'orthographe exacte du nœud dans `planets_graph.json` de p04 et suit l'exemple `Mars`).

Message complet décodé (sauvé dans `message.txt` par `solve.py`) :

> NOUS SOMMES ARRIVÉ SUR LA PLANÈTE CEROSARAE, ELLE SEMBLE HABITABLE ET PROPICE À LA VIE
> POUR CONSTRUIRE UNE NOUVELLE CIVILISATION. LES PLANÈTES VEGAELUS ET ZORAORARA SONT À
> ÉVITER ABSOLUMENT, IL Y A UN CHAMP D'ASTÉROIDES AUTOUR DE CES DEUX PLANÈTES. IL FAUT
> PASSER PAR LA PLANÈTE PHOSUNION PUIS NEPTANOS AFIN D'ÉVITER L'ATTRACTION D'UN TROU NOIR.
> AFIN DE RAVITAILLER EN VIVRE, VOUS POUVEZ ALLER SUR TARAISIS QUI EST UNE AUTRE PLANÈTE
> HABITABLE ET RICHE EN ALIMENT COMESTIBLE EN TOUT GENRE.

**Ce message est l'entrée de p04** (contraintes d'itinéraire) : challenge enchaîné.

## Interprétation de l'énoncé

- « Le nom de la planète d'où provient le message » = la planète où l'équipe est arrivée
  (« NOUS SOMMES ARRIVÉ SUR LA PLANÈTE CEROSARAE »). Pas d'ambiguïté réelle : c'est la
  seule planète présentée comme point d'arrivée. Taraisis est aussi « habitable » mais
  citée comme ravitaillement optionnel — piège potentiel, à ne pas soumettre.

## Approche

1. `wave` + numpy : 44,1 kHz, mono, 16 bits, 6 min. Enveloppe d'amplitude par fenêtres
   de 10 ms → signal tout-ou-rien parfait (silences = 0 exact).
2. FFT : une seule porteuse à **800 Hz** → Morse classique (CW).
3. Histogramme des durées : bips 100 ms / 300 ms (point / trait) ; silences 100 / 200 /
   300 / 400 ms.
4. Décodage avec table Morse **étendue** (accents français).

## Ce qui a marché

- Commencer par l'histogramme des longueurs de plages on/off : en 1 commande on voit
  l'unité (100 ms) et toute la grammaire du signal. Pas besoin de regarder le spectrogramme.
- Décodeur générique (`solve.py`) : unité auto-détectée, seuil relatif, gère mono/stéréo
  et 8/16/32 bits → réutilisable tel quel le jour J sur tout .wav Morse.

## Ce qui n'a pas marché / pièges

- **Espacements non standard** : intra-lettre 1u, lettre **2u** (au lieu de 3), mot
  **4u** (au lieu de 7), et **3u** = fin de phrase (2 occurrences). Un décodeur avec les
  seuils standards (3u/7u) fusionne les mots. → Toujours calibrer sur l'histogramme.
- **Morse étendu** : `..-..`=É, `.-..-`=È, `.--.-`=À. Une table de base affiche
  `[..-..]` : ne pas paniquer, c'est un accent.
- 35 % de l'énergie spectrale hors 700-900 Hz : ce sont les bandes latérales dues aux
  fronts raides du tout-ou-rien, **pas** un second message caché (vérifié : les silences
  valent exactement 0, aucun autre pic que 800 Hz).

## Vérifications faites

- Texte décodé 100 % lisible en français, aucun symbole inconnu après la table étendue.
- Deux seuils de mot testés (3u et 4u) → même texte, seule la ponctuation change.
- Planète cherchée dans le graphe de p04 : `Cerosarae` existe (orthographe exacte),
  ainsi que Vegaelus, Zoraorara, Phosunion, Neptanos, Taraisis.
- Pas de contenu caché : pic unique 800 Hz, silences à 0.

## Temps / difficulté réelle

~5 min. Facile si on pense « Morse » tout de suite (tag « Audio, Encodage » + son
bip-bip). Fichier lourd (31 Mo) mais traitement < 1 s avec numpy.

## Leçons pour le jour J

1. **Audio → regarder d'abord l'enveloppe et l'histogramme des durées**, puis la FFT.
   Tout-ou-rien + une fréquence = Morse ; plusieurs fréquences = DTMF/FSK ; signal
   continu complexe = voix (inverser/ralentir) ou image dans le spectrogramme (SSTV).
2. **Lire le message en entier** : il contenait les contraintes d'un autre challenge
   (p04). Le noter immédiatement pour la personne qui le traite.
3. Réutiliser `practice/p05-message-code/solve.py` (décodeur Morse prêt à l'emploi).

## Journal

| Heure | Action | Résultat |
|---|---|---|
| 18:50 | Enveloppe 10 ms + histogramme | Morse 800 Hz, unité 100 ms |
| 18:52 | Décodage table de base | Texte lisible, 3 symboles inconnus |
| 18:53 | Table étendue | É/È/À résolus, message complet |
| 18:55 | Contrôle FFT / silences | Rien de caché |
