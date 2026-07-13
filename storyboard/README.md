# Pipeline storyboard Midjourney

Une histoire en entrée, un storyboard PDF en sortie. Le pipeline ne génère
aucune image : Midjourney n'a pas d'API publique, il y a donc une étape
humaine obligatoire entre la génération des prompts et l'assemblage de la
planche.

## Relancer sur une nouvelle histoire

Remplacer `00_histoire/histoire.md`, relancer. Concrètement :

1. Remplacer `00_histoire/histoire.md` par la nouvelle histoire.
2. Réécrire `01_bible/bible.json` (et `bible.md`) à partir de l'histoire,
   puis figer la bible après validation.
3. Réécrire `02_decoupage/plans.json` (un objet par plan).
4. `python3 scripts/build_prompts.py` → produit `03_prompts/prompts.md`.
5. Coller chaque prompt dans Midjourney, déposer les images dans
   `04_assets/` nommées `P01.png`, `P02.png`, etc.
6. `python3 scripts/build_planche.py` → produit `05_planche/storyboard.pdf`.

Les étapes 2 et 3 sont les seules étapes d'écriture. Tout le reste est
dérivé et régénéré à l'identique par les scripts.

## Arborescence

| Chemin | Rôle | Édité à la main ? |
|---|---|---|
| `00_histoire/histoire.md` | Histoire d'entrée | oui (c'est l'entrée) |
| `01_bible/bible.json` | Gabarit visuel, figé après validation | oui |
| `01_bible/bible.md` | Bible en lecture humaine | oui |
| `02_decoupage/plans.json` | Table de pilotage, 1 objet = 1 plan | oui |
| `03_prompts/prompts.md` | Prompts Midjourney | **non — généré** |
| `04_assets/` | PNG déposés depuis Midjourney | dépôt manuel |
| `05_planche/storyboard.pdf` | Planche finale | **non — généré** |
| `scripts/build_prompts.py` | Moteur de prompts | oui |
| `scripts/build_planche.py` | Assemblage de la planche | oui |

## Règles

- Si un prompt est mauvais : corriger `plans.json` ou `bible.json`, relancer
  `build_prompts.py`. Ne jamais éditer `prompts.md`.
- `--sref` est identique sur tous les plans (cohérence de style globale).
  Tant que `bible.json` contient `"sref": "A_CREER"`, le moteur le signale :
  créer le moodboard décrit dans `bible.md`, récupérer le code sref dans
  Midjourney, le reporter dans `bible.json`, relancer.
- Même chose pour l'`oref_url` de chaque personnage (portrait de référence).
- Affectation du modèle (état Midjourney juillet 2026, codée dans
  `build_prompts.py` → `parametres_modele`) : `--oref` n'existe qu'en V7,
  donc plan avec personnage → V7 `--oref --ow`, plan sans personnage →
  V8.1 `--hd`.
- `--s` est plafonné à 250 par le moteur, quelle que soit la bible.
- Ordre de prompt imposé : sujet → action → environnement → lumière →
  paramètres.
- Aucun texte incrusté dans l'image : les titres sont ajoutés en post.
- Contrainte de rythme vérifiée par le moteur : jamais trois valeurs de
  plan identiques consécutives (erreur bloquante sinon).
- `build_planche.py` signale les images manquantes (case grise dans le PDF
  et liste en console) sans jamais planter.

## Dépendances

Python 3 standard + `reportlab` (`pip install reportlab`). Rien d'autre.
