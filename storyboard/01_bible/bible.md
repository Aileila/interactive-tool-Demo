# Bible visuelle — La dernière lanterne

Version humaine de `bible.json`. Le fichier qui fait foi est `bible.json` :
il est figé après validation et le moteur ne lit que lui.

## Style global

- **Ratio** : 16:9 (format storyboard écran).
- **Stylize** : 200 (plafond du pipeline : 250).
- **Référence de style (`--sref`)** : `A_CREER` — aucun sref n'existe encore.
  Voir le moodboard ci-dessous. Une fois l'URL sref obtenue dans Midjourney,
  la reporter dans `bible.json` et relancer `scripts/build_prompts.py`.

## Palette

| Couleur | Rôle |
|---|---|
| Bleu nuit profond | Dominante : ciel, mer, nuit |
| Ambre chaud de lanterne | Source de lumière unique, cœur émotionnel |
| Gris ardoise | Rochers, murs du phare, tempête |
| Blanc écume | Vagues, pluie, accents |
| Jaune ciré usé | Signature du personnage |

## Lumière

Source chaude unique dans une nuit froide. Contre-jours marqués, pluie
rétroéclairée. Tout le film oppose l'ambre de la flamme au bleu de la mer.

## Focales

24mm (plans d'ensemble), 35mm (plans larges), 50mm (plans moyens),
85mm (plans rapprochés et gros plans).

## Personnages

### nora (`--oref`, `--ow 450`, modèle V7)

Femme de 60 ans, cheveux gris courts, visage buriné, regard clair. Ciré
jaune usé sur pull de laine sombre, bottes de mer.

**URL oref** : `A_CREER`. Générer d'abord un portrait de référence de Nora
dans Midjourney (V7, fond neutre, buste, lumière douce), récupérer l'URL de
l'image, la reporter dans `bible.json` → `personnages[0].oref_url`, puis
relancer le moteur.

## Moodboard à réunir pour créer le --sref (10 images)

1. Phare de Kéréon ou d'Ar-Men battu par une vague, photo longue focale.
2. Photogramme de nuit de « The Lighthouse » (2019) pour les textures, mais en couleur.
3. Peinture d'Edward Hopper « Lighthouse Hill » pour les masses simples.
4. Photo de lanterne de phare allumée vue de l'intérieur, optique de Fresnel ambre.
5. Mer d'huile au crépuscule, dégradé bleu nuit vers ambre.
6. Portrait de marin âgé en ciré, lumière de lampe-tempête.
7. Escalier en colimaçon de phare, éclairage rasant chaud.
8. Pluie rétroéclairée par un projecteur, fond noir.
9. Caboteur feux allumés dans la brume, vu de loin.
10. Aube grise sur une île rocheuse, contre-jour doux.

Assembler ces images dans Midjourney (`/imagine` d'un collage ou via l'onglet
style reference), récupérer le code `--sref`, le reporter dans `bible.json`.
