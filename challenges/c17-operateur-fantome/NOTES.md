---
owner: lyam
status: failed
points: "26"
tags: "bonusmalus"
answer: ""
confidence: ""
---

# c17 L'opérateur fantôme

## Réponse

Non trouvée pendant l'event (0 essai soumis, donc aucun malus).

## Solution (connue après coup)

Challenge **hybride : l'indice était sur le site, la réponse dans la salle.**

1. **Sur le site** : une image complètement invisible était cachée dans la **page HTML du
   scoreboard** (`/scoreboard`). Elle donnait la consigne : aller voir un opérateur et lui
   demander où aura lieu la prochaine fête. Rapporté de vive voix après l'event par l'équipe
   qui l'a validé en premier : leur Claude, qui lisait le site page par page, l'a signalée
   tout de suite (« j'ai trouvé ça »). Contenu exact de l'image non vu par nous.
2. **Dans la salle** : chuchoter **« Où aura lieu la fête »** à un organisateur **portant une
   étoile de shérif**. Il répondait par l'adresse, dont le nom de rue était le flag (format
   `rue du saloon`, sans déterminant).

Lecture de l'énoncé a posteriori :
- « l'Opérateur Fantôme est toujours en ville » → c'est quelqu'un de présent dans la salle ;
- « ces messages passent sous les yeux de tout le monde » → la page que tout le monde regarde :
  le **scoreboard** ;
- « le lieu du prochain sabotage » → dans le code des conspirateurs, le sabotage devient « la fête ».

**Pourquoi on l'a raté** : on a appelé l'API `/api/v1/scoreboard` (JSON) au moins 5 fois,
mais jamais lu la page HTML `/scoreboard`. Le JSON ne contient que les équipes et les
scores : une `<img>` du gabarit de la page n'y apparaît pas. Le sous-agent « repartir de
zéro » avait pourtant cité « le scoreboard » parmi les endroits « sous les yeux de tout le
monde », mais l'a rangé dans la piste « salle ».

## Ce qui n'a pas marché / pièges

- Image invisible de l'énoncé (`/files/media/indice_operateur_fantome.txt`) : appât, elle
  contient seulement « Bien essayé, mais c'est non… vous êtes sur la bonne voie ». On l'a lue
  comme une impasse ; elle voulait dire « image cachée = bonne technique, mauvais endroit ».
- ~40 min de fouille de la plateforme, sans lire les pages HTML du site : HTML/JSON du challenge, en-têtes HTTP,
  flux `/events`, `/plugins/countdown/times`, notifications, robots.txt, CSS/JS du thème,
  logo/bannière/favicon, utilisateurs et équipes, DNS, stéganographie du texte (acrostiches,
  accents, caractères invisibles), fichiers des autres challenges, réseaux Wi-Fi.
- Demandes aux orgas sans la bonne phrase (« c'est vous l'opérateur fantôme », lampe torche,
  « Bandit », « Reno ») : refusées.

## Indices qu'on avait

- Normale Surchauffe l'a validé à 19:29 (UTC), 9 min après le début, sans dépendre d'un
  autre challenge : la clé était accessible tout de suite.
- Certains orgas portaient une étoile de shérif, d'autres non.

## Leçon

1. Dès la 1re minute : `python3 scripts/recon_ctfd.py <url>` lit **toutes les pages HTML**
   du site (pas seulement l'API) et relève les images et textes cachés.
2. Un appât qui dit « bonne voie » confirme la technique : chercher le même procédé ailleurs.
3. Énoncé sans fichier + « toujours en ville » → un humain dans la salle, qui parle aux orgas
   avec le vocabulaire du récit. Voir `docs/PLAYBOOK.md`, section 6.
