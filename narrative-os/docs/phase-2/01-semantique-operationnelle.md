# Phase 2 — Sémantique opérationnelle de l'ontologie v0.1

Ce document est le **contrat sémantique** du format `nos-0.1`
([`../../schema/nos-world.schema.json`](../../schema/nos-world.schema.json)) : ce que les
objets *signifient* et comment les moteurs doivent les interpréter.
[`tools/nosval.py`](../../tools/nosval.py) en est l'implémentation de référence ;
[`tools/run_tests.py`](../../tools/run_tests.py) en est la suite de conformité (les
résultats d'E2 rejoués mécaniquement + contre-épreuves). Toute divergence future entre ce
texte et le code est un bug de l'un des deux.

## 1. Le delta narratif

Un delta est un fait de fabula daté par un **temps logique** `t` (Q4 : ordre, pas date).
Ses quatre faces sont interprétées ainsi :

- `change` : le contenu du changement. En v0.1, `summary` est normatif pour l'humain ;
  les `assertions_*` (triplets) sont la partie machine, **optionnelle** tant que le
  vocabulaire de prédicats par domaine n'est pas fixé (décision reportée à la Phase 3,
  World State Store — reportée en connaissance de cause : E2 a montré que causes, portées
  et charges suffisent aux requêtes visées).
- `causes` : arêtes causales typées (§2).
- `charges` : évaluations axiologiques (§4).
- `scope` : portée épistémique (§5).
- `irreversible` : ferme des futurs (I9) ; condition d'appartenance à un arc.
- `change.attempt` : marque la **triade de Bremond** — ce delta est une tentative dont
  l'issue (succès/échec) est portée par un delta aval.

## 2. Arêtes causales

Chaque cause a un **type** (nature du lien) et une **origine** (exactement une) :

| | `from` (delta) | `disposition` (trait durable) | `commitment` (engagement) | `exogenous` |
|---|---|---|---|---|
| `phy` physique | chute du fromage ← bec ouvert | savoir-faire du chimiste | — | le cancer |
| `psy` psychologique | croire ← flatterie | flaw, croyance, relation | — | — |
| `soc` sociale | menace ← première cuisson | réseau criminel | la dette pèse sur la situation | le ride-along proposé |
| `them` thématique | morale ← intention initiale | — | — | — |

**R1 (disposition ≠ déclencheur).** Une origine `disposition` ou `commitment` est un
état *durable* : elle co-explique mais ne déclenche pas. Tout delta qui a des causes
doit avoir au moins une origine événementielle (`from` ou `exogenous`) — sinon rejet.
(Découverte E2 ; contre-épreuve dans la suite de tests.)

