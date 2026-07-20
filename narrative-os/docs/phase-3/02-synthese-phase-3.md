# Phase 3 — Synthèse, questions ouvertes, gate Phase 4

## 1. Livré

1. **Q8 tranchée sur pièces** : noyau de 9 prédicats + extensions déclarées ; les trois
   mondes re-convertis en `nos-0.2` (assertions machine + acteurs sur les 34 deltas),
   schéma normatif mis à jour.
2. **Paquet `kernel/`** (Python pur, zéro dépendance) : `model`, `vocabulary`,
   `validation`, `causality`, `store` (event sourcing + time-travel + rollback),
   `coherence` (gardien de commit, 12 règles de refus motivés, sensibles aux
   révélations).
3. **Suite de tests noyau** (`tools/run_kernel_tests.py`) : **23 tests verts** — rejeu
   intégral des 3 mondes (34 commits, 0 refus), état final et time-travel vérifiés,
   rollback, les 12 règles du catalogue testées une à une sur des deltas corrompus, et
   la double épreuve « refusé avant révélation / accepté après ».
4. **Compatibilité intégrale** : la suite Phase 2 reste verte (26/26) via délégation ;
   la CLI `validate.py` fait désormais conformité statique **et** rejeu complet.

Total : **49 tests verts**, toujours aucune dépendance externe, aucun LLM nulle part.

## 2. Ce que l'implémentation a appris

- **Le gardien épistémique a corrigé le corpus** (acteur erroné sur d6 de la Cité
  d'Ambre) dès son premier rejeu — la valeur du refus motivé est démontrée sur nos
  propres données avant même d'affronter un générateur.
- **Sémantique précisée : l'irréversibilité est narrative, pas factuelle** (l'état
  « détenue » finit, l'arrestation demeure). Le flag contraint arcs et futurs, pas
  l'algèbre d'assertions.
- **La révélation comme clé d'accès épistémique** donne gratuitement la mécanique
  quiproquo/résolution : aucun objet supplémentaire n'a été nécessaire.

## 3. Questions ouvertes

- **Q3 (profondeur épistémique imbriquée)** : inchangée, à traiter en Phase 5 sur le
  même store (contextes préfixés, profondeur 2 par défaut).
- **Q5 (fonction de tension)** : attend toujours E3 (lecteurs humains).
- **Q10 (nouvelle) — compilation des préconditions de mécaniques** : quel langage de
  motifs sur les triplets + objets narratifs (engagements ouverts, relations, charges
  cumulées) ? Candidat : conjonctions de motifs `(s, p, o)` avec variables + prédicats
  dérivés (`dette-ouverte(A)`, `sait(A, X)`), style Datalog restreint — à trancher en
  ouverture de Phase 4, sur les 5 mécaniques de la Cité d'Ambre re-jouées.
- **Q11 (nouvelle) — réparation guidée** : le refus doit-il proposer des alternatives
  (« d3 est caché à CORBEAU ; le rendre inférable ou insérer une révélation ») ?
  Prévu Phase 6 ; le catalogue actuel fournit déjà la matière (règle + éléments).

## 4. Gate Phase 3 → Phase 4

Critères d'entrée posés en Phase 2 : Q8 tranchée sur pièces ✅ ; noyau exécutable en
mode symbolique pur ✅ ; corpus rejoué par le gardien sans refus ✅ ; refus motivés
démontrés (catalogue testé, un vrai bug attrapé) ✅.

**La Phase 4 peut s'ouvrir** — moteurs dynamiques :
1. compiler les préconditions de mécaniques (Q10) et rejouer la sélection par état de la
   Cité d'Ambre mécaniquement (le moteur retrouve seul quelles mécaniques étaient
   éligibles à chaque tour) ;
2. Character Engine : appraisal OCC dérivé des deltas perçus (émotions calculées, jamais
   stockées) + délibération BDI minimale ;
3. Tension Engine v0 : dette narrative (engagements ouverts + anticipations non
   résolues) et ironie dramatique détectée, en attendant E3 pour la forme complète de la
   fonction de tension.
