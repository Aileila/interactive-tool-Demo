# Phase 2 — Synthèse, architecture mise à jour, questions ouvertes

## 1. Livré

1. **Schéma normatif** [`schema/nos-world.schema.json`](../../schema/nos-world.schema.json)
   (JSON Schema draft 2020-12, version `nos-0.1`) : delta narratif, agents BDI étendus,
   axes de valeur, normes (A1), charges anticipées (A2), entités collectives (A3),
   liaisons joueur (A4), engagements à six forces dont morale (A5), secrets,
   révélations, arcs, mécaniques.
2. **Sémantique opérationnelle** ([`01-semantique-operationnelle.md`](01-semantique-operationnelle.md)) :
   R1/R1b (dispositions et arêtes thématiques ne déclenchent pas), `requires`
   (nécessité) vs causes multiples (surdétermination), sémantique normée d'`ablate`,
   cycle de vie des engagements, règle A4, criticité = portance ≠ nécessité.
3. **Corpus de référence exécutable** [`testdata/`](../../testdata/) : les 34 deltas
   d'E1 convertis en trois mondes conformes (9 + 15 + 10 deltas, 8 engagements,
   3 secrets, 2 révélations, 3 arcs, 5 mécaniques, 2 normes, 1 liaison joueur).
4. **Implémentation de référence** [`tools/nosval.py`](../../tools/nosval.py) (Python
   pur, zéro dépendance) + CLI [`tools/validate.py`](../../tools/validate.py) +
   **suite de conformité** [`tools/run_tests.py`](../../tools/run_tests.py) :
   **26 tests verts** — 3 validations de conformité, 5 requêtes « pourquoi ? »,
   8 assertions d'ablation rejouant E2, 2 assertions de criticité, 5 contre-épreuves
   (le validateur refuse bien les mondes corrompus : R1, scopes, I9, A4, cycle de vie).

## 2. Ce que la formalisation a appris (méthodologie : l'exécution comme arbitre)

- **La suite de tests a attrapé une vraie divergence** : la première implémentation
  laissait la morale de la fable survivre à l'ablation de la flatterie via son arête
  *thématique*. Le texte d'E2 disait l'inverse. Tranché en faveur du texte → règle
  **R1b** promue au rang de norme. C'est exactement le rôle attendu du corpus de
  référence : les documents ne suffisent pas, l'exécutable force les décisions.
- **`requires` est né de la conversion** : en JSON, la distinction entre « d7 a quatre
  causes » et « d7 est impensable sans le diagnostic » n'était pas exprimable — E2
  l'avait vue (nécessité vs contingence), le schéma la porte désormais.
- **La criticité fonctionne mais mesure la portance, pas la nécessité** (crit(d3)=42 >
  crit(d6)=23 sur Breaking Bad) ; les deux notions sont maintenant distinctes et
  outillées (`criticality` vs `requires`).
- **L'agency est effectivement mesurable** (session interactive : crit(choix 1)=23
  contre crit(rumeur)=1) — confirmation chiffrée du constat C2 d'E1.3.

## 3. Architecture mise à jour

Pas de changement de découpage (les 8 moteurs et la périphérie tiennent) ; deux
précisions actées :

- Le **World State Store** (Phase 3) reçoit une exigence d'entrée claire : définir le
  vocabulaire de prédicats des assertions par domaine, seule pièce manquante pour rendre
  `change` entièrement machine.
- Le couple **`requires`/`criticality`** entre au contrat du Progression Engine :
  protéger les deltas à forte portance planifiés, choisir les contingences substituables
  quand une proposition est refusée.

## 4. Questions ouvertes après Phase 2

- **Q5 (fonction de tension)** : inchangée, attend E3 (protocole prêt, lecteurs requis).
- **Q8 (nouvelle) — vocabulaire d'assertions** : ontologie de prédicats unique et
  minimale (situé-à, possède, croit, relation-avec…) ou vocabulaires par domaine avec un
  noyau commun ? Position provisoire : noyau commun (spatial, possession, épistémique,
  social) + extensions déclaratives — à trancher en Phase 3 sur les mêmes trois mondes.
- **Q9 (nouvelle) — anticipations non résolues** : faut-il exiger (avertissement ou
  erreur ?) qu'une charge `anticipated` soit résolue en aval ? V0.1 : avertissement
  futur, jamais erreur (le pilote de série vit de ses anticipations ouvertes).

## 5. Gate Phase 2 → Phase 3

Critères : schéma normatif publié ✅ ; sémantique opérationnelle écrite et exécutée ✅ ;
corpus de référence conforme et suite de conformité verte (26/26) ✅ ; divergences
détectées tranchées et documentées ✅.

**La Phase 3 peut s'ouvrir** : implémentation du noyau symbolique (World State Store en
event sourcing sur les deltas, Causality Engine industrialisant `ancestors`/`ablate`/
`criticality`, Coherence Engine transformant les contrôles de `nosval` en gardien de
commit avec refus motivés), en mode symbolique pur, les trois mondes de `testdata/`
servant de jeu d'intégration. Prérequis d'entrée : trancher Q8 (vocabulaire
d'assertions) sur pièces, en re-convertissant les trois mondes.
