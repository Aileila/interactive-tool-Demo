# Brief d'utilisation du pipeline

Pour toute nouvelle idée de vidéo — histoire, pub, générique, clip. Le
pipeline transforme un texte d'idée en : prompts Midjourney, document
d'animation Seedance, planche storyboard PDF, bout-à-bout vidéo.

Deux règles absolues :

- On n'édite **jamais** un fichier généré. On corrige la source
  (`bible.json`, `plans.json`) et on relance.
- Les fichiers déposés respectent un nommage strict : `X01.png` dans
  `04_assets/`, `X01.mp4` dans `06_clips/` (X = préfixe du projet).

## Étape 0 — Poser l'idée (10 minutes)

Écrire l'idée en texte libre : trois lignes ou trois pages. Ce qui compte :
qui/quoi on voit, l'émotion visée, la fin. Ouvrir une session Claude Code
sur le dépôt et dire : « Nouveau projet : [texte]. Monte-le dans le
pipeline. » Claude crée le dossier projet (copie de l'arborescence,
préfixe d'identifiants dédié) et développe le texte en
`00_histoire/histoire.md`.

## Étape 1 — La bible (validation n° 1)

Claude en tire `01_bible/bible.json` : ratio, palette, lumière, focales,
personnages avec fiche, bloc animation (tempo, contraintes de mouvement).
C'est ici qu'on décide : format, style, personnages récurrents. Tant que la
bible n'est pas validée, rien d'autre ne bouge. Validée = figée.

## Étape 2 — Le découpage (validation n° 2)

`02_decoupage/plans.json` : un objet par plan — sujet, action, lieu,
lumière, focale, durée, personnage oui/non, voix off ou indication
sonore, mouvement et caméra (FR + EN). La contrainte de rythme (jamais
trois valeurs de plan identiques d'affilée) est vérifiée mécaniquement.
Relire comme un réalisateur : ordre, durées, ce qu'on voit.

## Étape 3 — Les moteurs (10 secondes)

    STORYBOARD_RACINE=<projet> python3 storyboard/scripts/build_prompts.py
    STORYBOARD_RACINE=<projet> python3 storyboard/scripts/build_animation.py

Sortent `03_prompts/prompts.md` (prompts image, anglais exécutable +
référence française) et `03_prompts/animation.md` (document d'exécution
Seedance). La sync Notion pousse tout dans les bases de suivi (galerie
« 🎬 » triée dans l'ordre du montage).

## Étape 4 — Les références visuelles (une fois par projet)

Dans Midjourney : créer le **sref** (assembler le moodboard décrit dans
`bible.md`, récupérer le code) et un **oref par personnage** (portrait de
référence). Reporter les URL dans `bible.json`, relancer l'étape 3. Tant
que c'est `A_CREER`, le moteur le rappelle à chaque run.

## Étape 5 — Les images (Midjourney)

Copier chaque prompt (colonne « Prompt » dans Notion), choisir la
meilleure génération, déposer le PNG dans `04_assets/` sous le nom exact
du plan. Suivre dans Notion : a generer → genere → valide → integre,
« a refaire » pour ce qui déçoit. Puis :

    STORYBOARD_RACINE=<projet> python3 storyboard/scripts/build_planche.py

→ la planche PDF, cases grises pour ce qui manque, jamais bloquant.

## Étape 6 — L'animation (Seedance)

Pour chaque plan imagé : l'image de `04_assets/` en première frame
(image-to-video) + le prompt de la colonne « Prompt animation ». Générer
au palier indiqué (5 ou 10 s), déposer le MP4 dans `06_clips/`. Puis :

    STORYBOARD_RACINE=<projet> python3 storyboard/scripts/assemble_film.py

→ `05_planche/film.mp4`, le bout-à-bout coupé aux durées du découpage.
Le lancer même incomplet : c'est le meilleur juge du rythme.

## Étape 7 — La post-production (hors pipeline, volontairement)

Son (les indications « SON : » sont sous chaque vignette de la planche),
textes et lockups (jamais dans les images générées), étalonnage. Le
pipeline s'arrête au bout-à-bout muet : le goût final reste humain.

## Si quelque chose déçoit

Ne jamais retoucher le résultat. Corriger `bible.json` ou `plans.json`,
relancer les moteurs, régénérer uniquement les plans concernés.

## Annexe — rendement attendu (objet type : 30 s, 10-12 plans)

| Poste | Traditionnel | Pipeline |
|---|---|---|
| Écriture + bible | 3-5 jours | 1-2 heures |
| Storyboard dessiné | 2-5 jours | 30 minutes |
| Production des images | 2-6 semaines, équipe | ½-1 jour, seul |
| Animation | 1-4 semaines | ½ jour |
| Coût direct | 15 000-300 000 € | 100-300 € de crédits |
| Idée → film monté | 4-10 semaines | 2-4 jours |

Ordres de grandeur : 10-20× plus rapide, coût direct divisé par 50 à 200.
À intégrer dans le plan de charge : 20-40 % de plans à régénérer
(cohérence de personnage surtout), et 1-2 jours de post-production humaine
pour du diffusable. Le vrai gain structurel : le coût marginal de
l'itération s'effondre, et la bible / le sref / les oref sont des actifs
réutilisables — le deuxième film d'un même univers coûte bien moins que le
premier. Le goulot restant est la décision créative, pas l'exécution.
