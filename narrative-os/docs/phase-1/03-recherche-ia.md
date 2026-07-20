# Phase 1 — État de l'art : narration computationnelle et IA

Objectif : couvrir ~50 ans de recherche (symbolique → agents → LLMs), en extraire les
mécanismes validés et les limites documentées. Chaque section se termine par « retenu /
rejeté » pour le NOS.

---

## 1. Génération symbolique classique (1977-2000)

- **TALE-SPIN** (Meehan, 1977) : les histoires émergent de la **résolution de problèmes
  par les personnages** (planification de buts : faim → obtenir nourriture). Leçon
  fondatrice, y compris par ses échecs célèbres (« mis-spun tales ») : la seule
  rationalité des personnages produit des comptes rendus, pas des récits — il manque la
  dimension auctoriale.
- **UNIVERSE** (Lebowitz, 1984) : bascule inverse — planification **auctoriale**
  (author goals) sur un soap opera sans fin ; les personnages sont des ressources du plan
  auteur. Introduit la tension personnage/auteur qui structure tout le champ.
- **MINSTREL** (Turner, 1993) : créativité par transformation de cas connus (TRAMs) ;
  montre l'intérêt et la fragilité du raisonnement par cas en narration.
- **MEXICA** (Pérez y Pérez, 1999) : cycle **engagement-réflexion** — génération
  associative libre puis critique/réparation. Ce motif « proposer largement, filtrer
  strictement » est directement réutilisable (c'est notre patron LLM-propose /
  moteurs-disposent).
- **Plot units** (Lehnert, 1981) : résumé du récit par configurations d'**états
  affectifs** (+/-/M) reliés par motivation/actualisation — première formalisation du
  récit comme graphe d'affects. Précurseur direct de notre « delta narratif ».

