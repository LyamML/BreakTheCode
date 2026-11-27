# Bilan final — Break the Code 2026 (26/11/2026)

Équipe **SENDAI** (Lyam, Kevin, Antho), EPSI Rennes. 35 équipes classées.

## Classement

Relevé sur le CTFd après la clôture :

| Rang | Équipe | Points |
|---|---|---|
| 1 | Normale Surchauffe | 335 |
| 2 | SaladeTomateOignon2 | 295 |
| 3 | sudo | 290 |
| 4 | Recours gracieux | 289 |
| **5** | **SENDAI** | **287** |
| 6 | RENNUET | 273 |
| 7 | MILO | 264 |

Le classement public était gelé à 21h20 (heure de Paris). La page de l'équipe affiche
308 points, sans doute à cause de soumissions après le gel. **c20 (classement, correction
manuelle) n'était pas encore compté** : il peut encore changer le rang final.

Sur l'event, l'équipe a eu **10 réponses refusées** (malus des challenges bonusmalus).

## Challenges

| Challenge | Points | Résultat | Flag / note |
|---|---|---|---|
| c15 La mine des Dalton | 39 | ✅ validé | `4` |
| c16 Le Duel Truqué | 21 | ✅ validé | `BANDIT` |
| c17 L'opérateur fantôme | 26 | ❌ non trouvé | Hybride : image invisible dans la page HTML du scoreboard, puis chuchoter « Où aura lieu la fête » à un orga avec une étoile de shérif |
| c18 Pony Express | 23 | ✅ validé | voir `challenges/c18-pony-express/answer.txt` |
| c19 Artefact – Second message | 17 | ❌ refusé | `ANNAPOLIS`, `NANNAPOLIS`, `8`, `87` refusés |
| c20 Tournée des saloons | 60 | ⏳ correction manuelle | 19 arrêts en 4 h 08 |
| c21 Visite surprise | 17 | ✅ validé | `26` |
| c22 Attaque du train | 39 | ❌ refusé | Déchiffré `MEET OK CROSSROADS SET OLD SIGN ACTIVE HOLD UNTIL NIGHT SHIFT` ; la phrase entière et `SEYMOUR` refusés : format du flag non trouvé |
| c23 Avis de recherche | 33 | ✅ validé | `LLIAM` (affiches de la salle, n°5) |
| c24 Concours de tir : feu ! | 33 | ✅ validé | `226` |
| c25 Trip from Seattle | 28 | ✅ validé | `WWWEST` |
| c26 Artefact – Premier message | 47 | ✅ validé | `GLOOSCAP` |
| c27 Concours de tir : After party | 29 | ✅ validé | `Abraham Lincoln` |
| c28 L'attaque de la diligence | 53 | ✅ validé | voir `challenges/c28-attaque-diligence/answer.txt` |

Les 10 validations sont toutes au nom du compte de Kevin (19h26–19h50, heure UTC).
Détails de chaque challenge : `challenges/cNN-*/NOTES.md`.

## Ce qu'on retient

- Les 9 challenges « algorithmiques » ont été validés en 25 min : l'outillage
  (fetch, solveurs, vérification) a fonctionné.
- Les points perdus viennent de la **mise en route** (trop d'étapes avant le premier
  flag), du **site lu seulement via l'API** (c17 : l'indice était dans la page HTML du
  scoreboard), de la **salle** (c17, c23) et du **format du flag** (c19, c22 : réponse
  déchiffrée mais refusée).
- Leçons détaillées : `docs/PLAYBOOK.md`, section 6.
