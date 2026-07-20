# Phase 1 — Les invariants de la narration

Méthode : un candidat n'est retenu comme **invariant** que s'il apparaît, sous des noms
différents, dans **au moins trois traditions indépendantes** (narratologie littéraire,
scénaristique, narratologie cognitive/mondes possibles, narration computationnelle) et
s'il survit aux contre-exemples (récits non occidentaux, non linéaires, interactifs,
non textuels). Les conventions qui échouent à ce test (actes, scènes, chapitres, ordre de
Propp, monomythe) sont classées **conventions de surface**.

---

## I1. Double niveau : monde raconté ≠ discours

- Formalistes russes (fabula/sjužet) ; Genette (histoire/récit/narration) ; Chatman
  (story/discourse) ; en IA : séparation fabula/discours du Virtual Storyteller,
  planification du discours de Suspenser/Dramatis.
- Contre-exemples : aucun — même un récit oral linéaire est une *sélection* d'un monde
  plus riche.
- **Conséquence système** : deux espaces de données distincts (WorldGraph vs Discourse),
  reliés par des opérations de sélection/ordonnancement/focalisation.

## I2. Agents intentionnels

Toute narration implique des entités à états mentaux : buts (Aristote : action ; Greimas :
sujet/objet ; Truby : désir ; BDI/IPOCL : intentions justifiant les actions). Herman :
« l'expérience vécue » comme élément de base. Les récits « sans personnages » (docu
nature, histoire d'objets) fonctionnent par anthropomorphisation — l'audience projette
des intentions, ce qui confirme l'invariant côté récepteur.
**Conséquence** : l'agent (avec buts hiérarchisés désir/besoin) est un objet noyau.

## I3. Valeur : rien ne compte sans axiologie