**Retenu** : la dialectique but-personnage vs but-auteur ; engagement-réflexion ;
l'affect comme colonne vertébrale du résumé narratif. **Rejeté** : gabarits de plans
fermés (passage à l'échelle impossible sans modularité).

## 2. Planification narrative (1990-2020)

- **IPOCL / Fabulist** (Riedl & Young, « Narrative Planning: Balancing Plot and
  Character », JAIR 2010) : planification à causalité explicite où chaque action d'un
  personnage doit être **intentionnellement justifiée** (rattachée à un but adopté par ce
  personnage), tout en atteignant le but auctorial. Résout formellement TALE-SPIN vs
  UNIVERSE.
- **CPOCL / conflit** (Ware & Young, 2011-2014) : extension où des plans **en conflit**
  coexistent (le conflit = interférence planifiée entre plans d'agents) ; **Sabre**
  (Ware & Siler, 2021) ajoute croyances imbriquées et utilités — l'état de l'art du genre.
- **Suspense et théorie du récepteur** : **Suspenser** (Cheong & Young, 2015) et
  **Dramatis** (O'Neill & Riedl, 2014) planifient le *discours* pour maximiser le
  suspense, défini via les plans d'échappement perçus par l'audience — preuve
  computationnelle que **la tension est une propriété du modèle mental du récepteur**
  (converge avec Herman, cf. `01-narratologie.md` §9).
- **Drama management** : de Weyhrauch (1997, recherche adversariale sur une fonction
  d'évaluation auctoriale) aux TTD-MDP (Roberts & Isbell) : arbitrer en continu entre
  liberté du joueur et objectifs auteur.

**Retenu** : causalité et intentionnalité comme **contraintes de validité vérifiables**
(pas des heuristiques) ; le conflit comme relation entre plans ; la tension calculée sur
le modèle du récepteur. **Limite documentée** : explosion combinatoire — la planification
complète ne passe pas l'échelle d'un monde riche ; d'où notre choix de la réserver à des
horizons courts (vérification locale) plutôt qu'à la génération globale.

## 3. Récit émergent et agents sociaux

- **Emergent narrative** (Aylett, 1999 ; **FearNot!**, Aylett et al., 2005) : agents
  affectifs autonomes (architecture FAtiMA, émotions **OCC**) en pédagogie anti-harcèlement
  — validation du récit émergent *à but pédagogique*, notre cas d'usage « éducation ».
- **OCC** (Ortony, Clore & Collins, *The Cognitive Structure of Emotions*, 1988) : les
  émotions comme **évaluations cognitives** (désirabilité d'événements vs buts,
  louabilité d'actions vs normes, attrait d'objets vs attitudes). Standard de facto de
  l'émotion computationnelle (utilisé par FAtiMA, EMA de Gratch & Marsella).
- **Comme il Faut / Prom Week** (McCoy et al., 2011-2014) et **Versu** (Evans & Short,
  2014) : normes sociales réifiées, volitions calculées (cf. `02-moteurs-narratifs.md`).
- **Kreminski & Wardrip-Fruin** (« Felt », « Winnow », 2019-2021) : moteurs légers de
  **reconnaissance de motifs narratifs** dans un flux d'événements simulés (sifting) —
  répond au problème Dwarf Fortress (récit riche mais non raconté) : simuler large,
  **extraire** les suites d'événements tellables.

**Retenu** : OCC pour les émotions ; volitions sociales à la CiF ; le **story sifting**
comme moteur duale de la génération (le NOS doit savoir *reconnaître* un récit dans un
flux d'événements, pas seulement en produire).

## 4. Mémoire d'agents et contexte long

- **Generative Agents** (Park et al., UIST 2023) : mémoire en **flux d'observations**
  avec récupération pondérée par **récence × importance × pertinence**, plus
  **réflexions** périodiques (synthèses de plus haut niveau) et planification
  journalière. Comportements sociaux émergents crédibles (diffusion d'information,
  coordination).
- **MemGPT** (Packer et al., 2023) et lignée « LLM OS » : hiérarchie mémoire
  (contexte = RAM, stockage externe = disque, l'agent pagine lui-même).
- Limite documentée de la fenêtre longue seule : dégradation du rappel en milieu de
  contexte (« lost in the middle », Liu et al., 2023) ; le contexte long n'est pas une
  mémoire structurée.

**Retenu** : mémoire hiérarchique (épisodique → sémantique via réflexion) avec
récupération multi-critères, mais adossée au **graphe** (la mémoire d'un agent = un
sous-graphe daté de croyances, pas un tas de textes) — amélioration argumentée : la
récupération devient une requête de graphe explicable, et l'oubli/la déformation
deviennent des opérations typées (utile dramatiquement : faux souvenirs, secrets).

## 5. Graphes de connaissances et représentations narratives

- **Story Intention Graphs** (Elson, 2012) : annotation du récit en couches
  (textuelle, temporelle, **interprétative** : buts, croyances, affects) — validation
  qu'une couche interprétative est nécessaire pour capturer la similarité entre récits.
- **Drammar** (Damiano, Lombardo et al.) : ontologie formelle (OWL) du drame — unités,
  agents, **valeurs en jeu**, émotions ; conçue pour l'annotation et le patrimoine.
  Base solide, mais orientée description de récits existants, pas exécution.
- **OntoMedia, ProppOnto**, story grammars : ontologies descriptives partielles.
- **Fabula model** (Swartjes & Theune, Virtual Storyteller, 2006) : graphe causal typé —
  éléments {but, action, événement, perception, état interne} reliés par arêtes typées
  {motive, enables, causes (φ/ψ)} psychologiques ou physiques. **Le formalisme causal le
  plus directement réutilisable** pour notre couche causale.
- Знание récent : extraction de graphes narratifs par LLM (character graphs, event
  graphs) — utile en outillage, pas en fondation.

**Retenu** : fabula model (arêtes causales typées) + couche interprétative (SIG) +
valeurs (Drammar). **Manque identifié dans la littérature** : aucune de ces ontologies ne
réifie **engagements, dettes, promesses et secrets** comme objets de première classe —
alors que la narratologie (Ryan : O-worlds ; McKee : setup/payoff) les exige. C'est une
contribution originale assumée de notre ontologie v0.

## 6. LLMs et narration longue (2022-2025)

- **Dramatron** (Mirowski et al., 2022) : génération **hiérarchique** de scénarios
  (logline → personnages → beats → dialogues) avec humain dans la boucle ; l'étude
  utilisateur confirme : structure utile, cohérence longue fragile.
- **Re³** (Yang et al., 2022) et **DOC** (Yang et al., 2023) : plan-brouillon-réécriture-
  vérification, contrôle par plan détaillé ; améliorent mais ne suppriment pas les
  dérives (contradictions factuelles, personnages qui « oublient »).
- Études d'évaluation (p. ex. Chakrabarty et al., 2024, sur le test créatif ; travaux
  sur la cohérence longue) : les LLMs seuls excellent en style et cohésion locale,
  échouent statistiquement sur **la causalité longue, la constance des états mentaux, la
  gestion de l'information cachée** (qui sait quoi), et l'homogénéité vers des tropes.
- **GENEVA, StoryVerse, agents scénaristes multi-LLM** (2023-2025) : orchestration
  multi-agents de personnages LLM sous contraintes d'un « directeur » — convergence
  indépendante de plusieurs équipes vers notre architecture cible (agents + arbitre),
  mais l'état y reste textuel, donc invérifiable.

**Conclusion structurante (fonde la décision D5)** : les faiblesses des LLMs sont
exactement les fonctions que la recherche symbolique sait garantir (causalité,
cohérence d'état, épistémique), et réciproquement (surface, variété, naturel). Le NOS
est donc **neuro-symbolique par construction** : état et règles symboliques,
vérifiables ; proposition et réalisation librement neuronales, interchangeables, ou
absentes.

## 7. Positionnement du NOS dans le champ

| Fonction | Meilleure référence validée | Ce que le NOS reprend | Ce que le NOS ajoute |
|---|---|---|---|
| Monde & causalité | Inform 7 ; fabula model ; Ceptre | relations + règles ; arêtes causales typées | multi-couches (fait/cause/croyance/valeur) unifiées |
| Personnages | BDI ; OCC ; CiF ; IPOCL | croyances-désirs-intentions ; appraisal ; volitions sociales | valeurs et engagements de 1re classe ; désir vs besoin (Truby) |
| Progression | storylets/QBN ; Façade ; drama management | sélection par état ; arbitre dramatique | mesures explicites (tension, dette narrative) sur le graphe |
| Mémoire | Generative Agents ; MemGPT | récence×importance×pertinence ; réflexion | mémoire = sous-graphe daté ; oubli/distorsion typés |
| Récepteur | Suspenser/Dramatis ; Herman | tension calculée sur le modèle de l'audience | audience = agent épistémique standard du système |
| Surface | Dramatron ; Re³/DOC | génération hiérarchique contrainte | LLM optionnel, derrière interface, jamais source de vérité |
