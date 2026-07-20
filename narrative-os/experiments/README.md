# Expériences de validation de l'ontologie v0 (gate Phase 1 → Phase 2)

Protocole défini en [`../docs/phase-1/07-synthese-et-questions-ouvertes.md`](../docs/phase-1/07-synthese-et-questions-ouvertes.md) §3.

## Contenu

| Exp. | Objet | Fichier(s) | Statut |
|---|---|---|---|
| **E1** | Annotation de 3 récits contrastés dans l'ontologie v0 | [`e1/01-fable-corbeau-renard.md`](e1/01-fable-corbeau-renard.md), [`e1/02-episode-breaking-bad-s01e01.md`](e1/02-episode-breaking-bad-s01e01.md), [`e1/03-session-jeu-cite-ambre.md`](e1/03-session-jeu-cite-ambre.md) | ✅ |
| **E2** | Rejouabilité causale (requêtes « pourquoi ? » + ablation) | [`e2-ablation-causale.md`](e2-ablation-causale.md) | ✅ |
| **E3** | Tension calculée vs ressentie | protocole rédigé (§E3 de [`resultats-et-amendements.md`](resultats-et-amendements.md)) | ⏸ requiert des lecteurs humains |
| **E4** | Preuve d'indépendance LLM (Realizer à gabarits, déroulé manuel) | [`e4-realisation-sans-llm.md`](e4-realisation-sans-llm.md) | ✅ |
| **E5** | Mesure du coût d'authoring (base de référence) | §E5 de [`resultats-et-amendements.md`](resultats-et-amendements.md) | ✅ |

Résultats consolidés, amendements v0 → v0.1 et décision de gate :
[`resultats-et-amendements.md`](resultats-et-amendements.md).

## Format d'annotation E1

Chaque récit est annoté avec les objets de
[`../docs/phase-1/05-ontologie-v0.md`](../docs/phase-1/05-ontologie-v0.md) :

- `entities` / `agents` (BDI étendu : beliefs, want/need, values, flaw) ;
- `valueAxes` utilisés (registre commun + extensions de domaine — test de Q2) ;
- `deltas` : la fabula entière en deltas narratifs `d1..dn`, chacun avec
  `change`, `causes` (arêtes typées `phy` physique / `psy` psychologique / `soc`
  sociale / `them` thématique, pointant vers des deltas amont), `charges`
  (agent, axe, polarité, magnitude 1-3), `scope` (observé/caché/inférable —
  l'audience `AUD` est un agent épistémique comme les autres), `irr` (irréversible) ;
- `commitments`, `secrets`, `revelations`, `conflicts` (dérivés — on vérifie qu'ils
  sont *détectables* depuis les deltas, pas posés arbitrairement), `arcs`.

**Critère de succès E1** : tout événement narrativement signifiant s'exprime dans ce
vocabulaire **sans** recourir à scène/chapitre/acte ; tout manque est consigné comme
amendement candidat, jamais contourné en silence.

## Choix des trois récits (justification)

1. **Fable** (*Le Corbeau et le Renard*, La Fontaine, 1668) : cas minimal fermé, domaine
   public, canonique — teste le noyau (mensonge, ironie dramatique, anagnorisis, morale).
2. **Épisode de série** (*Breaking Bad* S01E01, pilote, 2008) : récit long-format
   moderne — teste disruption, secret structurel, seuils irréversibles, normes sociales,
   charges anticipées. (Annotation analytique de l'intrigue, grain grossier : ~15 deltas.)
3. **Session de jeu narratif** (*La Cité d'Ambre*, session synthétique de type
   storylets/QBN, entièrement spécifiée ici) : mode interactif — teste l'agency
   (Murray), le joueur à la fois agent et audience, la sélection par état. Synthétique
   à dessein : la trace est intégralement contrôlée, donc vérifiable.
