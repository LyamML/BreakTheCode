# Workflow git — éviter les conflits à 3 personnes + 3 agents

## Au démarrage de TOUTE tâche qui modifie des fichiers

Avant d'écrire la moindre ligne :

```bash
git fetch origin
git switch -c <prenom>/<id>-<slug> origin/main   # ex: lyam/c03-labyrinthe
```

- `<prenom>` : `lyam`, `kevin` ou `antho` (voir le tableau Équipe de CLAUDE.md).
- `<id>` : le préfixe du dossier créé par `fetch_ctfd.py` (`c01`, `c12`) ; pour un
  entraînement `p01`… ; pour de l'outillage partagé `tools`.
- Pour une chaîne de challenges tenue par une seule personne : une branche par
  challenge quand même (`lyam/c05-message`, puis `lyam/c04-planete` depuis la première
  si elle a besoin de son résultat).
- `<slug>` : 1 à 3 mots en kebab-case, sans accents.
- Si la branche existe déjà (reprise de travail) : `git switch <branche>` puis
  `git pull --rebase`.
- Si tu es déjà sur une branche qui n'est pas `main` et qui correspond à la tâche,
  reste dessus.

Si `origin/main` n'existe pas encore (repo vide), crée la branche depuis l'état local.

## Périmètre de chaque branche

- Une branche ne modifie **que** `challenges/<son-dossier>/` (ou `practice/<son-dossier>/`).
- Fichiers partagés — `CLAUDE.md`, `.claude/`, `docs/`, `scripts/`, `.githooks/` :
  uniquement dans une branche `<prenom>/tools-<slug>`, courte, mergée vite.
- `challenges/INDEX.md` et `practice/INDEX.md` sont **générés** : ne pas les éditer à
  la main, lancer `python3 scripts/build_index.py`. En cas de conflit dessus : prendre
  n'importe quelle version puis relancer le script.
- Les fichiers de `data/` lourds (audio, > 20 Mo) ne sont pas commités (voir
  `.gitignore`) : chacun les récupère avec `fetch_ctfd.py`.

## Commits

- Petits et fréquents, message en français à l'impératif :
  `c03: solution BFS, passe les 4 exemples`.
- Jamais `git add -A` à l'aveugle : vérifier `git status` d'abord.
- Jamais `--no-verify` : les hooks sont là pour protéger `main` et l'attribution.

## Intégrer son travail

```bash
git push -u origin <branche>
gh pr create --fill --base main
```

Merge par l'humain (squash). Pas de force-push sur une branche qu'un autre utilise.
Ne jamais merger, rebase ou push sur `main` directement.

## Récupérer le travail des autres

`git fetch origin && git rebase origin/main` sur sa branche. En cas de conflit hors
de son dossier : s'arrêter et demander à l'humain.
