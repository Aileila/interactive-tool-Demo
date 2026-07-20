# Phase 1 — Ontologie de la narration (v0)

Statut : v0 argumentée, à formaliser en JSON Schema en Phase 2. Chaque objet est justifié
par les invariants (`04-invariants.md`) et rattaché à la littérature. Rien ici n'est une
scène, un chapitre ou un acte.

## 0. Primitive centrale : le delta narratif

**Définition.** Un `NarrativeDelta` est le plus petit fait narratif : un **changement
d'état** (ou une tentative de changement) qui est
(a) **causé** — rattaché par ≥1 arête causale typée à des deltas ou états antérieurs (I4),
(b) **chargé** — évalué sur ≥1 axe de valeur pour ≥1 agent (I3),
(c) **perçu ou caché** — doté d'une portée épistémique : quels agents (audience incluse)
l'observent, s'en informent, ou l'ignorent (I6),
(d) marqué **réversible ou irréversible** (I9).

```
NarrativeDelta {
  id, t                       // temps du monde (fabula), pas du discours
  change:  Assertion → Assertion   // motif de graphe avant → après (ou tentative échouée)
  causes:  [CausalEdge]       // physique | psychologique | sociale | thématique
  charges: [{agent, valueAxis, polarity, magnitude}]
  scope:   {observedBy: [AgentId], hiddenFrom: [AgentId], inferableBy: [AgentId]}
  reversible: bool
}
```

**Justification croisée** : changement de valeur (McKee), triade de Bremond (la tentative
échouée est un delta à part entière), plot units (Lehnert : affects reliés), fabula model
(Swartjes & Theune : arêtes typées), événement comme unité chez Herman/Ryan.
**Amélioration vs littérature** : aucun formalisme existant ne combine les quatre faces
(causale, axiologique, épistémique, irréversibilité) sur la même unité ; c'est cette
combinaison qui rend chaque moteur aval calculable sur la même donnée.

## 1. Objets fondamentaux

### 1.1 Entités et agents

- **Entity** : tout ce qui existe dans le monde raconté (personne, objet, lieu,
  institution, idée). Typée par `kind` avec héritage (Inform 7).
