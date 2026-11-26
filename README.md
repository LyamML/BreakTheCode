# Break the Code 2026

Repo de l'équipe Lyam / Kevin / Antho (SENDAI, EPSI Rennes) pour l'event Sopra Steria
Break the Code 2026.

## Résultat (26/11/2026)

**5e sur 35 équipes, 287 points** au classement gelé : 10 challenges validés sur 14.
c20 (Tournée des saloons) était encore en correction manuelle à la clôture. Ce résultat
peut donc encore changer.

| | |
|---|---|
| Validés | c15, c16, c18, c21, c23, c24, c25, c26, c27, c28 |
| Refusés (format du flag) | c19, c22 |
| Non trouvé | c17 (se résolvait dans la salle) |
| En attente | c20 (optimisation, correction manuelle) |

Bilan complet : [docs/ETAT.md](docs/ETAT.md). Leçons : [docs/PLAYBOOK.md](docs/PLAYBOOK.md), section 6.

## Utiliser le repo

L'objectif était **la 1re place**. Les instructions pour Claude Code sont dans
[CLAUDE.md](CLAUDE.md), [.claude/rules/](.claude/rules/) et [.claude/agents/](.claude/agents/).

## Installation — macOS / Linux (machine de l'agent principal)

```bash
git clone https://github.com/LyamML/BreakTheCode.git && cd BreakTheCode
git config core.hooksPath .githooks
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

`python3 -m venv` évite l'erreur « externally-managed-environment » du Python Homebrew.
Penser à `source .venv/bin/activate` dans chaque nouveau terminal (ou lancer Claude Code
depuis un terminal où le venv est actif).

## Installation — Windows

```powershell
git clone https://github.com/LyamML/BreakTheCode.git; cd BreakTheCode
```

```powershell
git config core.hooksPath .githooks
```

```powershell
python -m pip install -r requirements.txt
```

Sous Windows, remplacer `python3` par `python` dans les commandes du repo. Si une
bibliothèque échoue avec « Une stratégie de contrôle d'application a bloqué ce
fichier », c'est Windows qui bloque une DLL : passer par numpy pur.

## Réglage Claude Code (chacun, une fois)

Ajouter dans `.claude/settings.local.json` (non versionné) ou dans les réglages
utilisateur de Claude Code, pour qu'il n'ajoute aucune attribution :

```json
{
  "attribution": { "commit": "", "pr": "" },
  "includeCoAuthoredBy": false
}
```

Puis compléter sa ligne dans le tableau « Équipe » de [CLAUDE.md](CLAUDE.md).

## Jour J

```bash
python3 scripts/fetch_ctfd.py https://<url-de-la-plateforme>   # énoncés + fichiers
python3 scripts/scan_traps.py challenges                       # pièges pour IA
python3 scripts/build_index.py                                 # tableau de bord
```

- Tableau de bord : [challenges/INDEX.md](challenges/INDEX.md)
- Entraînement résolu et commenté : [practice/INDEX.md](practice/INDEX.md)
- Retours d'expérience : [docs/PLAYBOOK.md](docs/PLAYBOOK.md)
