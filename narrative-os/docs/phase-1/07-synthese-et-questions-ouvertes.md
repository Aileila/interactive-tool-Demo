# Phase 1 — Synthèse, questions ouvertes, expériences avant Phase 2

## 1. Synthèse de phase

La Phase 1 a produit, conformément à la méthodologie (recherche avant code) :

1. **État de l'art narratologique** (13 corpus théoriques analysés, grille commune) —
   résultat : aucune théorie n'est exécutable seule, mais leurs recouvrements donnent
   **12 invariants** validés par croisement inter-traditions et résistance aux
   contre-exemples ([`04-invariants.md`](04-invariants.md)).
2. **État de l'art des moteurs** — résultat : quatre étages validés séparément (monde
   riche / sélection par état / agents sociaux / gestion dramatique) mais **jamais
   assemblés** ; la storylet généralisée retenue comme unité de contenu ; le coût
   d'authoring identifié comme risque n° 1.
3. **État de l'art IA** (1977-2025) — résultat : le partage des rôles est net et
   documenté : le symbolique garantit (causalité, épistémique, état), le neuronal propose
   et réalise (surface, variété). D'où l'architecture **neuro-symbolique, LLM en
   périphérie**.
4. **Ontologie v0** — primitive centrale : le **delta narratif** (changement causé,
   chargé en valeur, à portée épistémique, réversible ou non) ; multigraphe 5 couches ;
   contribution originale : **engagements/dettes/secrets réifiés**, absents des
   ontologies existantes.
5. **Architecture v0** — 8 moteurs + noyau + périphérie, contrats d'indépendance,
   testabilité par module, risques et mitigations.

Décisions actées : D1-D5 (voir [`README.md`](../../README.md) §6), chacune sourcée.

## 2. Questions ouvertes (à trancher avant ou pendant la Phase 2)

- **Q1 — Références ambiguës du brief.** « Viv », « StoryEngine », « OpenNovel » ne
  correspondent à aucune architecture publiée faisant référence
  ([`02-moteurs-narratifs.md`](02-moteurs-narratifs.md) §9). Demander au commanditaire
  les projets précis visés ; risque sinon d'analyser le mauvais objet.
- **Q2 — Registre des axes de valeur.** Liste ouverte par agent (fidèle à McKee, mais
  interopérabilité faible) vs registre commun extensible avec mapping par domaine
  (pédagogie ≠ thriller) ? Position provisoire : registre commun minimal + extensions de
  domaine ; à confronter aux récits de référence.
- **Q3 — Profondeur épistémique.** Les croyances imbriquées (A croit que B sait que…)
  explosent vite (cf. Sabre). Quelle profondeur par défaut (2 ? 3 ?) et quel mécanisme
  d'approfondissement à la demande ?
- **Q4 — Granularité temporelle.** Temps continu daté vs tours discrets ? Les médias
  visés divergent (simulation temps réel vs récit rédigé). Piste : temps logique ordonné
  par la causalité, datation optionnelle.
- **Q5 — Tension : forme exacte de la fonction.** I10 donne les facteurs
  (incertitude × enjeu × proximité) mais pas la forme ; nécessite l'expérience E3.
- **Q6 — Mode interactif : arbitrage agency/auteur.** Le « narrative paradox » (Ryan,
  Murray) n'a pas de solution générale ; quel contrat par défaut (le Progression Engine
  garantit les invariants, jamais les issues) ?
- **Q7 — Multilinguisme et culture.** Les invariants sont argumentés trans-culturels,
  mais les profils de genre chargés par défaut sont occidentaux ; prévoir des profils
  (kishōtenketsu, structures orales…) comme données dès la Phase 2 pour tester la
  neutralité du noyau.

## 3. Expériences à mener avant de poursuivre (gate de la Phase 2)

- **E1 — Annotation manuelle de 3 récits contrastés** (une fable, un épisode de série,
  une session de jeu narratif) dans l'ontologie v0. Critère de succès : tout événement
  narrativement signifiant s'exprime en deltas + objets v0 **sans** recourir à
  scène/acte ; les manques observés amendent l'ontologie (méthode SIG d'Elson).
- **E2 — Rejouabilité causale.** À partir de l'annotation E1, vérifier que le graphe
  causal répond correctement à « pourquoi X ? » et « que devient l'histoire si on retire
  le delta D ? » (test d'ablation — un twist retiré doit casser des chaînes en aval).
- **E3 — Tension calculée vs ressentie (pilote).** Faire annoter le suspense ressenti
  (échelle continue) par quelques lecteurs sur les récits E1 ; corréler avec 2-3
  variantes de la fonction de tension calculées à la main. Choisir la forme pour Q5.
- **E4 — Preuve d'indépendance LLM (maquette papier).** Dérouler à la main la boucle
  d'exécution (§1 de l'architecture) sur la fable E1 avec un Realizer à gabarits, zéro
  LLM. Critère : récit lisible et cohérent, même stylistiquement plat.
- **E5 — Coût d'authoring (mesure initiale).** Chronométrer l'annotation E1 ; établir la
  base de référence du risque n° 1 et les cibles d'outillage.

## 4. Critère d'ouverture de la Phase 2

La Phase 2 (formalisation JSON Schema + sémantique opérationnelle) ne s'ouvre que si :
E1 et E2 réussies (l'ontologie couvre les récits de référence et supporte l'ablation
causale), Q1 levée ou explicitement abandonnée, Q2 et Q4 tranchées sur pièces.
