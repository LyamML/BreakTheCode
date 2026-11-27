# Stratégie pour finir N°1

## Ce qui rapporte des points

- Scoring CTFd **dynamique, décroissance logarithmique** : les points d'un challenge
  baissent à chaque équipe qui le valide. Valider tôt un challenge que tout le monde
  résoudra vaut beaucoup ; valider seul un challenge difficile vaut encore plus.
- Les points affichés sont les points **actuels**. Un challenge à forte valeur et peu
  de résolutions = peu d'équipes l'ont eu = grosse opportunité.
- Sur les challenges d'**optimisation** (score calculé sur la réponse), le classement se
  joue sur la qualité : viser l'optimum prouvé, pas une solution valide.
- Les challenges `bonusmalus` ont un champ `bonus` (probablement pour les premiers à
  valider) et un `malus` par mauvaise réponse. En 2026, l'équipe 1re avait validé 4 ou 5
  challenges, avec ces bonus, pendant qu'on installait encore l'orchestration.

## Les 10 premières minutes

1. **Chacun sur sa machine, sans attendre personne** (aucune PR avant le premier flag) :
   `python3 scripts/recon_ctfd.py <url> --every 300` en arrière-plan, puis
   `python3 scripts/fetch_ctfd.py <url>`. Le recon donne le triage (points, bonus, malus,
   temps restant) et tout ce qui est caché dans les pages HTML du site.
2. **Les S tout de suite** : l'agent de chacun résout directement les challenges courts
   à une seule interprétation, pendant que les autres lisent les énoncés.
3. Chaque agent lit **tous** les `ENONCE.md` (titre, tags, points, fichiers) et le
   `RAPPORT.md` du recon, et estime pour chacun : durée (S < 15 min, M < 45 min,
   L > 45 min), technique, risque.
4. L'humain répartit. Règle par défaut :
   - **Les rapides d'abord, en parallèle** : chaque personne prend 1 à 2 challenges S
     pour encaisser les points pendant qu'ils sont hauts.
   - **Les chaînes à une seule personne** (ex. décoder un message → l'utiliser dans un
     plus court chemin) : un seul propriétaire pour toute la chaîne.
   - **Les L / optimisation** à la personne la plus à l'aise, lancés tôt pour laisser
     tourner les solveurs.
5. Noter la répartition dans `NOTES.md` de chaque challenge (`owner`, `status: todo`)
   et régénérer le tableau (`python3 scripts/build_index.py`).

## Pendant l'event

- **Recon toutes les 5 min** : lire les lignes `NOUVEAU` du recon (page modifiée, image
  ajoutée, nouvelle notification) et les rattacher à un challenge.
- **Coupe-circuit 20 min** : sans progrès net après 20 min sur un S/M, le dire à l'humain
  (ce qui est compris, ce qui bloque, 2 pistes) et proposer de basculer.
- **Ambiguïté d'énoncé** : calculer la réponse pour chaque interprétation plausible,
  les classer par vraisemblance, et donner ce classement à l'humain avant toute
  soumission. Ne jamais trancher en silence.
- **Essais limités** : lire `Essais max` dans `ENONCE.md`. Si l'essai est unique ou
  l'énoncé parle d'un seul essai : double vérification (deux méthodes indépendantes)
  obligatoire avant de proposer le flag.
- **Format du flag** : copier le format de l'exemple au caractère près (séparateurs,
  espaces, majuscules, accents, unités, signes, nombre de décimales). Donner à
  l'humain le flag dans un bloc de code prêt à copier.
- **Indices CTFd** : peuvent coûter des points. Jamais débloqués sans l'humain.
- **Partager les pièges tout de suite** : un piège trouvé → une ligne dans
  `docs/PLAYBOOK.md` via une mini PR `tools-*`, et prévenir l'humain pour qu'il passe
  le mot aux deux autres.

## Après une soumission

- Validée : `status: submitted`, flag dans `answer`, push.
- Refusée : `status: failed`, noter la réponse refusée et l'hypothèse fausse dans
  `NOTES.md` (« Ce qui n'a pas marché »), puis repartir de l'énoncé, pas du code.
