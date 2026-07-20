# Phase 1 — État de l'art : narratologie

Objectif : extraire de chaque théorie ce qu'elle formalise réellement, ses limites, et ce
qu'elle impose (ou interdit) à un moteur narratif universel. La grille de lecture est
toujours la même : **quelle est l'unité de base ? quelle est la force motrice ? qu'est-ce
qui est invariant vs conventionnel ?**

---

## 1. Aristote — *Poétique* (~335 av. J.-C.)

**Apports formels.** Première théorie systémique : le récit est un *mythos* (agencement
des actions), pas une suite d'événements. Concepts opératoires :

- **Causalité nécessaire ou probable** : les événements doivent s'enchaîner « par
  nécessité ou vraisemblance », pas « l'un après l'autre » — c'est la première
  formulation de la différence entre chronologie et intrigue.
- **Péripétie** (renversement de situation) et **anagnorisis** (reconnaissance, passage de
  l'ignorance à la connaissance) : deux opérateurs formels, l'un sur l'état du monde,
  l'autre sur l'état *épistémique* d'un agent.
- **Hamartia** (erreur/faille) : la cause interne du renversement.
- **Catharsis** : l'effet émotionnel visé (pitié + crainte) — le récit est défini par son
  effet sur le récepteur, pas seulement par sa structure.
- Complétude : « début, milieu, fin » = un système fermé de causes.

**Limites.** Normatif (tragédie grecque), centré sur un seul arc, muet sur la narration
non linéaire, l'interactivité, le point de vue.

**Ce qu'on retient pour le NOS.** (a) La causalité comme contrainte de validité, pas comme
décoration. (b) L'anagnorisis prouve que l'état épistémique des agents est une dimension
de premier ordre. (c) L'effet émotionnel du récepteur est une *sortie mesurable* du
système.

---

## 2. Vladimir Propp — *Morphologie du conte* (1928)

**Apports.** Analyse de ~100 contes russes : 31 **fonctions** (méfait, interdiction,
transgression, départ, épreuve, victoire, retour, reconnaissance…) et 7 **sphères
d'action** (héros, agresseur, donateur, auxiliaire, mandateur, princesse, faux héros).
Deux résultats majeurs :

1. Les fonctions sont définies par leur **conséquence dans l'intrigue**, pas par leur
   contenu de surface (un dragon ou un patron abusif remplissent la même fonction de
   « méfait »).
2. Les rôles sont des **positions relationnelles**, pas des personnages : un même
   personnage peut occuper plusieurs sphères.

**Limites.** Corpus mono-genre ; l'ordre des fonctions est quasi fixe (grammaire linéaire) ;
aucune psychologie interne ; les tentatives de généralisation directe (grammaires de
récit, story grammars de Rumelhart 1975) se sont heurtées à la variété des récits non
folkloriques.

**Ce qu'on retient.** La **séparation fonction/surface** (un même opérateur narratif,
mille habillages) et les **rôles comme relations** — deux principes structurants pour
l'ontologie. On rejette en revanche l'idée d'un ordre canonique universel.

---

## 3. Joseph Campbell — *The Hero with a Thousand Faces* (1949)

**Apports.** Le monomythe : séparation → initiation → retour. Lecture comparatiste des
mythes : le récit comme trajectoire de **transformation identitaire** (mort symbolique et
renaissance), franchissement de seuils entre monde ordinaire et monde spécial.

**Limites.** Fortement contesté en anthropologie (généralisation abusive, biais de
sélection) ; prescriptif quand il est utilisé comme gabarit ; ne dit rien de la mécanique
causale fine.

**Ce qu'on retient.** Non pas les 17 étapes, mais l'invariant sous-jacent : **le récit
opère une transformation d'identité/croyance de l'agent**, et cette transformation passe
par des franchissements de seuils (états d'où l'on ne revient pas identique). C'est un
argument pour un « moteur de transformation » distinct du moteur d'événements.

## 4. Christopher Vogler — *The Writer's Journey* (1992)

Adaptation scénaristique de Campbell (12 étapes, 8 archétypes fonctionnels : mentor,
gardien du seuil, ombre, trickster…). **Intérêt** : les archétypes sont explicitement des
**fonctions dramatiques temporaires** (« l'archétype est un masque que porte un
personnage »), ce qui converge avec Propp. **Limite** : gabarit hollywoodien, souvent
appliqué mécaniquement. **Retenu** : rôles = fonctions attachables/détachables aux agents.

---

## 5. Syd Field — *Screenplay* (1979)

