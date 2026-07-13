# Bible visuelle — Générique Maqnin

Version humaine de `bible.json`. Le fichier qui fait foi est `bible.json`.
L'ADN de marque complet est dans `00_histoire/histoire.md` ; cette bible le
traduit en règles d'image.

## Ce que chaque règle d'image doit raconter

| Pilier ADN | Traduction visuelle |
|---|---|
| Héritage (le maqnin du Maghreb) | l'oiseau est le seul sujet, jamais un décor |
| Artisanat | macros de matière : fil, papier, perles, broderie |
| Métamorphose | la créature émerge de la matière, jamais montrée d'emblée |
| Envol | caméra qui s'élargit, fils suspendus, l'oiseau choisit où se poser |

## Style global

- **Ratio** : 16:9 (à trancher avant production si la cible est verticale).
- **Stylize** : 250 (le plafond — le générique est un objet esthétique).
- **`--sref`** : `A_CREER` — à construire d'abord à partir du **clip
  existant** : extraire 6 à 8 frames nettes de la vidéo actuelle
  (macro tête, ailes déployées, plan lettrage bleu nuit), les compléter de
  2 à 3 références de sculpture textile (style Zim & Zou / paper art), et
  créer le code sref dans Midjourney. Le générique doit être raccord avec
  ce qui est déjà tourné.

## Palette

Écru fibre de lin (dominante matière), rouge chardonneret (le masque —
seule couleur vive), noir perle (œil, calotte, ponctuation), gris atelier
dégradé (fond des actes 1-2), bleu nuit signature (fond de l'acte 3, celui
du logo), blanc calligraphie (la courbe finale).

L'arc chromatique du générique : écru/gris (matière) → rouge révélé
(vie) → bleu nuit + blanc (signature). Le fond glisse du gris au bleu
pendant l'envol : c'est la transition de marque.

## Lumière

Studio douce et enveloppante, fond dégradé, aucune ombre dure. Sur les
plans d'envol, matière rétroéclairée (les fils deviennent lumineux).

## Personnage

### maqnin (`--oref`, `--ow 450`, modèle V7)

La sculpture du chardonneret : fibres de papier, broderie et lin, masque
rouge profond, calotte noire, joues blanches, aile noire à barre rouge,
œil de perle noire cerclé de broderie, ailes déployables en éventail de
fils écrus piquetés de perles noires.

**URL oref** : `A_CREER` — utiliser une frame nette du clip existant
(tête de trois quarts, acte 2) comme image de référence : c'est elle qui
garantit que les nouveaux plans prolongent l'existant.

## Son (pilier du montage, hors Midjourney)

Le champ `voix_off` de chaque plan porte l'indication sonore, imprimée
sous chaque vignette de la planche. Fil conducteur : bruits de matière
(acte 1) → montée organique et battement (acte 2) → chant réel du
chardonneret, trois notes, puis silence sur le lockup (acte 3). Le chant
du maqnin est la signature sonore de la marque.

## Règle absolue

Aucun texte dans les images générées : le plan final est une courbe
calligraphique blanche abstraite, le lockup « MaQnin / maqnin.com » est
ajouté en post-production.
