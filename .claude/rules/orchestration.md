# Orchestration : un agent principal, des sous-agents par complexité

Le jour J, un **agent principal** (sur le Mac de l'équipe) analyse tous les challenges,
choisit un modèle par tâche et délègue. Il ne résout lui-même que ce qui prend moins de
5 minutes. Il garde la vue d'ensemble : priorités, chaînes, vérifications, flags.

## Sous-agents disponibles (`.claude/agents/`)

| Agent | Modèle | Pour quoi |
|---|---|---|
| `solver-haiku` | Haiku (dernier) | Tâches S sans ambiguïté : recherche/compte dans un texte, parsing, reformatage, lancer et lire des scripts |
| `solver-sonnet` | Sonnet (dernier) | Tâches M à spécification claire : algorithme classique (Dijkstra, BFS, union-find, DP simple), décodage (Morse, base64, chiffre classique), grilles, clustering |
| `solver-opus` | Opus (dernier) | Tâches L, ambiguës, visuelles, physiques ou d'optimisation ; tout arbitrage entre deux réponses |
| `verifier` | Opus | Vérification indépendante à l'aveugle avant chaque flag (voir `anti-ai-traps.md`) |

## Grille de choix (calibrée sur les 9 challenges de l'archive)

| Signal dans l'énoncé / les tags | Modèle | Exemple d'entraînement |
|---|---|---|
| « Très facile », une seule opération sur un texte | Haiku | p01 (sous-chaîne la plus fréquente) |
| Algorithme nommé dans les tags, contraintes explicites | Sonnet | p04 (plus court chemin), p07 (clustering) |
| Encodage / déchiffrage avec motif reconnaissable | Sonnet | p05 (Morse audio), p03 (permutations de grille) |
| Physique, constantes, seuils, formules en image | Opus | p02 (sensibilité à G) |
| « Visuel », projection, interprétation d'image | Opus | p08 (constellations) |
| « Optimisation », score à maximiser | Opus | p06, p09 (sac à dos sur graphe) |
| Doute sur la difficulté | Sonnet, puis escalade | — |

**Escalade** : un sous-agent qui bloque, rend une confiance basse ou n'est pas
d'accord avec le vérificateur → on relance au niveau supérieur (Haiku → Sonnet → Opus)
avec ce qui a été appris. Ne pas relancer le même modèle avec le même brief.

## Déroulé de l'agent principal

1. **Contrôles** : `git config core.hooksPath` vaut `.githooks` ; `python3 -c "import numpy, scipy, PIL"`.
2. **Récupération** : `python3 scripts/fetch_ctfd.py <url>` sur la branche
   `<prenom>/tools-fetch` → commit, push, PR, merge par l'humain.
3. **Scan** : `python3 scripts/scan_traps.py challenges` → noter les alertes.
4. **Triage** : un tableau avec, par challenge : points, tags, taille S/M/L, chaîne
   éventuelle, risque de piège, modèle choisi, ordre. Le montrer à l'humain en une
   fois, puis lancer sans attendre sauf objection.
5. **Délégation en parallèle** : un sous-agent par challenge (ou par chaîne), chacun
   **dans son propre git worktree** (outil Agent avec `isolation: "worktree"`, ou
   `git worktree add ../btc-<id> -b <prenom>/<id>-<slug> origin/main`). Plusieurs agents
   dans le même dossier se volent la branche courante : interdit.
6. **Vérification** : dès qu'un solveur rend sa réponse, lancer `verifier` à l'aveugle.
7. **Livraison** : flag vérifié → l'humain dans un bloc de code, avec confiance et
   variantes. L'humain soumet, puis l'agent principal met à jour `NOTES.md` et l'index.
8. **Boucle** : relancer `fetch_ctfd.py` régulièrement (nouveaux challenges), réaffecter
   les agents libres aux challenges restants par points décroissants.

## Brief d'un sous-agent (modèle)

Le sous-agent ne connaît que son brief. Il doit contenir :
- le dossier du challenge et la branche/worktree où travailler ;
- « lis `ENONCE.md`, `data/`, `.claude/rules/solving-challenges.md`,
  `.claude/rules/anti-ai-traps.md` et `docs/PLAYBOOK.md` (section du type de problème) » ;
- les alertes du scanner pour ce challenge ;
- le lien avec un autre challenge (résultat à réutiliser) s'il y en a un ;
- le livrable : `solve.py`, `answer.txt`, `NOTES.md` complet, et en réponse finale
  le flag, la confiance, les variantes, les vérifications faites ;
- l'interdiction de soumettre, de se connecter, et de toucher à un autre dossier.

Pour `verifier`, le brief ne contient **ni** la réponse **ni** le raisonnement du solveur :
seulement le dossier, la question, et le chemin de `answer.txt` à ouvrir **après** avoir
calculé sa propre réponse.