**Apports.** Le paradigme en 3 actes avec *plot points* : formalisation industrielle de la
position des renversements. **Limites.** C'est une **convention de surface d'un médium**
(long-métrage ~120 min), pas un invariant : Field lui-même parle en pages/minutes. La
recherche computationnelle qui l'a utilisé comme structure profonde a produit des récits
rigides. **Retenu.** Une seule chose : la notion de **point d'irréversibilité** (le plot
point comme événement qui ferme des futurs possibles) — qu'on réencode comme propriété
causale (réduction de l'espace des états atteignables), pas comme position dans un acte.

---

## 6. Robert McKee — *Story* (1997)

**Apports décisifs pour nous.**

- **La valeur comme substance du récit** : « Le changement de valeur est le battement de
  cœur du récit. » Une unité narrative existe si et seulement si une valeur chargée
  (vie/mort, amour/haine, liberté/servitude, vérité/mensonge) **change de polarité**.
- **Le gap** : le personnage agit selon ses attentes ; le monde répond autrement ;
  l'écart (gap) entre résultat attendu et résultat obtenu force une décision plus risquée.
  C'est une boucle de rétroaction formalisable : `intention → action → réaction du monde
  ≠ attente → réévaluation → nouvelle intention (enjeu ↑)`.
- **Progression des enjeux** : chaque itération du gap engage davantage.
- Distinction texte/sous-texte (ce qui est dit vs ce qui se joue).

**Limites.** McKee raisonne en scènes/séquences/actes (surface cinéma) ; son vocabulaire
de « valeur » reste informel (pas de typologie close).

**Ce qu'on retient.** Le **changement de valeur** comme critère d'existence d'une unité
narrative (fonde notre « delta narratif », cf. `05-ontologie-v0.md`), et la **boucle du
gap** comme moteur de progression des personnages.

---

## 7. John Truby — *The Anatomy of Story* (2007)

**Apports.**

- Le récit comme **argument moral** : le protagoniste a une **faiblesse** (psychologique
  *et* morale — elle fait du tort aux autres), un **besoin** (ce qu'il doit apprendre) vs
  un **désir** (ce qu'il poursuit). Le dénouement est la **révélation de soi**
  (self-revelation) : mise à jour de croyance sur sa propre identité.
- **L'opposition à quatre coins** : le conflit riche n'est pas binaire ; l'antagoniste
  principal est « la personne la mieux placée pour attaquer la faiblesse du héros ».
- La **toile de personnages** (character web) : les personnages se définissent par leurs
  différences relationnelles autour d'un même thème.

**Limites.** Toujours prescriptif ; les « 22 étapes » restent un gabarit linéaire.

**Ce qu'on retient.** (a) La distinction **désir/besoin** = deux buts de niveaux
différents (objet vs identité), essentielle pour des personnages nuancés. (b) Le conflit
comme **attaque de la faiblesse** : le système doit savoir *cibler* les vulnérabilités.
(c) Le réseau de personnages comme graphe de contrastes thématiques.

---

## 8. Marie-Laure Ryan — *Possible Worlds, AI and Narrative Theory* (1991), *Avatars of Story* (2006)

**Apports fondamentaux (la plus directement computationnelle).**

- **Sémantique des mondes possibles** : un récit = un monde réel textuel (TAW) + les
  **mondes privés** des personnages : monde de croyance (K-world), de souhait (W-world),
  d'obligation (O-world), mondes fantasmés (F-worlds). **Le conflit se définit comme
  incompatibilité entre ces mondes** (entre le W-world d'un agent et le TAW, ou entre les
  W-worlds de deux agents, ou entre W-world et O-world d'un même agent → dilemme).
- **Narrativité scalaire et tellability** : être un récit n'est pas binaire ; certains
  enchaînements sont plus « racontables » (tellability) que d'autres.
- Typologie de l'**interactivité** (interne/externe × exploratoire/ontologique) et le
  « narrative paradox » : tension entre agentivité de l'utilisateur et contrôle auctorial.

**Limites.** Cadre descriptif, pas d'algorithme ; la tellability reste qualitative.

**Ce qu'on retient.** La **définition formelle du conflit et du dilemme** par
incompatibilité de mondes privés — c'est la meilleure base théorique existante pour notre
couche épistémique/motivationnelle, et elle est convergente avec BDI (cf.
`03-recherche-ia.md`).

---

## 9. David Herman — *Story Logic* (2002), *Basic Elements of Narrative* (2009)

**Apports.** Narratologie cognitive : le récit est un **storyworld** — un modèle mental
que le récepteur construit et met à jour. Quatre éléments de base : situatedness,
event sequencing, worldmaking/world disruption, « what it's like » (qualia, l'expérience
vécue). Le récit prototypique = **une perturbation d'un état d'équilibre, vécue par une
conscience**.

**Ce qu'on retient.** (a) Le récepteur maintient un modèle du monde ⇒ le système doit
modéliser **le storyworld du lecteur** (ce que l'audience sait/croit) comme un agent
épistémique de plus — c'est la clé du suspense et de l'ironie dramatique. (b) La
« disruption » comme condition de narrativité (converge avec Todorov : équilibre →
déséquilibre → nouvel équilibre).

---

## 10. Janet Murray — *Hamlet on the Holodeck* (1997)

**Apports.** Propriétés des médias numériques (procédural, participatif, spatial,
encyclopédique) et esthétiques associées : **immersion, agency, transformation**.
L'« agency » = la satisfaction de voir ses actions produire des effets significatifs.

**Ce qu'on retient.** L'agency impose que les actions de l'utilisateur produisent des
**conséquences chargées en valeur** (pas seulement des effets mécaniques) — contrainte de
conception pour le moteur de conséquences en mode interactif.

## 11. Henry Jenkins — « Game Design as Narrative Architecture » (2004)

**Apports.** Le récit n'est pas forcément un flux : il peut être **spatialisé**
(environmental storytelling), **embarqué** (embedded : des traces à reconstituer),
**émergent** (des systèmes qui produisent des histoires), **évoqué**. **Ce qu'on
retient.** La distinction embarqué/émergent structure notre moteur de progression : le
NOS doit servir les deux régimes — contenu pré-auteurisé déclenché par conditions, et
récit émergent des interactions d'agents — et Jenkins montre qu'ils coexistent dans une
même œuvre.

---

## 12. Compléments indispensables (hors liste initiale, justifiés)

Conformément à la méthodologie (« ne pas réinventer, chercher les invariants »), quatre
références manquantes à la liste sont intégrées car elles fournissent des formalisations
plus directement opérationnelles :

- **Gérard Genette, *Figures III* (1972)** : séparation histoire/récit/narration ; ordre
  (analepse/prolepse), durée, fréquence, **focalisation** (qui perçoit) et voix (qui
  raconte). Indispensable pour découpler le monde (fabula) du discours (sjužet) — décision
  D1/D5 du README.
- **Claude Bremond, *Logique du récit* (1973)** : toute séquence narrative élémentaire =
  **potentialité → passage à l'acte (ou non) → achèvement (succès/échec)**. Les récits
  sont des enchâssements/enchaînements de ces triades. C'est la brique de séquencement la
  plus petite et la plus universelle proposée par la narratologie structurale.
- **Tzvetan Todorov (1969)** : équilibre → transgression → déséquilibre → réaction →
  nouvel équilibre (transformé). Converge avec Herman (disruption).
- **Algirdas J. Greimas (1966)** : le **modèle actantiel** (sujet/objet, destinateur/
  destinataire, adjuvant/opposant) généralise les sphères de Propp en pure structure
  relationnelle de forces autour d'un but.

---

## 13. Tableau comparatif

| Théorie | Unité de base | Force motrice | Invariant réutilisable | Piège à éviter |
|---|---|---|---|---|
| Aristote | action agencée | causalité + hamartia | causalité nécessaire ; anagnorisis (épistémique) ; effet récepteur | normativité tragique |
| Propp | fonction | méfait/manque | fonction ≠ surface ; rôle = relation | ordre canonique |
| Campbell/Vogler | étape du voyage | appel/transformation | transformation identitaire ; seuils ; archétype = masque | gabarit universel |
| Field | acte / plot point | structure | irréversibilité des tournants | penser en actes/pages |
| McKee | changement de valeur | le gap attente/résultat | **valeur** ; boucle du gap ; enjeux croissants | penser en scènes |
| Truby | étape morale | faiblesse/besoin vs désir | désir vs besoin ; conflit = attaque de la faiblesse ; toile de personnages | 22 étapes linéaires |
| Ryan | monde possible | incompatibilité de mondes | **conflit/dilemme formalisés** ; tellability ; mondes privés K/W/O | rester descriptif |
| Herman | storyworld | disruption | modèle mental du récepteur ; qualia | pas d'algorithme |
| Murray | affordance du médium | agency | conséquences signifiantes des actions | tech-centrisme |
| Jenkins | espace narratif | exploration | embarqué vs émergent | opposer récit et jeu |
| Genette | relation histoire/discours | — | fabula ≠ sjužet ; focalisation | confondre les niveaux |
| Bremond | triade processuelle | choix d'actualisation | plus petite séquence universelle | — |
| Greimas | actant | quête | structure relationnelle des forces | abstraction stérile |

**Conclusion.** Aucune théorie ne fournit à elle seule un modèle exécutable, mais leurs
recouvrements sont massifs et convergent vers un petit noyau d'invariants (agents
intentionnels, valeurs, causalité, asymétrie d'information, transformation, disruption,
double niveau monde/discours). Ces invariants sont consolidés et démontrés par
croisement dans [`04-invariants.md`](04-invariants.md).
