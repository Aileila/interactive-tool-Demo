# Bible visuelle — La Revanche

Version humaine de `bible.json`. Le fichier qui fait foi est `bible.json` :
il est figé après validation et le moteur ne lit que lui.

## Style global

- **Ratio** : 16:9 (format storyboard écran).
- **Stylize** : 200 (plafond du pipeline : 250).
- **Référence de style (`--sref`)** : `A_CREER` — aucun sref n'existe encore.
  Voir le moodboard ci-dessous. Une fois le code sref obtenu dans Midjourney,
  le reporter dans `bible.json` et relancer `scripts/build_prompts.py`.

## Palette

| Couleur | Rôle |
|---|---|
| Bleu nuit d'open space | Le monde corporate qui les écarte |
| Cuivre chaud | L'atelier, le collectif, la reconquête |
| Gris béton | Bureaux, brique peinte, ville |
| Blanc froid d'écran | Écrans, IA, scènes de travail nocturne |
| Bordeaux profond | Accent : blazers, affiches, scène de conférence |

## Lumière

Lumières froides d'écran contre lampes chaudes d'atelier, néons de ville en
fond, contrastes marqués. L'arc du film va du froid corporate (début) vers
le chaud de l'atelier, puis les projecteurs de scène (fin).

## Focales

24mm (plans d'ensemble), 35mm (plans larges et moyens en mouvement),
50mm (plans moyens posés), 85mm (plans rapprochés et gros plans).

## Personnages

### claire (`--oref`, `--ow 450`, modèle V7)

Femme de 54 ans, carré court argenté, blazer sombre bien coupé sur chemise
claire, regard déterminé, port droit. Ex-directrice marketing, fondatrice
du collectif.

**URL oref** : `A_CREER`. Générer un portrait de référence (V7, buste, fond
neutre, lumière douce), reporter l'URL dans `bible.json` →
`personnages[].oref_url`, relancer le moteur.

### awa (`--oref`, `--ow 450`, modèle V7)

Femme de 58 ans, tresses grises relevées, lunettes rondes fines, chemise à
motifs colorés, sourire en coin. Ex-ingénieure systèmes, architecte de la
plateforme. Son vieux portable couvert de stickers est son accessoire
signature.

**URL oref** : `A_CREER`, même procédure que pour claire.

## Moodboard à réunir pour créer le --sref (10 images)

1. Open space de tour de bureaux la nuit, éclairage bleu froid, photo réaliste.
2. Portrait éditorial d'une dirigeante aux cheveux argentés, lumière douce (type presse économique).
3. Atelier de brique reconverti en bureau, lampes tungstène chaudes, câbles apparents.
4. Photogramme de « Margin Call » ou « The Intern » pour la grammaire corporate.
5. Macro d'un clavier mécanique éclairé, mains de femme âgée, reflets d'écran.
6. Café le soir, groupe en discussion animée autour d'une table, lumière mixte.
7. Scène de conférence tech : keynote, projecteurs, salle dans la pénombre.
8. Ville en périphérie à l'aube, brume, une fenêtre d'atelier allumée.
9. Vieux portable couvert de stickers ouvert dans la pénombre, écran allumé.
10. Couloir de bureaux vide avec carton de déménagement, lumière neutre triste.

Assembler ces images dans Midjourney (onglet style reference), récupérer le
code `--sref`, le reporter dans `bible.json`, relancer le moteur.
