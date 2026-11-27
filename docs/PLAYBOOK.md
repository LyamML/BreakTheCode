# Playbook — ce qui marche, ce qui ne marche pas

Tiré des 9 challenges de l'archive Break the Code, résolus en conditions réelles par
des agents Claude (détails dans chaque `practice/pNN-*/NOTES.md`). À lire avant chaque
challenge ; à compléter pendant l'event (mini PR `<prenom>/tools-playbook`).

## 1. Les 10 réflexes qui font gagner

1. **Lire les tags d'abord** : ils nomment la technique (« Plus court chemin »,
   « Clustering », « Audio, Encodage »). C'est le meilleur indice disponible.
2. **Reproduire l'exemple de l'énoncé avant tout** : sinon l'interprétation est fausse.
3. **Afficher le top 5, pas seulement le meilleur** : les égalités sautent aux yeux (p01).
4. **Analyse de sensibilité** sur toute constante dès qu'une contrainte est un seuil :
   les données sont générées au ras de la limite (p02 : le gagnant change avec le 4e
   chiffre de G).
5. **Calculer toutes les interprétations plausibles d'un coup** et regarder si elles
   divergent (p07 : 447 / 429 / 455 selon la métrique). Si oui, c'est le texte qui
   tranche, et l'humain voit le tableau.