**R1b (les arêtes `them` relient sans causer).** Une arête thématique est une origine
`from` pour la remontée interprétative (« pourquoi, au sens du thème ? ») mais **ne
compte pas** comme cause événementielle : un delta dont il ne reste que des arêtes
`them` est orphelin. (Divergence détectée par la suite de tests lors de l'implémentation
— la fable survivait à l'ablation de la flatterie via l'arête thématique de la morale —
et tranchée dans le sens du texte d'E2.)

**`requires` (préconditions dures).** Distinct des causes : `requires: [dX]` signifie
« ce delta est *inintelligible* si dX n'a pas eu lieu », même si d'autres causes
subsistent (participants introduits par dX, états créés par dX). Promu au rang de champ
du schéma suite à E2 (cas d6 de la Cité d'Ambre, cas d7/d8/d10 de Breaking Bad).
C'est la différence formelle entre **surdétermination** (plusieurs causes, chacune
dispensable) et **nécessité** (précondition dure).

## 3. Requêtes causales normées

- `ancestors(d)` — « pourquoi d ? » : fermeture amont sur les origines `from` (tous
  types, `them` inclus), plus la liste des dispositions et engagements co-causes.
- `ablate(d)` — « que devient l'histoire sans d ? » : retrait de d, puis point fixe :
  un delta est invalidé si (a) un de ses `requires` est retiré, ou (b) toutes ses causes
  événementielles non-`them` de type delta sont retirées et aucune cause `exogenous` ne
  subsiste. Sont rapportés comme **sans objet** : engagements dont `opened_by`/
  `resolved_by` est retiré, révélations et secrets pointant vers des deltas retirés.
- `criticality(d)` (R4, candidate) : somme des magnitudes des charges des deltas
  invalidés par `ablate(d)` + 2 par engagement impacté. **Interprétation stricte :
  mesure de portance (load-bearing), pas de nécessité dramatique** — un delta contingent
  mais situé en amont d'une longue branche (rencontrer Jesse) peut porter beaucoup tout
  en étant remplaçable ; la nécessité se lit dans `requires`, la portance dans
  `criticality`. Les deux mesures servent le Progression Engine à des fins différentes
  (protéger vs pouvoir substituer).

## 4. Charges

`{agent, axis, polarity, magnitude 1-3, mode}` — l'évaluation d'un delta sur un axe de
valeur, **relative à un agent** (I3 : pas de valeur objective unique).

- `mode: realized` : l'effet est advenu.
- `mode: anticipated` (A2) : l'effet est projeté — c'est le matériau formel de l'espoir
  (`+`) et de la peur (`-`) au sens OCC, et l'assiette du calcul de suspense (I10) quand
  l'agent porteur est l'audience.
- Discipline v0.1 (non bloquante, vérifiée en avertissement futur) : une charge
  anticipée devrait être *résolue* en aval (réalisée, évitée ou annulée) — une
  anticipation jamais résolue est une dette d'attente, comptabilisée par le moteur de
  tension avec les engagements ouverts.

## 5. Portées épistémiques et liaison joueur

- `observed` ⊥ `hidden` (disjoints, vérifié) ; `inferable` : accessible par inférence
  sans observation directe (statut validé en E1 : soupçon de Skyler, alerte de la
  Garde).
- L'audience (`kind: audience`) est un sujet épistémique ordinaire ; **tout monde doit
  en déclarer au moins une** (I6) — vérifié.
- **A4 (liaison joueur)** : pour toute liaison `{player, agent, audience}` :
  `agent ∈ observed ⇒ audience ∈ observed`. L'inverse est permis (le joueur peut savoir
  ce que son personnage ignore — ironie dramatique contre le PJ, cas d6 d'Ambre).
  Vérifié, contre-épreuve incluse.
- Ironie dramatique = invariant épistémique dérivable : `∃d : AUD ∈ observed(d) ∧
  a ∈ hidden(d)` persistant tant qu'aucune révélation ne l'éteint.

## 6. Cycle de vie des engagements

```
                    ┌── honored  (resolved_by requis)
open ──(delta)──────┼── betrayed (resolved_by requis)
  ↑                 └── cancelled(resolved_by requis)
  opened_by optionnel (absent = antérieur au récit)
```

Contraintes vérifiées : `open` ⇒ pas de `resolved_by` ; état terminal ⇒ `resolved_by`
présent et `t(resolved) ≥ t(opened)` ; `force ≠ genre` ⇒ `debtor` requis ;
`deadline` est le **seul objet temporel daté** du format (Q4). La **dette narrative**
d'un état = ensemble des engagements `open` (+ anticipations non résolues, §4) —
c'est la mesure que le Progression Engine pilote (I7) et que la clôture doit solder ou
assumer (le serment final de la fable reste ouvert : c'est un choix de genre, pas une
erreur).

## 7. Secrets, révélations, arcs, mécaniques

- Secret : `revealed_by` strictement postérieur à `opened_by` (vérifié). Un secret non
  révélé à la clôture est licite (Breaking Bad, pilote) — il compte dans la dette.
- Révélation : `reveals_delta` doit être antérieur au delta porteur (on ne révèle que du
  passé) ; `twist: true` = anagnorisis, la révélation force la ré-évaluation causale
  d'un passé montré.
- Arc : tous ses deltas sont `irreversible` (I9, vérifié) ; `thresholds` et
  `self_revelation` appartiennent à l'arc.
- Mécanique : en v0.1 les préconditions restent des chaînes semi-structurées
  (documentation d'intention) ; leur compilation en motifs de graphe exécutables est un
  livrable de la Phase 3/4 — assumé, car dépendant du vocabulaire d'assertions.

## 8. Ce que v0.1 ne formalise volontairement pas

| Reporté | Vers | Raison |
|---|---|---|
| Vocabulaire de prédicats des assertions | Phase 3 | dépend du World State Store et des domaines |
| Compilation des préconditions de mécaniques | Phase 3/4 | dépend du vocabulaire ci-dessus |
| Émotions OCC dérivées | Phase 4 (Character Engine) | dérivées, jamais stockées — les stocker en v0.1 créerait la double vérité qu'on interdit |
| Couche discours (ordre, focalisation) | Phase 6 | I1 : espace distinct ; E4 en a validé le principe |
| Forme de la fonction de tension | après E3 | Q5 — expérimentale, pas décidable sur table |
