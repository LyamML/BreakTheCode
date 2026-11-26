# État des challenges — 26/11/2026, ~20h35 (Kevin)

Statuts CTFd relevés dans la session de Kevin (gel du classement à 21h20).
Dernier relevé : **3e avec ~295 points** (1er 335, 2e 305).

## ✅ Validés sur CTFd (10)

| Challenge | Flag accepté |
|---|---|
| c15 La mine des Dalton | `4` |
| c16 Le Duel Truqué | `BANDIT` |
| c18 Pony Express | voir `challenges/c18-pony-express/answer.txt` |
| c21 Visite surprise | `26` |
| c23 Avis de recherche | `LLIAM` — **nouveau** (l'« Homme en noir », n°5 ; résolu avec les affiches de la salle) |
| c24 Concours de tir : feu ! | `226` |
| c25 Trip from Seattle | `WWWEST` |
| c26 Artefact – Premier message | `GLOOSCAP` |
| c27 Concours de tir : After party | `Abraham Lincoln` |
| c28 L'attaque de la diligence | voir `challenges/c28-attaque-diligence/answer.txt` |

## ⏳ Soumis, en attente

- **c20 Tournée des saloons** (60 pts, classement) : soumis avec 19 arrêts en 4 h 08,
  correction manuelle. Une 2e version **sans piste réutilisée** est en calcul pour couvrir
  le cas où les juges l'interdiraient.

## ❌ Ce qui nous manque

### c17 — L'opérateur fantôme (26 pts) — rien trouvé, 1 seule équipe l'a
- Réponse : un **nom de rue sans déterminant** (format « rue du saloon »).
- Pas de fichier. Le fichier caché `/files/media/indice_operateur_fantome.txt` dit seulement
  « bien essayé… vous êtes sur la bonne voie » → il faut chercher des éléments cachés.
- Déjà vérifié sans résultat : code HTML des pages, en-têtes HTTP, plugins, notifications,
  `robots.txt`, flux d'événements, logo/favicon, liste des équipes.
- Pistes : **dans la salle** (message en points et traits, panneau ou plan avec un nom de
  rue, écran qui tourne en boucle), **noms des réseaux Wi-Fi** visibles dans la salle.

### c22 — Attaque du train (39 pts) — en pause, personne ne l'a
- Message déchiffré (Morse puis Vigenère, clé RENO) :
  `MEET OK CROSSROADS SET OLD SIGN ACTIVE HOLD UNTIL NIGHT SHIFT`.
- **Refusés** : la phrase entière, `SEYMOUR`. C'est le format du flag qui manque.

### c19 — Artefact – Second message (17 pts) — en pause
- Ligne 7 : `NANNAPOLIS` (décalage −8) ou `nannapolis` (décalage +24).
- **Refusés** : `ANNAPOLIS`, `NANNAPOLIS`, `8`, `87`. Chaque essai coûte un malus.
- Meilleure piste : `annapolis` en minuscules, puis `nannapolis`.

Les solutions (`solve.py`, `NOTES.md`, `answer.txt`) sont dans `challenges/cNN-*/`.
