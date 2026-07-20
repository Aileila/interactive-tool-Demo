# Résultats consolidés — amendements v0 → v0.1 — décision de gate

## 1. Verdict global des expériences

| Exp. | Critère de succès | Résultat |
|---|---|---|
| E1 | tout événement signifiant exprimable sans scène/acte | ✅ sur les 3 récits (34 deltas au total) ; 5 manques consignés (A1-A5), aucun contournement silencieux |
| E2 | « pourquoi ? » + ablations correctes | ✅ 5/5 requêtes, 5/5 ablations ; 2 découvertes bonus (criticité, disposition ≠ déclencheur) |
| E3 | corrélation tension calculée/ressentie | ⏸ protocole prêt (§4), requiert des lecteurs humains |
| E4 | récit lisible et cohérent sans LLM | ✅ ; frontière Realizer/moteurs confirmée (la focalisation est systémique) |
| E5 | base de référence du coût d'authoring | ✅ mesures ci-dessous |

## 2. Amendements d'ontologie (v0 → v0.1)

Chacun est né d'un manque **observé** en E1, conformément à la méthodologie.

- **A1 — `Norm` de première classe** (source : BB, n1 « illégalité »). Une norme est une
  contrainte axiologique **sociale, opposable**, distincte des `values` personnelles :
  sa violation charge l'agent même s'il ne la partage pas (honte/risque vs culpabilité).
  Appui : CiF (règles sociales), Drammar (valeurs sociales), OCC (louabilité vs normes).
  → objet `Norm {portée, contenu, sanction, émetteur}` dans la couche axiologique.
- **A2 — Charges anticipées** (source : fable d2 ; BB d3/d5/d7). Distinguer
  `realized | anticipated` sur chaque charge. Appui théorique direct : OCC fonde
  espoir/peur sur les *prospects* — l'ontologie devient strictement alignée sur son
  modèle émotionnel. Bénéfice : le suspense (I10) se calcule sur les charges anticipées
  de l'audience, sans mécanisme ad hoc.
- **A3 — Entités collectives** (source : BB, FAMILLE ; Cité d'Ambre, GARDE).
  `CollectiveEntity {membres, croyances partagées approximées, peut être créancier/
  débiteur/porteur de charges}` — sans délibération BDI propre (v0.1 : pas d'agentivité
  collective, décision conservatrice à réévaluer en Phase 4).
- **A4 — `PlayerBinding`** (source : Cité d'Ambre). Liaison normée
  `JOUEUR = bind(Agent, AudienceModel)` : perceptions du PJ ⊆ savoir du joueur (jamais
  l'inverse imposé) ; l'ironie « contre le joueur-personnage » (d6) devient spécifiable.
- **A5 — Engagements non contractuels** (source : Cité d'Ambre c3, BB c1). Le champ
  `force` admet {contrat, serment, menace, implicite, **morale**} : une dette peut
  naître d'une *conséquence* (faute) et pas seulement d'une promesse. Appui : Ryan
  (O-worlds incluent les obligations morales non déclarées).

Règles de sémantique actées pour la Phase 2 (issues d'E2/E4) :
- **R1** : une disposition (flaw, valeur, relation) est co-cause, jamais cause
  suffisante — tout delta psy exige un déclencheur événementiel.
- **R2** : complétude (dettes soldées) et validité (causalité, épistémique) sont des
  vérifications distinctes → moteurs Progression vs Coherence, confirmé.
- **R3** : la focalisation est appliquée par le système avant tout générateur de
  surface ; un Realizer ne reçoit jamais un delta hors du champ épistémique choisi.
- **R4 (candidate)** : criticité d'un delta = f(descendants, charges) — à formaliser
  comme mesure standard (sert Progression et sifting).

## 3. E5 — Coût d'authoring (base de référence)

| Récit | Durée narrative | Objets annotés | Observation |
|---|---|---|---|
| Fable | ~30 s de lecture | 9 deltas + 22 objets | grain fin ; ratio le plus lourd |
| BB S01E01 | ~47 min | 15 deltas + ~30 objets | le grain grossier suffit à toutes les requêtes E2 ⇒ le grain est un **choix d'usage**, pas une obligation d'exhaustivité |
| Cité d'Ambre | session ~15 min | 10 deltas + 5 mécaniques + ~15 objets | les 5 mécaniques sont **réutilisables** pour d'autres sessions : le coût marginal chute à la trace seule |

Enseignements : (1) le coût est dominé par les deltas et leurs causes — c'est
précisément ce qu'un Proposer (LLM d'authoring) peut pré-remplir sous validation du
Coherence Engine ; (2) viser en Phase 2 un outillage où l'humain **valide/corrige** des
annotations proposées plutôt qu'il ne les saisit.

## 4. E3 — Protocole prêt (en attente de lecteurs)

Matériel : les 3 récits E1 rendus par le Realizer à gabarits (E4) pour neutraliser le
style. Sujets : ≥12 lecteurs. Tâche : curseur continu de tension pendant la lecture
(méthode des courbes d'intensité, cf. études sur le suspense de Sternberg
opérationnalisées par Cheong & Young). Comparaison : 3 formes candidates de la fonction
de tension — (a) enjeu × incertitude, (b) + proximité d'échéance des engagements,
(c) + charges anticipées de l'audience (A2). Critère : meilleure corrélation de rang
moyenne sur les 3 récits ; choix de la forme → tranche Q5.

## 5. Décision de gate (Phase 1 → Phase 2)

Conditions posées en `07-synthese` : E1 ✅, E2 ✅, Q2 et Q4 tranchées sur pièces,
Q1 levée ou abandonnée.

- **Q2 (registre des axes de valeur) — tranchée** : registre commun minimal
  {vie-mort, liberté, subsistance/fortune, appartenance/loyauté, estime-de-soi/fierté,
  vérité-mensonge, justice-légalité†} + extensions de domaine. Les 3 récits (3 domaines)
  sont couverts par 8 axes dont 6 partagés. († scindé en valeur personnelle vs Norm
  par A1.)
- **Q4 (temps) — tranchée** : temps logique ordonné par la causalité, datation
  optionnelle (nécessaire seulement pour les échéances d'engagements — BB d3, Ambre c1 :
  l'échéance devient le seul objet temporel daté obligatoire).
- **Q1 (Viv/StoryEngine/OpenNovel) — abandonnée par défaut** : sans précision du
  commanditaire, l'analyse documentée en EDA §9 fait foi ; réouvrable à tout moment.
- **Q5** : en attente d'E3 (n'est pas bloquante pour la formalisation des schémas).

**Verdict : gate OUVERTE.** La Phase 2 (formalisation JSON Schema de l'ontologie v0.1 +
sémantique opérationnelle des deltas et des arêtes causales + les 34 deltas d'E1 comme
jeu de test de référence) peut commencer. E3 court en parallèle et tranchera Q5 avant la
Phase 4 (Tension Engine).
