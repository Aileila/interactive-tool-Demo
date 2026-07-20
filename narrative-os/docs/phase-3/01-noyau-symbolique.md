# Phase 3 — Le noyau symbolique : Q8, architecture du kernel, catalogue de refus

## 1. Q8 tranchée : vocabulaire de prédicats

**Décision** : noyau commun minimal + extensions déclarées par monde (champ
`vocabulary`), format `nos-0.2`.

Noyau (9 prédicats) : `situé-à` (fonctionnel : une localisation par sujet), `possède`
(objet exclusif : un possesseur par objet), `est` (propriété libre), `croit`, `sait`,
`veut`, `intention`, `cache`, `membre-de`. Toute autre relation est une **extension de
domaine** déclarée (ex. fable : `a-flatté`) ; un prédicat non déclaré est refusé
(R-VOCAB-1) ; redéfinir le noyau est interdit.

**Alternatives écartées, avec raisons** :
- *Vocabulaire libre* (tout prédicat accepté) : c'est le régime de fait des LLMs — il
  interdit toute vérification de contradiction (deux prédicats synonymes non unifiés) ;
  rejeté par l'objectif même du noyau.
- *Ontologie lourde* (OWL/Drammar complet, event calculus) : puissance supérieure
  (inférence, subsomption) mais coût d'authoring et d'implémentation contraire à la
  leçon n° 3 de l'état de l'art des moteurs (le mur de l'authoring) ; l'expressivité
  supplémentaire n'était requise par **aucune** requête d'E2. Réévaluable si un domaine
  l'exige.
- *Triplets RDF stricts avec IRIs* : interopérabilité réelle mais lourdeur d'écriture ;
  le mapping vers RDF reste trivial depuis notre forme (sujet, prédicat, objet) si un
  besoin d'export apparaît.

**Validation sur pièces** (méthode imposée par le gate) : les trois mondes ont été
re-convertis — chaque delta porte désormais des assertions machine et, quand il est
pertinent, un `actor`. Le noyau + 1 extension a suffi aux 34 deltas ; aucune requête
d'E2 n'a été dégradée (suite Phase 2 : 26/26 inchangés).

## 2. Architecture du kernel (`kernel/`)

```
kernel/
  model.py       World : la fabula chargée/indexée (délègue les requêtes causales)
  vocabulary.py  noyau Q8 + build_vocabulary(monde) → vocabulaire effectif
  validation.py  conformité statique nos-0.2 (miroir du schéma + règles)
  causality.py   Causality Engine : ancestors / descendants / ablate / criticality
  store.py       World State Store : event sourcing, état = triplets, time-travel
  coherence.py   Coherence Engine : propose(delta) → commit | refus motivés
```

Séparation stricte conforme à l'architecture v0 :

- **Store** applique sans vérifier (responsabilité unique : l'état et son histoire).
  État = ensemble de triplets ; l'historique des deltas committés **est** la fabula
  (event sourcing). `state_at(t)` reconstruit tout état passé (exigence posée en
  Phase 1 : le twist relit le passé ; le rollback façon Ren'Py sert le débogage
  narratif) ; `rollback()` fait le time-travel arrière.
- **Coherence** est le seul chemin d'écriture (`propose` → `check` → commit). Il ne
  connaît ni LLM ni surface : il applique le catalogue de règles ci-dessous et rend des
  **refus motivés** — règle + message + éléments en cause. C'est l'interface qu'un
  `Proposer` (LLM ou non) recevra en Phase 6 : le refus est le signal d'apprentissage.
- **Causality** reste pur (fonctions sur la fabula), inchangé depuis la Phase 2 —
  l'« industrialisation » a consisté à le sortir de l'outil de validation pour en faire
  un module du noyau, l'API de la suite Phase 2 étant préservée par délégation
  (`tools/nosval.py` est devenu un shim).

## 3. Catalogue des refus (contrat du Coherence Engine)

| Règle | Refuse | Fondement |
|---|---|---|
| R-CAUS-1 | cause vers un delta non committé | I4 (causalité vérifiable) |
| R-CAUS-2 | précondition dure `requires` non committée | nécessité (Phase 2 §2) |
| R-CAUS-3 | dispositions/engagements sans déclencheur | R1 |
| R-CAUS-4 | temps logique non croissant | Q4 (ordre de fabula) |
| R-EPIS-1 | l'acteur réagit (psy) à un delta hors de son champ épistémique, sauf révélation committée | I6 — l'erreur LLM canonique (« agir sur ce qu'on ignore ») |
| R-EPIS-2 | observed/hidden non disjoints | I6 |
| R-EPIS-3 | le PJ observe sans son joueur | A4 |
| R-VOCAB-1 | prédicat hors vocabulaire | Q8 |
| R-STATE-1 | retrait d'une assertion absente | continuité factuelle |
| R-STATE-2 | ajout d'une assertion déjà présente | idem |
| R-STATE-3 | seconde valeur d'un prédicat fonctionnel | idem (téléportation…) |
| R-STATE-4 | double possession d'un objet exclusif | idem |

La règle R-EPIS-1 est **sensible aux révélations** : un acteur peut réagir à un delta
caché si une révélation committée le lui a transmis — testé dans les deux sens (accepté
après d8/r1 de la Cité d'Ambre, refusé avant). L'information qui circule éteint le refus :
c'est la mécanique du quiproquo et de sa résolution, obtenue sans règle dédiée.

## 4. Deux résultats notables de l'implémentation

1. **R-EPIS-1 a corrigé notre propre corpus.** Le premier rejeu de la Cité d'Ambre a été
   refusé : d6 (« Mira couvre la fuite et se fait identifier ») était attribué à la
   GARDE comme acteur, alors que sa cause psychologique (le pacte du choix 1, d4) est
   inaccessible à la Garde — l'acteur réel de la cause est MIRA. L'annotation a été
   corrigée, pas la règle. C'est le comportement attendu du gardien : il attrape les
   erreurs d'attribution mentale, première cause d'incohérence des générateurs.
2. **L'irréversibilité est narrative, pas factuelle.** La détention de Mira (état,
   posé par d6 irréversible) prend fin en d10 ; ce qui ne peut pas être défait, c'est
   que *l'arrestation a eu lieu* (le delta reste dans l'historique, ses charges et son
   empreinte causale persistent). Le flag `irreversible` contraint donc les **arcs et
   l'espace des futurs**, jamais l'algèbre des assertions — précision de sémantique
   actée, découverte en écrivant le test.

## 5. Limites assumées de v0.2 (et où elles se lèvent)

- Les croyances par agent restent des triplets `croit/sait` plats — la couche
  épistémique *imbriquée* (A croit que B sait…) attend la Phase 5, portée par le même
  store (préfixage de contexte), profondeur bornée (Q3).
- Le Coherence Engine vérifie, il ne **répare** pas (pas de suggestion d'alternative
  dans le refus) ; la réparation guidée est un objectif Phase 6 (dialogue avec le
  Proposer).
- Les préconditions des mécaniques ne sont toujours pas compilées en motifs — c'est le
  premier chantier de la Phase 4 (le Progression Engine en a besoin pour sélectionner).