- **Agent** ⊂ Entity : entité à états mentaux. Modèle **BDI étendu** (Bratman 1987 ;
  Rao & Georgeff 1995 ; IPOCL) :
  - `beliefs` : sous-graphe daté d'assertions crues (K-world de Ryan) — possiblement
    fausses, incomplètes, imbriquées (croyances sur les croyances d'autrui, cf. Sabre).
  - `desires` : buts hiérarchisés en **Want** (désir conscient, objet — Truby) et
    **Need** (besoin, souvent inconscient, portant sur l'identité/croyance de soi).
  - `intentions` : plans adoptés (triades de Bremond en cours).
  - `values` : axes axiologiques pondérés propres à l'agent (loyauté > vérité, etc.) —
    fonde dilemmes et jugements (Drammar ; Egri).
  - `emotions` : état d'appraisal **OCC** (joie/détresse, espoir/peur, fierté/honte,
    gratitude/colère…), dérivé — jamais saisi à la main — de l'évaluation des deltas
    contre buts/normes/attitudes (OCC 1988 ; FAtiMA ; EMA).
  - `identity` : croyances de l'agent sur lui-même + rôles occupés (cf. Role).
  - `flaw` : faiblesse morale/psychologique = croyance erronée protégée (Truby) ; cible
    déclarée pour le moteur de conflit.
- **AudienceModel** ⊂ Agent : le récepteur comme agent épistémique standard (I6, I10 ;
  Herman ; Suspenser/Dramatis). Même structure de `beliefs`, plus `expectations`
  (prédictions de futurs) et `genreContract` (promesses de genre actives).

### 1.2 Relations et rôles

- **Relation** : arête typée et datée entre entités (aime, doit, commande, possède,
  ignore…), avec intensité et **asymétrie possible** (A aime B ≠ B aime A). Citoyenne de
  première classe (Inform 7 ; CiF).
- **Role** : fonction narrative attachable/détachable à un agent dans un contexte
  (mentor, opposant, faux allié…) — masque, pas essence (Propp ; Vogler ; Greimas).
  Un agent peut cumuler et changer de rôles ; c'est un *pattern* sur le graphe, pas un
  attribut.

### 1.3 Information et régime épistémique

- **Information** : assertion sur le monde, avec valeur de vérité dans le WorldGraph et
  distribution épistémique (qui la croit, la sait, la soupçonne).
- **Secret** : Information + intention active de dissimulation par un détenteur envers
  une portée (I6). Possède un coût de maintien (pression dramatique).
- **Revelation** : opérateur `reveal(info, to)` — delta épistémique ; le **twist** est le
  cas particulier où la révélation force le re-parcours causal d'un passé déjà montré
  (anagnorisis, Aristote).
- **Lie / Misbelief** : assertion crue-fausse installée intentionnellement (mensonge) ou
  non (malentendu, quiproquo).

### 1.4 Engagements (contribution originale, I7)

- **Commitment** : {débiteur, créancier (agent ou audience), contenu, échéance, force}.
  Sous-types : promesse, dette, serment, menace, annonce (setup/Chekhov — créancier =
  audience), contrat de genre.
  États : ouvert → honoré | trahi | annulé — chaque transition est un delta fortement
  chargé (la trahison d'un serment est un générateur de conflit canonique).

### 1.5 Valeur, conflit, dilemme

- **ValueAxis** : axe bipolaire (vie/mort, liberté/servitude, vérité/mensonge,
  appartenance/exil…) — registre ouvert, non limitatif (McKee ; Drammar).
- **Conflict** (dérivé, jamais saisi) : incompatibilité détectée entre
  (a) intentions de deux agents (CPOCL), (b) intention et état du monde,
  (c) deux desires/values d'un même agent → **Dilemma** (Ryan O/W-worlds ;
  Barber & Kudenko).
- **Stakes** : ce qui est perdu/gagné selon l'issue d'un conflit, exprimé en charges de
  valeur — entrée du calcul de tension.

### 1.6 Transformation

- **Arc** : chaîne datée de deltas **irréversibles** portant sur `identity`/`beliefs`/
  `values` d'un agent (I9) ; jalonnée de **Threshold** (delta après lequel un ensemble
  d'états antérieurs devient inaccessible — Campbell ; Field réencodé).
- **SelfRevelation** : delta épistémique réflexif (l'agent met à jour une croyance sur
  lui-même — Truby) ; clôt typiquement un Arc.

## 2. Les graphes narratifs (couches d'un même multigraphe)

| Couche | Nœuds/arêtes | Source théorique | Requêtes types |
|---|---|---|---|
| **Factuelle** | entités, relations, états datés | Inform 7 ; KG | « où est X à t ? » |
| **Causale** | deltas reliés (causes/enables/motive/thématique) | fabula model ; IPOCL | « pourquoi X ? », « qu'a permis Y ? » |
| **Épistémique** | assertions × agents (croit/sait/ignore/soupçonne), imbriquable | Ryan ; Sabre | « qui sait que A sait S ? », ironie dramatique |
| **Axiologique/sociale** | valeurs, relations sociales, normes, engagements | CiF ; Drammar ; I7 | « quels serments ouverts ? », « quelle norme viole ce delta ? » |
| **Discours** | unités de rendu ordonnées, focalisation, ellipses | Genette ; Suspenser | « qu'a vu l'audience, dans quel ordre ? » |

La couche discours référence les autres sans les dupliquer (I1) : raconter = sélectionner
et ordonner des deltas, choisir une focalisation, en cacher d'autres.

## 3. Taxonomie des mécaniques narratives (v0)

Mécanique = opérateur paramétré sur le graphe, avec préconditions et effets (storylet
généralisée, cf. `02-moteurs-narratifs.md` §6). Familles :

1. **Épistémiques** : révéler, cacher, mentir, semer un indice, quiproquo, ironie
   dramatique, twist.
2. **Contractuelles** : promettre, trahir, honorer, menacer, annoncer (setup/payoff).
3. **Conflictuelles** : interférer avec un plan, attaquer la faiblesse, escalader,
   forcer un dilemme, sacrifier.
4. **Relationnelles** : allier, rompre, séduire, trahir la confiance, changer de rôle.
5. **Transformationnelles** : franchir un seuil, tenter/échouer (Bremond), révélation de
   soi, chute/rédemption.
6. **De disruption** : méfait/manque (Propp), appel, catastrophe, don inattendu.
7. **De discours** : ellipse, retard, changement de focalisation, montage alterné,
   analepse/prolepse (Genette).

Chaque mécanique déclare ses effets attendus sur les mesures (tension, dette,
équilibre) — c'est ce qui permet au moteur de progression de composer sans gabarit d'actes.

## 4. Ce que cette ontologie interdit volontairement

- Pas d'objet « Scene », « Chapter », « Act » au niveau monde (uniquement des unités de
  rendu côté discours, définies par les profils de médium).
- Pas d'émotion saisie à la main : toujours dérivée par appraisal (sinon incohérences
  garanties entre état et affect).
- Pas de « conflit » saisi à la main : toujours détecté (sinon le moteur de cohérence ne
  peut pas le vérifier).
- Pas de texte comme source de vérité : le texte est une projection, régénérable.