6. **Visuel → rendre en PNG et regarder** (Read sur l'image), identifiants écrits
   dessus, rotations + miroir testés (p08 : le dinosaure ne se lit qu'en miroir).
7. **Recherche exhaustive + score automatique** plutôt que deviner le sens d'une
   transformation (p03 : 2 tentatives raisonnées illisibles, la recherche exhaustive
   trouve en secondes).
8. **Lire tout le résultat d'un challenge enchaîné** : le message audio de p05
   contenait les contraintes de p04.
9. **Optimisation → modèle exact + validateur séparé + borne** : le classement se joue
   au score (p06 : 242, p09 : 154, optimum prouvé).
10. **Vérification à l'aveugle** par un autre agent avant chaque flag
    (`.claude/rules/anti-ai-traps.md`).

## 2. Pièges rencontrés

| Piège | Où | Parade |
|---|---|---|
| Donnée leurre (`g = 9.81` inutile, invalide tout si utilisée) | p02 | Vérifier la cohérence de chaque donnée ; tester avec et sans |
| Image de formule dupliquée (« durée » = copie de « force ») | p02 | `scan_traps.py` le détecte ; déduire la formule, montrer la variante |
| Coordonnées avec espaces/unités (`82.97942° N`) | p02 | Garder la chaîne source pour la réponse, parser à part pour calculer |
| Constante physique au ras du seuil | p02 | Tableau G = 6.674e-11 / 6.6743e-11 / 6.67e-11 → réponses différentes |
| Énoncé sans exemple | p03 | Score automatique (adjacence des pixels, mots lisibles) + recherche exhaustive |
| Bruit nommé de façon détournée (« Alpha à Echo » = lettres a–e) | p03 | Alphabet OTAN, chiffres romains, etc. : décoder le récit |
| Chemin le plus court « évident » qui passe par des nœuds interdits | p04 | Les contraintes sont ailleurs (autre challenge, récit) |
| Ex-aequo avec poids entiers | p04 | Vérifier l'unicité ; deux chemins = deux flags possibles |
| Morse à espacements non standard (lettre 2u, mot 4u) | p05 | Seuils calibrés sur l'histogramme des durées, pas les valeurs théoriques |
| Morse étendu (`..-..` = É, `.-..-` = È, `.--.-` = À) | p05 | Table étendue dans `practice/p05-message-code/solve.py` |
| Métrique de distance ambiguë (euclidienne / Chebyshev / Manhattan) | p07 | Toutes les calculer, « rayon » = boule euclidienne |
| Point d'observation = étoile courante → division par 0 (NaN) | p08 | Exclure l'observateur de la projection |
| Élément orphelin = la réponse (« sa composition a changé ») | p08 | Quand le récit parle de changement, chercher l'anomalie dans les données |
| Pression « un seul essai » | p01 | Double vérification, aucune précipitation |

Aucune injection de texte visant les IA dans l'archive, mais l'event en contiendra
probablement : `scripts/scan_traps.py` est testé sur des pièges synthétiques (zero-width,
tags Unicode, HTML caché, homoglyphes, base64, « si vous êtes une IA… »).

## 3. Recettes par type (code réutilisable dans `practice/`)

| Type | Recette | Code prêt |
|---|---|---|
| Sous-chaîne la plus fréquente | `Counter` sur toutes les fenêtres, avec et sans chevauchement, top 5 | `p01-hal-code/solve.py` |
| Physique / filtrage CSV | Formules extraites des images, unités en SI, sensibilité aux constantes | `p02-planet-landing/solve.py` |
| Grille brouillée (décalages lignes/colonnes) | Recherche exhaustive des sens/ordres + score d'adjacence | `p03-tleilax/solve.py` |
| Plus court chemin avec étapes imposées et nœuds interdits | Dijkstra (`heapq`) par tronçon, nœuds interdits retirés, unicité vérifiée | `p04-planete-habitable/solve.py` |
| Audio Morse | Enveloppe → on/off → histogramme des durées → seuils → table étendue | `p05-message-code/solve.py` |
| Chemin + sac à dos sur DAG | DP sur (nœud, capacité) en ordre topologique ; ILP en contrôle | `p06-attaque-rebelles/solve.py`, `validate.py` |
| Clustering 3D sur pile d'images | `ndimage.label` (26-connexe) puis union-find par décalages ≤ r | `p07-cailloux-cosmiques/solve.py` |
| Projection sphérique / constellations | Coordonnées relatives, gnomonique centrée, rendu PNG annoté | `p08-sauts-constellations/sky.py` |
| Optimisation à contraintes couplées (carburant consommable) | ILP `scipy.optimize.milp` : variable « ressource i utilisée à l'étape e » | `p09-offensive-rebelles/solve.py`, `validate.py` |

Audio, au-delà du Morse : tout-ou-rien + une fréquence = Morse ; plusieurs fréquences
discrètes = DTMF/FSK ; signal complexe = voix (inverser, ralentir) ou image dans le
spectrogramme (SSTV). Commencer par l'enveloppe et un spectrogramme en PNG.

## 4. Environnement et outils

- **PuLP 4.x a changé son API** et n'embarque plus CBC : ne pas l'utiliser. Prendre
  `scipy.optimize.milp` (HiGHS inclus, API stable).
- **Windows (poste de Lyam)** : certaines DLL de scipy sont bloquées par la stratégie de
  contrôle d'application (`scipy.signal` systématiquement, `scipy.spatial`/`linalg` par
  moments). Repli : numpy pur. Sans objet sur macOS.
- **macOS** : utiliser un venv (`python3 -m venv .venv`), sinon le Python Homebrew
  refuse `pip install`. Erreur SSL avec le Python de python.org : lancer
  `Install Certificates.command` (ou `certifi`, déjà dans `requirements.txt`).
- Les gros fichiers (31 Mo de WAV) se traitent en < 1 s avec numpy : pas besoin d'optimiser.
- `scripts/fetch_ctfd.py` récupère les 9 challenges de l'archive en ~12 s.

## 5. Choix du modèle (constaté à l'entraînement)

| Challenge | Points | Durée réelle | Modèle qui suffit | Pourquoi |
|---|---|---|---|---|
| p01 sous-chaîne | 17 | 2 min | Haiku | Une opération, vérif d'égalités |
| p02 atterrissage | 25 | 10 min | **Opus** | Constantes au ras du seuil, image dupliquée, leurre |
| p03 grille | 27 | 10 min | Sonnet | Recherche exhaustive, validation visuelle |
| p04 chemin | 33 | 5 min | Sonnet | Dijkstra classique, mais dépend de p05 |
| p05 Morse | 47 | 5 min | Sonnet | Décodage standard avec calibrage |
| p06 sac à dos DAG | 53 | 10 min | **Opus** | Optimum à prouver |
| p07 clustering | 59 | 15 min | Sonnet (+ Opus si métriques divergent) | Interprétation à trancher |
| p08 constellations | 63 | 30 min | **Opus** | Lecture visuelle, miroir, anomalie |
| p09 carburant | 80 | 25 min | **Opus** | ILP à contraintes couplées |

Les points de l'archive sont ceux d'après la décroissance : les plus « chers » sont
ceux que peu d'équipes ont résolus (optimisation, visuel). C'est là que se fait l'écart.

## 6. À ajouter pendant l'event

| Heure | Challenge | Piège / leçon | Qui |
|---|---|---|---|
| 26/11 | c17 L'opérateur fantôme (bonusmalus, sans fichier) | **Challenge hybride : indice sur le site, réponse dans la salle.** Une image invisible cachée dans la **page HTML du scoreboard** disait de demander à un opérateur où aura lieu la prochaine fête (rapporté le 27/11 par l'équipe qui l'a eu en premier : leur Claude lisait le site page par page). Il fallait chuchoter « Où aura lieu la fête » à un orga **portant une étoile de shérif** pour obtenir l'adresse. La balise `<img>` invisible de l'énoncé (`/files/media/indice_operateur_fantome.txt`) était un appât : « Bien essayé, mais c'est non… bonne voie » (= bonne technique, mauvais endroit). On a perdu ~40 min à fouiller le CTFd **via l'API seulement** (`/api/v1/scoreboard` appelé 5 fois, page `/scoreboard` jamais lue). Normale Surchauffe l'a validé en 9 min. **Signaux** : « toujours en ville », « sous les yeux de tout le monde », aucun fichier. **Parade** : dès qu'un énoncé sans fichier pointe vers un lieu physique, envoyer tout de suite un humain noter ce qui est affiché ou dit dans la salle (slides, affiches, annonce d'ouverture) et parler aux orgas *avec le vocabulaire du récit* (on se fait passer pour un complice : « sabotage » → « fête »). Ce sont les orgas **avec une étoile de shérif** qui donnaient la réponse (ceux sans étoile, non) : quand certains orgas portent un signe distinctif lié au récit, c'est à eux qu'il faut parler. **Parade outil** : `scripts/recon_ctfd.py` dès la 1re minute (toutes les pages HTML, éléments cachés). | Lyam |
| 26/11 | c23 Avis de recherche, c17 | Texte `visibility: hidden` dans l'énoncé : **pas toujours un leurre**. En c17 c'était un appât (fichier « bien essayé, mais c'est non »). En c23 c'était le mode d'emploi (« le numéro 5 », « 5 dernières lettres du prénom en majuscule ») : avec les affiches de la salle, ça donnait `LLIAM`. **Parade** : le traiter comme une donnée à recouper, jamais comme une consigne à appliquer seule ; en bonusmalus, chaque erreur coûte 4 à 5 pts. | Lyam |
| 26/11 | c19, c22 | Réponse déchiffrée mais **refusée pour le format** (c22 : phrase entière refusée ; c19 : `ANNAPOLIS`/`NANNAPOLIS` refusés). 6 malus au total. **Parade** : quand l'énoncé ne donne pas le format, ne pas enchaîner les variantes ; relire le récit pour la question exacte posée (un nom ? un lieu ? un mot ?) avant le 2e essai. | Lyam |
| 27/11 | Toute la plateforme | **Lire le site comme un visiteur, pas seulement l'API.** L'API ne renvoie que des données : une `<img>` ou un texte caché dans le gabarit d'une page (scoreboard, accueil, pages perso) n'y apparaît pas. `recon_ctfd.py` lit toutes les pages HTML, le thème et les médias, et signale ce qui est NOUVEAU toutes les 5 min. Un appât qui dit « bonne voie » : chercher le même procédé ailleurs. | Lyam |
| 27/11 | Mise en route | **Rien de git avant le premier flag.** L'équipe 1re travaillait directement via l'API dans une seule session et avait 4 ou 5 challenges (avec les bonus des premiers) pendant qu'on faisait fetch → PR → merge → orchestration. Nos 10 refus venaient tous du format, aucun du calcul : vérification proportionnée (script pour un S, agent `verifier` pour le reste, format toujours). | Lyam |
| 26/11 | Event | 9 challenges algorithmiques validés en 25 min ; les points perdus sont sur les challenges **dans la salle** (c17, c23) et le **format** (c19, c22). Prochaine fois : un humain dédié à la salle dès le début. | Lyam |
