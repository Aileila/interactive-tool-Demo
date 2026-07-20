# Phase 1 — État de l'art : moteurs narratifs existants

Objectif : analyser l'architecture réelle des moteurs cités (et des moteurs de référence
qu'ils impliquent), pour ne rien réinventer et identifier ce qui manque à chacun.
Grille : **modèle de données, unité de contenu, gestion d'état, moteur de progression,
place de la logique narrative, limites.**

---

## 1. Ink (Inkle Studios, open source, 2016)

- **Modèle** : langage de script à flux ; `knots`/`stitches` (nœuds), `diverts`
  (sauts), *weave* (choix imbriqués avec recollement), variables globales, listes.
- **Forces** : excellent pour le **tissage local** (choix → recollement sans explosion
  combinatoire) ; état persistant léger ; runtime portable (JSON compilé) ; prouvé en
  production (*80 Days*, *Heaven's Vault*, *Sorcery!*).
- **Logique narrative** : inexistante en tant que telle — Ink séquence du contenu écrit à
  la main ; toute cohérence causale, émotionnelle, thématique est à la charge de l'auteur.
- **Limite structurante** : le monde n'est pas modélisé (pas d'agents, pas de causalité) ;
  l'état est un sac de variables sans sémantique.

## 2. Yarn Spinner (open source, écosystème Unity)

- **Modèle** : nœuds de dialogue reliés, variables, commandes vers le moteur de jeu.
  Très proche de Twine dans le modèle, orienté dialogue de jeu.
- **Apport/limite** : mêmes conclusions qu'Ink — bon format d'**écriture et de rendu**,
  aucune intelligence narrative. Confirme un pattern : les outils adoptés par l'industrie
  sont ceux qui **restent proches de l'écriture** ; leçon d'ergonomie à retenir pour la
  couche auteur du NOS.

## 3. Twine (Klimas, 2009, open source)

- **Modèle** : hypertexte — passages reliés par liens ; macros et variables (Harlowe,
  SugarCube). Graphe explicite visible par l'auteur.
- **Apport** : démocratisation radicale ; le **graphe de passages** comme représentation
  mentale premier degré. **Limite** : explosion combinatoire des branches ; état faible ;
  aucune séparation monde/discours.

## 4. Ren'Py (open source, visual novels)

