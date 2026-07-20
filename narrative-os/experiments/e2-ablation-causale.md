# E2 — Rejouabilité causale : requêtes « pourquoi ? » et tests d'ablation

Protocole : sur les annotations E1, (a) vérifier que le graphe causal répond à
« pourquoi X ? » par remontée d'arêtes ; (b) retirer un delta et vérifier que la rupture
des chaînes aval est **détectée** (un delta devient orphelin s'il perd toutes ses causes
psy/phy — les arêtes `them` seules ne suffisent pas à causer).

## E2.1 — Requêtes « pourquoi ? »

| Requête | Remontée obtenue | Verdict |
|---|---|---|
| Fable : pourquoi d7 (chute du fromage) ? | d7 ←phy d6 ←psy d5 ←psy{d4, flaw} ←psy d3 ←psy d2 ←psy d1 | ✅ chaîne complète, bifurquée sur la flaw (réponse « à cause de la vanité ET de la flatterie ») |
| Fable : que rend possible d3 (intention cachée) ? | descendants : d4→d5→d6→d7→d8 ; + ironie dramatique (état épistémique persistant d3..d8) | ✅ les effets épistémiques sont des descendants au même titre que les physiques |
| BB : pourquoi d10 (première cuisson) ? | d10 ←psy d7 ←psy{d3, d5, d6, d2} ; ←phy d9 | ✅ le nœud d7 concentre 4 causes — la remontée restitue la surdétermination du tournant |
| BB : pourquoi d15 (« Walt, c'est bien toi ? ») ? | d15 ←psy{d10, d12} — SKYLER perçoit l'effet sans accéder aux causes (hidden) | ✅ la requête distingue « cause réelle » et « cause connaissable par SKYLER » (∅) : c'est exactement la mécanique du soupçon |
| Cité d'Ambre : pourquoi d10 (se livrer) ? | d10 ←psy d9 ←psy d8 ←soc d6 ←psy d4 (choix 1) | ✅ la responsabilité du joueur est traçable : son choix d4 est un ancêtre causal de la capture de MIRA — base formelle du « c'est ta faute » ressenti |

## E2.2 — Ablations

| Ablation | Effet attendu | Effet constaté sur le graphe | Verdict |
|---|---|---|---|
| Fable − d4 (flatterie) | tout s'effondre | d5 orphelin (sa seule cause psy externe disparaît, la flaw seule est une disposition, pas un déclencheur) → d6, d7, d8, d9 en cascade ; c1 (morale) insolvable | ✅ rupture détectée dès d5 |
| Fable − d8 (révélation) | l'histoire survit mais la fable meurt | d1..d7 intacts ; d9 orphelin ; c1 (contrat de genre) reste **ouvert** à la clôture → violation détectable par la mesure de dette | ✅ cas subtil correctement discriminé : c'est la *complétude* qui casse, pas la causalité |
| BB − d3 (diagnostic) | le pilote s'effondre | d4 orphelin ; d7 perd 2 de ses 4 causes (d3 direct + d5 qui dépendait de d3 psy) ; d5 dégénère en anecdote (info inerte, charge anticipée nulle) | ✅ et la dégradation de d5 en « événement non narratif » (charge→0) confirme I3 : sans valeur en jeu, l'événement sort du récit |
| BB − d6 (aperçu de Jesse) | l'intention survit, le plan précis meurt | d7 garde 3 causes (intention maintenue) mais d8 (recrutement de JESSE) orphelin → toute la branche d10..d15 doit être re-dérivée avec un autre partenaire | ✅ distingue « tournant nécessaire » (d3) et « contingence de réalisation » (d6) — distinction théorisée par Bremond (choix d'actualisation) et retrouvée mécaniquement |
| Cité d'Ambre − d4 (choix 1 : accepter MIRA) | la culpabilité disparaît | d6 perd sa cause psy (MIRA absente du vol) → d8, c3, d9, d10 sans objet ; la session dégénère en transaction (voler-payer) sans dilemme | ✅ démontre que l'agency du choix 1 portait TOUTE la charge morale de la session — mesure C2 confirmée |

## Conclusions E2

1. **Critère de gate atteint** : les deux familles de requêtes fonctionnent sur les
   trois récits ; les ablations cassent exactement ce qu'elles doivent casser, et la
   détection est mécanique (orphelinage + dette insolvable + charges nulles).
2. Résultat non prévu : l'ablation discrimine **nécessité dramatique** (d3) vs
   **contingence** (d6) — piste pour une mesure de « criticité » d'un delta (nombre de
   descendants pondéré par charges) utile au Progression Engine et au sifting (E5+).
3. Règle confirmée pour la Phase 2 : une **disposition** (flaw, valeur, relation) est
   co-cause mais jamais cause suffisante — il faut toujours un déclencheur événementiel.
   (Formulation à inscrire dans la sémantique opérationnelle des arêtes psy.)
4. La complétude narrative (fable − d8) relève de la **dette**, pas de la causalité :
   confirme la séparation des moteurs Coherence (validité) / Progression (complétude).
