# Narrative Operating System — Fondations

> Un moteur universel de narration, explicable, modulaire, indépendant de tout modèle d'IA.
> **Pas un générateur de texte.** Un système d'exploitation pour récits.

## 1. Vision

Le Narrative OS (NOS) est conçu pour produire et piloter des récits humains, nuancés et
cohérents dans tous les domaines : cinéma, pédagogie, jeux, simulations, communication,
apprentissage. Le texte n'est qu'une *surface de rendu* parmi d'autres. Le cœur du système
est un **modèle formel du monde raconté** (agents, valeurs, croyances, engagements,
causalité) et des **moteurs** qui le font évoluer selon des règles narratives explicites.

Principe directeur, hérité de la distinction fabula/sjužet des formalistes russes et de
Genette (*Figures III*, 1972) :

- **Le monde raconté** (fabula) : états, événements, causes — porté par le système.
- **Le discours** (sjužet) : l'ordre, le point de vue, le médium — une projection du monde.
- **La surface** (texte, dialogue, image, cinématique) : un rendu, éventuellement délégué
  à un LLM, jamais dépositaire de la logique narrative.

## 2. Principes non négociables

1. **La logique narrative vit dans le système, jamais dans les prompts.** Un LLM peut
   *réaliser* (verbaliser, styliser, proposer), le système *décide* (cohérence, causalité,
   progression).
2. **Aucune dépendance à un modèle IA particulier.** Le moteur fonctionne sans LLM
   (mode symbolique pur, sortie structurée) ou avec n'importe quel fournisseur derrière
   une interface de réalisation.
3. **Pas de scènes, pas de chapitres, pas d'actes comme primitives.** Ce sont des
   *conventions de surface*, propres à des médias et des époques. Les primitives sont les
   plus petites unités invariantes (intention, valeur, conflit, croyance, engagement,
   révélation, conséquence… — voir l'ontologie).
4. **Chaque affirmation est sourcée.** Toute brique du système doit être rattachée à la
   littérature (narratologie, moteurs existants, recherche IA), ses limites identifiées,
   et l'amélioration proposée argumentée.
5. **Modularité stricte.** Un module = une responsabilité, des interfaces définies, des
   entrées/sorties typées, des tests possibles sans les autres modules.

## 3. Méthodologie

Pour chaque idée : (1) vérifier son existence dans la littérature ; (2) comparer plusieurs
approches ; (3) citer les références ; (4) identifier les limites ; (5) proposer une
amélioration argumentée. Jamais d'affirmation sans justification.

Le travail est découpé en phases. Une phase ne s'ouvre que si les fondations de la
précédente sont jugées solides (synthèse produite, architecture mise à jour, questions
ouvertes listées, expériences proposées).

## 4. Plan de phases

| Phase | Objet | Statut |
|---|---|---|
| **1** | État de l'art (narratologie, moteurs, recherche IA), invariants, ontologie v0, architecture v0 | ✅ livrée (ce dépôt) |
| **1b** | Expériences de validation E1/E2/E4/E5 ([`experiments/`](experiments/)) → amendements v0.1 (A1-A5), règles R1-R4, Q2/Q4 tranchées | ✅ gate ouverte |
| **2** | Formalisation : [schéma `nos-0.1`](schema/nos-world.schema.json), [sémantique opérationnelle](docs/phase-2/01-semantique-operationnelle.md), [corpus de référence](testdata/) + [validateur et suite de conformité](tools/) (26 tests verts) | ✅ livrée — [synthèse](docs/phase-2/02-synthese-phase-2.md) |
| 3 | Noyau exécutable : World State + Causality + Coherence (mode symbolique pur, sans LLM) | prête à ouvrir (prérequis : trancher Q8) |
| 4 | Moteurs dynamiques : personnages (BDI+émotions), tension, progression (drama manager) | — |
| 5 | Mémoire longue, transformation (arcs), couche épistémique complète | — |
| 6 | Couche de réalisation (adaptateurs LLM interchangeables + rendu structuré sans LLM) | — |
| 7 | Évaluation : métriques de cohérence/tension/tellability, études comparatives | — |

## 5. Livrables de la Phase 1

Dans [`docs/phase-1/`](docs/phase-1/) :

1. [`01-narratologie.md`](docs/phase-1/01-narratologie.md) — théories de la narration : ce que chacune apporte, ce qu'elle ne permet pas.
2. [`02-moteurs-narratifs.md`](docs/phase-1/02-moteurs-narratifs.md) — analyse des moteurs existants (Ink, Yarn Spinner, Twine, Ren'Py, Inform 7, systèmes à qualités/storylets, Versu, Façade…).
3. [`03-recherche-ia.md`](docs/phase-1/03-recherche-ia.md) — 50 ans de narration computationnelle : planification narrative, récit émergent, agents, mémoire, graphes de connaissances, LLMs.
4. [`04-invariants.md`](docs/phase-1/04-invariants.md) — les invariants présents dans toutes les grandes théories, avec preuves croisées.
5. [`05-ontologie-v0.md`](docs/phase-1/05-ontologie-v0.md) — objets fondamentaux, relations, graphes narratifs (version 0, argumentée).
6. [`06-architecture-v0.md`](docs/phase-1/06-architecture-v0.md) — architecture modulaire : les 8 moteurs, leurs interfaces, leurs E/S, leur testabilité.
7. [`07-synthese-et-questions-ouvertes.md`](docs/phase-1/07-synthese-et-questions-ouvertes.md) — synthèse de phase, décisions actées, questions ouvertes, expériences à mener avant la Phase 2.

## 6. Décisions d'architecture actées en Phase 1 (résumé)

- **D1.** La primitive centrale est le **delta narratif** : un changement d'état *chargé en
  valeur*, causé, et perçu (ou caché). Justification croisée : McKee (changement de valeur
  comme unité), Bremond (triade potentialité→passage à l'acte→achèvement), plot units de
  Lehnert (états d'affect reliés), fabula model de Swartjes & Theune.
- **D2.** Le monde raconté est un **graphe sémantique multi-couches** : couche factuelle,
  couche causale, couche épistémique (qui croit/sait quoi), couche sociale/axiologique.
  Justification : Inform 7 (relations comme citoyens de première classe), Drammar
  (ontologie du drame), Story Intention Graphs (Elson), knowledge graphs en IA narrative.
- **D3.** La progression est pilotée par un **drama manager déclaratif** opérant sur des
  mesures (tension, dette narrative, information asymétrique), pas sur un découpage en
  actes. Justification : Façade (beats), Quality-Based Narrative (storylets + qualités),
  drama management (Weyhrauch ; Roberts & Isbell).
- **D4.** Les personnages sont des agents **BDI étendus** (croyances, désirs, intentions
  + valeurs, engagements, émotions au modèle OCC). Justification : IPOCL (Riedl & Young),
  FearNot!/récit émergent (Aylett), Comme il Faut (McCoy et al.), Generative Agents (Park
  et al.) pour la mémoire.
- **D5.** Le LLM est confiné à la **périphérie** (réalisation de surface, propositions),
  derrière une interface `Realizer` interchangeable ; toute proposition repasse par les
  moteurs de cohérence avant intégration au monde. Justification : limites documentées des
  LLMs en cohérence causale longue (voir `03-recherche-ia.md`, §6).

Chaque décision est développée et sourcée dans les documents de phase.
