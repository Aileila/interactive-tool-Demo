# E1.3 — *La Cité d'Ambre* : session de jeu narratif synthétique en ontologie v0

Session **entièrement spécifiée ici** (type storylets/QBN, cf. état de l'art §6) : monde
minimal, 5 mécaniques auteurisées, une trace de jeu de 10 deltas avec deux choix joueur.
Objectif : tester le mode interactif — agency (Murray), joueur = agent **et** audience,
sélection par état, contrat de jeu.

## Monde et mécaniques auteurisées

```yaml
agents:
  PJ (ANJA, contrebandière):        # contrôlée par le JOUEUR
    beliefs: [ "je dois 300 ambres au passeur SILAS" ]
    desires: {want: "solder ma dette", need: "décider à qui va ma loyauté"}
    values: [ {axe: loyaute, poids: ?}, {axe: fortune, poids: ?} ]
      # poids « ? » : révélés par les choix du joueur — le système APPREND les valeurs
      # du PJ en observant les charges des deltas choisis (constat C3 ci-dessous)
  SILAS (passeur):  {desires: {want: "récupérer sa créance"}, values: [{axe: fortune, poids: 3}]}
  MIRA (amie, guetteuse): {values: [{axe: loyaute, poids: 3}]}
  GARDE (institution): {kind: entité-collective}
  JOUEUR: {bind: [PJ, AUD]}          # ⇒ amendement A4 : liaison agent+audience

commitments_initiaux:
  c1: {débiteur: PJ, créancier: SILAS, contenu: "300 ambres", échéance: "la nouvelle lune", force: menace}

mécaniques (storylets généralisées — préconditions/effets en motifs de graphe) :
  m1 rumeur-de-cargaison: pré: {dette ouverte} → propose delta "info: cargaison mal gardée"
  m2 offre-de-mira:       pré: {relation(MIRA,PJ)>0 ∧ PJ en difficulté} → propose aide risquée
  m3 coup-de-filet:       pré: {PJ a agi illégalement ∧ GARDE alertée} → menace d'arrestation
  m4 exigence-de-silas:   pré: {échéance proche ∧ dette ouverte} → escalade de la menace
  m5 revente-d-info:      pré: {PJ détient un secret monnayable} → propose trahison lucrative
```

## Trace de session (fabula jouée)

```yaml
d1: {change: "SILAS rappelle la dette et fixe l'échéance (m4)",
     causes: [{soc, c1}], charges: [{PJ, fortune, -, 2, anticipée}],
     scope: {obs: [PJ, SILAS, JOUEUR]}, irr: false}          # disruption : équilibre rompu
d2: {change: "rumeur : cargaison d'ambre mal gardée au quai 7 (m1)",
     causes: [{soc, d1}], charges: [], scope: {obs: [PJ, JOUEUR]}, irr: false}
d3: {change: "MIRA propose de faire le guet, par amitié (m2)",
     causes: [{soc, d2}, {psy, relation MIRA→PJ}],
     charges: [{PJ, loyaute, +, 1}], scope: {obs: [PJ, MIRA, JOUEUR]}, irr: false}
     # ⇒ COMMITMENT c2 implicite : accepter = engager la sécurité de MIRA

d4: {change: "★ CHOIX JOUEUR 1 : accepter l'aide de MIRA (options : seul / avec MIRA / renoncer)",
     causes: [{psy, d1..d3}], charges: [{PJ, loyaute, +, 1}, {MIRA, vie-mort, -, 1, anticipée}],
     scope: {obs: [PJ, MIRA, JOUEUR]}, irr: false}
     # AGENCY : le choix crée une charge sur un TIERS — conséquence signifiante (Murray)

d5: {change: "vol de la cargaison : réussite partielle — l'alarme est donnée",
     causes: [{phy, d4}, {phy, aléa}], charges: [{PJ, fortune, +, 2}, {PJ, legalite, -, 2}],
     scope: {obs: [PJ, MIRA, JOUEUR], inferable: [GARDE]}, irr: true}
d6: {change: "MIRA est identifiée par la GARDE en couvrant la fuite de PJ",
     causes: [{phy, d5}, {psy, d4}],
     charges: [{MIRA, liberte, -, 3}, {PJ, loyaute, -, 2}],
     scope: {obs: [MIRA, GARDE, JOUEUR], hidden: [PJ]}, irr: true}
     # information asymétrique inversée : le JOUEUR (via AUD) sait, le PJ pas encore —
     # l'ironie dramatique fonctionne AUSSI contre le personnage-joueur ✅
d7: {change: "PJ solde la dette : c1 honoré",
     causes: [{phy, d5}], charges: [{PJ, fortune, -, 2}, {PJ, liberte, +, 2}],
     scope: {obs: [PJ, SILAS, JOUEUR]}, irr: true}             # dette narrative --
d8: {change: "PJ apprend l'arrestation de MIRA (révélation r1)",
     causes: [{soc, d6}], charges: [{PJ, loyaute, -, 3}],
     scope: {obs: [PJ, JOUEUR]}, irr: false}
     # ⇒ nouvelle dette morale c3 (débiteur PJ, créancier MIRA) NON contractuelle :
     #   naît d'une conséquence, pas d'une promesse — l'objet Commitment couvre ce cas
     #   (force: morale) mais la v0 doit le dire explicitement → amendement A5
d9: {change: "★ CHOIX JOUEUR 2 : (m5) vendre à SILAS l'identité d'un témoin pour payer
              l'avocat de MIRA — ou se livrer à sa place — ou l'abandonner",
     causes: [{psy, d8}, {soc, m5}],
     charges_selon_option: "le DILEMME est le choix lui-même : loyaute vs fortune vs liberte",
     scope: {obs: [PJ, JOUEUR]}, irr: false}
     # choix joué : se livrer à sa place
d10:{change: "PJ se livre ; MIRA libérée ; SILAS empoche la cargaison restante",
     causes: [{psy, d9}], charges: [{PJ, liberte, -, 3}, {PJ, loyaute, +, 3},
                                     {MIRA, liberte, +, 3}],
     scope: {obs: [tous]}, irr: true}
     # SELF-REVELATION implicite : le need (« à qui va ma loyauté ») est tranché EN ACTE
```

## Constats E1.3

- **C1 — La sélection par état fonctionne sur le graphe** : chaque mécanique m1-m5 s'est
  déclenchée par motif (dette ouverte, relation positive, illégalité + alerte…), sans
  aucun graphe de passages écrit main — la généralisation storylet→graphe (décision de
  l'EDA moteurs, §11.2) est validée sur ce cas.
- **C2 — L'agency est mesurable** : magnitude des charges des deltas causés par les choix
  joueur (d4 : 2 ; d9-d10 : 9) — un critère quantitatif pour l'exigence de Murray
  (« conséquences signifiantes »), utilisable par le Progression Engine en mode
  interactif (réponse partielle à Q6).
- **C3 — Les valeurs du PJ sont apprises, pas déclarées** : les poids loyaute/fortune du
  PJ sont estimés par régression sur les charges choisies (d4, d9) — mécanisme nouveau à
  spécifier en Phase 2 (le Character Engine a un mode « observation » pour les agents
  contrôlés par l'humain).
- **C4 — Le dilemme comme choix offert** : en mode interactif, le dilemme n'est pas
  seulement détecté (I5), il est **fabriqué puis délégué** au joueur (d9) — le moteur de
  progression a besoin d'un opérateur « forcer un dilemme et le donner à jouer »
  (mécanique famille 3, déjà prévue ✅).
- **C5 — Amendement A4 confirmé** : le JOUEUR lié à la fois à PJ (agent) et AUD
  (audience) crée le cas `hidden: [PJ]` mais `obs: [JOUEUR]` (d6) — la v0 le représente,
  mais la sémantique de la liaison doit être normée en Phase 2.

Compte d'objets (E5) : 5 axes, 5 agents + JOUEUR lié, 5 mécaniques, 10 deltas,
3 engagements (contractuel, implicite, moral), 1 dilemme joué, 2 révélations, 1 arc PJ.