- **Modèle** : script Python-like (labels, menus, jumps), persistance et rollback
  intégrés. **Apport** : robustesse de la **persistance d'état** et du retour arrière
  (rollback = time-travel sur l'état — intéressant pour le débogage narratif du NOS).
  **Limite** : même famille qu'Ink/Twine — branchement écrit main, zéro modèle du monde.

## 5. Inform 7 (Graham Nelson, 2006)

Le plus proche d'un « OS narratif » côté modèle du monde :

- **Modèle** : véritable **modèle du monde déclaratif** — objets, **kinds** (héritage),
  **relations n-aires citoyennes de première classe** (« loving relates one person to
  another »), **règles** organisées en rulebooks (before/instead/after), actions avec
  préconditions.
- **Apport majeur** : la preuve qu'un monde riche + des règles déclaratives permettent des
  conséquences émergentes cohérentes ; la déclarativité (langage quasi naturel) le rend
  **explicable** — chaque refus d'action est traçable à une règle.
- **Limites** : aucune couche dramatique (pas de tension, pas d'arcs, pas de valeurs) ;
  la progression reste scriptée (scenes d'Inform = déclencheurs conditionnels).

## 6. Quality-Based Narrative / storylets — StoryNexus, Fallen London (Failbetter), *King of Dragon Pass*, StoryAssembler (Garbe et al., 2019)

- **Modèle** : le contenu est découpé en **storylets** : unités autonomes avec
  (a) **préconditions** sur des **qualités** (variables sémantiques du monde/joueur),
  (b) contenu, (c) **effets** sur les qualités. Le moteur sélectionne à chaque instant
  les storylets éligibles. Références : Failbetter (« qualities »), Emily Short
  (« Storylets: You Want Them », 2019), Kreminski & Wardrip-Fruin, « Sketching a Map of
  the Storylets Design Space » (ICIDS 2018).
- **Apport décisif** : c'est la **seule architecture répandue qui découple contenu et
  progression** — la structure émerge de l'état, pas d'un graphe écrit main. Résout
  l'explosion combinatoire de Twine.
- **Limites** : les qualités sont plates (entiers sans sémantique) ; pas de causalité
  explicite entre storylets ; la cohérence thématique/émotionnelle reste manuelle ;
  StoryAssembler ajoute la planification de séquences mais reste centré contenu.

## 7. Versu (Richard Evans & Emily Short, 2014)

- **Modèle** : simulation sociale à agents — les personnages évaluent les **pratiques
  sociales** (praxis) disponibles via une logique d'exclusion ; chaque agent a désirs,
  humeurs, jugements sur les autres. Article : Evans & Short, « Versu — A Simulationist
  Storytelling System » (IEEE TCIAIG, 2014).
- **Apport** : personnages autonomes crédibles dans des situations sociales ; le récit
  émerge des normes sociales représentées explicitement (« practices » réifiées).
- **Limites** : fort coût d'authoring ; pas de contrôle dramatique global (le récit peut
  être socialement cohérent et dramatiquement plat) ; système propriétaire, éteint.

## 8. Façade (Mateas & Stern, 2005)

- **Modèle** : agents réactifs (langage ABL) + **drama manager** qui séquence des
  **beats** (unités dramatiques avec préconditions/effets) pour suivre une courbe de
  tension cible (arc aristotélicien) ; NLU de surface pour l'entrée libre.
- **Apport** : première démonstration intégrée **agents + gestion dramatique globale** ;
  le beat comme unité à double face (contenu joué / fonction dramatique).
- **Limites** : authoring extrêmement coûteux (~une décennie-homme pour 20 min) ;
  fragile hors de son domaine ; tension modélisée par une seule courbe scalaire.

## 9. « StoryGraph », « Viv », « StoryEngine », « OpenNovel » — état de la documentation

Honnêteté méthodologique (règle : ne jamais affirmer sans justification) :

- **StoryGraph** : le terme recouvre (a) TheStoryGraph.com (recommandation de lectures,
  sans rapport), (b) des travaux académiques de représentation de récits en graphes
  (p. ex. story graphs pour la génération de quêtes, graphes de scènes vidéo). Nous
  retenons l'acception académique : **représentation du récit comme graphe
  d'événements/relations**, traitée dans `03-recherche-ia.md` §5.
- **Viv** : la référence publique la plus proche est Viv Labs (assistant conversationnel,
  racheté par Samsung) dont l'idée clé — *dynamic program generation* : composer
  dynamiquement un plan à partir de capacités déclarées — est transposable au NOS
  (composer une séquence narrative à partir de mécaniques déclarées), mais ce n'est pas
  un moteur narratif. Aucun moteur narratif notable nommé « Viv » n'est documenté dans la
  littérature à notre connaissance.
- **StoryEngine / OpenNovel** : noms génériques portés par plusieurs petits projets
  (bibliothèques de visual novel, outils LLM récents) sans architecture publiée faisant
  référence. → **Question ouverte Q1** (cf. `07-synthese-et-questions-ouvertes.md`) :
  demander au commanditaire quels projets précis il visait, pour ne pas analyser le
  mauvais objet.

## 10. Références complémentaires étudiées (car incontournables)

- **Ceptre** (Chris Martens, 2015) : programmation en **logique linéaire** — les
  ressources consommées/produites modélisent naturellement l'irréversibilité et les
  conséquences. Piste sérieuse pour le moteur de causalité.
- **Comme il Faut / Prom Week** (McCoy et al., 2011-2014) : « physique sociale » —
  ~5 000 règles sociales pondérées, volonté d'agir calculée par considérations
  (influence directe sur notre moteur de personnages).
- **Storyspace / hypertexte littéraire** (Bernstein) : patterns de navigation (cycles,
  contours) — utile pour la couche discours.
- **Dwarf Fortress** (Adams) : récit émergent par simulation profonde sans aucune couche
  dramatique — démontre le plafond du « pur émergent » : des événements riches mais une
  tellability faible (l'histoire doit être *extraite* par le joueur).

---

## 11. Synthèse comparative

| Système | Modèle du monde | Unité de contenu | Progression | Personnages | Logique narrative dans le système ? |
|---|---|---|---|---|---|
| Ink / Yarn / Twine / Ren'Py | non (variables plates) | passage/nœud écrit | graphe/flux écrit main | non | ❌ (tout chez l'auteur) |
| Inform 7 | ✅ riche (kinds, relations, règles) | action simulée | scripts conditionnels | rudimentaires | partielle (monde oui, drame non) |
| QBN / storylets | qualités plates | storylet (précond./effets) | ✅ sélection par état | non | partielle (structure oui, sens non) |
| Versu | modèle social | pratique sociale | émergente | ✅ autonomes | partielle (social oui, drame non) |
| Façade | état dramatique | beat | ✅ drama manager | ✅ réactifs | ✅ mais monolithique et hors de prix |
| Ceptre | ressources logiques | règle linéaire | émergente | non | partielle (causalité oui) |
| Dwarf Fortress | simulation profonde | événement simulé | aucune | simulés | ❌ (aucune couche dramatique) |

**Conclusions architecturales** (reprises dans `06-architecture-v0.md`) :

1. **Personne n'a assemblé les quatre étages** — modèle du monde riche (Inform 7),
   sélection par état (storylets), agents sociaux autonomes (Versu/CiF), gestion
   dramatique globale (Façade). Chaque système en a au plus deux. Le NOS vise l'assemblage
   modulaire des quatre, précisément parce que chacun est déjà validé isolément.
2. **La storylet généralisée est le meilleur candidat d'unité de contenu** : préconditions
   + effets sur un état sémantique. Notre amélioration argumentée : remplacer les
   « qualités » plates par le graphe sémantique multi-couches (les préconditions/effets
   deviennent des motifs de graphe typés, donc explicables et vérifiables).
3. **Le coût d'authoring est le mur** sur lequel Façade et Versu se sont brisés. Toute
   décision d'architecture doit être évaluée aussi sur ce critère ; c'est le rôle légitime
   des LLMs en périphérie (aide à l'authoring, réalisation), jamais au centre.
4. **Le pur émergent ne suffit pas** (Dwarf Fortress) et **le pur scripté ne passe pas à
   l'échelle** (Twine) : il faut les deux régimes de Jenkins (embarqué + émergent) sous un
   arbitre dramatique commun.