McKee (changement de valeur = unité minimale) ; Truby (argument moral) ; Drammar
(valeurs en jeu) ; Lehnert (états d'affect ±) ; en QBN les « qualités » jouent ce rôle en
version dégradée. Un événement sans charge de valeur pour personne (une pierre roule) n'est
pas narratif ; le même événement devient narratif dès qu'une valeur s'y attache (la pierre
scelle la sortie de la grotte).
**Conséquence** : chaque delta d'état porte une évaluation sur un ou plusieurs axes de
valeur, relative à chaque agent — pas de valeur « objective » unique.

## I4. Causalité chargée

Aristote (nécessité/vraisemblance) ; Forster (« the king died, then the queen died of
grief ») ; fabula model (arêtes causes/enables/motive) ; IPOCL (liens causaux +
intentionnels vérifiés). Les récits « acausals » apparents (Beckett, dream logic)
maintiennent une causalité thématique ou émotionnelle que le récepteur reconstruit.
**Conséquence** : toute transition d'état doit être rattachée à ≥1 arête causale typée
(physique, psychologique, sociale, thématique) — vérifiable par le moteur de cohérence.

## I5. Conflit / incompatibilité de mondes

Ryan : conflit = incompatibilité entre mondes privés (W/K/O-worlds) et monde actuel ;
Truby : attaque de la faiblesse ; CPOCL : interférence entre plans ; Egri (*The Art of
Dramatic Writing*, 1946) : la « prémisse » prouvée par le conflit. Le **dilemme** en est
le cas interne : deux obligations/désirs d'un même agent mutuellement exclusifs
(Ryan : conflit O-world/W-world ; cf. « dilemma-based narrative » de Barber & Kudenko,
2007).
**Conséquence** : le conflit est un objet **dérivé, calculable** (détection
d'incompatibilité entre buts/plans/valeurs), pas un objet saisi à la main.

## I6. Asymétrie d'information

Aristote (anagnorisis) ; suspense/surprise/curiosité comme les trois régimes de la
disposition de l'information (Sternberg, 1978) ; ironie dramatique = audience sait,
personnage non ; secret, mensonge, révélation, quiproquo. En IA : croyances imbriquées de
Sabre ; gestion du modèle de l'audience de Suspenser.
**Conséquence** : une couche épistémique par agent **plus l'audience comme agent
épistémique**, avec opérateurs {cacher, révéler, mentir, déduire}. Le « twist » devient
une opération formelle : révélation qui force la ré-évaluation causale d'un passé connu.

## I7. Engagement et dette narrative

Setup/payoff (McKee) ; « Chekhov's gun » ; promesse au lecteur (genre) ; O-worlds de
Ryan (obligations) ; serments/contrats comme moteurs universels (du *Roi Lear* au conte).
La narratologie computationnelle ne la réifie pas (manque identifié en
`03-recherche-ia.md` §5) — nous le faisons.
**Conséquence** : objet **Engagement** (promesse, dette, serment, annonce, Chekhov) avec
créancier, débiteur, échéance ; la **dette narrative globale** (engagements ouverts non
soldés) devient une mesure pilotable : trop basse = platitude, jamais soldée = frustration.

## I8. Disruption et rétablissement

Todorov (équilibre→déséquilibre→équilibre') ; Herman (world disruption) ; Propp
(méfait/manque comme fonction déclenchante) ; Campbell (appel) ; Bremond (potentialité
ouverte).
**Conséquence** : la narrativité d'un état se mesure à son **écart aux équilibres**
(homéostasies des agents et du monde) ; le moteur de progression maintient cet écart
au-dessus de zéro tant que le récit doit continuer.

## I9. Transformation irréversible

Campbell/Vogler (renaissance) ; Truby (self-revelation = mise à jour de croyance sur
soi) ; McKee (arc = trajectoire de valeurs) ; Field (plot points comme portes sans
retour) ; Ceptre (ressources linéaires consommées). Les récits « statiques » (sitcom
classique) confirment par contraste : la réinitialisation y est un choix de genre, codé
comme contrainte.
**Conséquence** : distinguer deltas **réversibles** et **irréversibles** ; un arc =
chaîne de deltas irréversibles sur l'identité/croyances d'un agent.

## I10. Tension = incertitude × enjeu, calculée chez le récepteur

Sternberg (suspense/curiosité/surprise) ; Cheong & Young, O'Neill & Riedl (calcul sur le
modèle de l'audience) ; Murray (agency = enjeux des actions) ; Ryan (tellability).
**Conséquence** : la tension n'est pas un scalaire d'ambiance mais une fonction
`f(incertitude sur les futurs accessibles, valeur en jeu, proximité)` évaluée **sur le
storyworld du récepteur** (I6). Multi-dimensionnelle (suspense, mystère, anticipation
d'ironie).

## I11. Séquence processuelle minimale

Bremond : potentialité → actualisation (ou abstention) → achèvement (succès/échec).
Recouvre le gap de McKee (attente→résultat→écart), la boucle but-plan-action de BDI, la
structure but/tentative/issue des story grammars.
**Conséquence** : le patron d'exécution du moteur de progression est cette triade,
enchâssable et interruptible — jamais « scène » ni « acte ».

## I12. Tellabilité et sélection

Ryan (tellability) ; Labov (evaluation dans les récits oraux) ; story sifting
(Kreminski). Tout n'est pas également racontable : la sélection de ce qui mérite d'être
raconté est une opération constitutive.
**Conséquence** : moteur de sifting/évaluation qui note des chaînes de deltas
(densité de valeurs, d'irréversibilité, de conflits, de révélations) — utilisé tant pour
générer que pour résumer/mémoriser.

---

## Anti-invariants (conventions à ne jamais coder en dur)

| Convention | Origine | Statut dans le NOS |
|---|---|---|
| 3 actes, plot points paginés | Field, industrie du long-métrage | profil de discours optionnel |
| Scènes, chapitres | médias texte/écran | unités de rendu de la couche discours |
| Ordre des 31 fonctions | Propp (conte russe) | grammaire de genre optionnelle |
| Monomythe en 12/17 étapes | Campbell/Vogler | gabarit de transformation optionnel |
| Fins fermées, happy end | genres | contrainte de genre déclarative |

Ces conventions restent **exprimables** (comme profils/contraintes déclaratifs chargés
par-dessus le noyau), ce qui est exactement la différence entre un OS et une application.

## Récapitulatif : des invariants aux moteurs

| Invariant | Objet(s) d'ontologie | Moteur responsable |
|---|---|---|
| I1 monde ≠ discours | WorldGraph / Discourse | tous / Réalisation |
| I2 agents intentionnels | Agent, Intention | Personnages |
| I3 valeur | Value, charge des deltas | Personnages, Tension |
| I4 causalité | arêtes causales typées | Causalité, Cohérence |
| I5 conflit/dilemme | Conflict (dérivé) | Causalité + Tension |
| I6 asymétrie d'info | Belief, Secret, Revelation ; AudienceModel | Épistémique (dans Cohérence/Tension) |
| I7 engagement/dette | Commitment | Progression |
| I8 disruption | mesures d'équilibre | Progression |
| I9 irréversibilité | flag des deltas ; Arc | Transformation |
| I10 tension | TensionVector | Tension |
| I11 triade processuelle | patron Bremond | Progression |
| I12 tellabilité | scores de chaînes | Mémoire (sifting) |
