# E4 — Preuve d'indépendance LLM : réalisation à gabarits, déroulé manuel

Objectif (décision D5, contrainte du brief) : démontrer que la boucle d'exécution
(architecture §1) produit un récit **lisible et cohérent sans aucun LLM**, à partir des
seuls deltas + une bibliothèque de gabarits. Le style peut être plat : seule la
cohérence compte.

## Gabarits (extrait de la bibliothèque `Realizer/templates-fr`)

```
T-état        : "{agent} {prédicat-état}."
T-perception  : "{agent} remarque {objet|fait}."
T-intention†  : "{agent} décide de {but}[, en {moyen}]."     † rendu seulement si focalisation interne
T-action      : "{agent} {verbe-action} {complément}."
T-parole      : "« {contenu} », {verbe-dire} {agent}."
T-conséquence : "Alors, {effet}." / "Mais {effet}."          connecteur choisi par la polarité
                                                             des charges (+ → "alors", − pour
                                                             le focalisé → "mais")
T-révélation  : "{agent} comprend alors que {contenu}."
T-serment     : "{agent} se jure que {contenu}."
```

Règles de projection (couche discours) :
1. Ordre = ordre fabula (aucune anachronie pour ce test).
2. Focalisation externe sauf `scope.hidden` ≠ ∅ : un delta caché à un agent présent est
   rendu **sans mention de l'intention** (le discours respecte l'épistémique — c'est le
   Realizer qui applique la focalisation, pas le gabarit).
3. Un delta interne (`psy` pur, non observable) n'est verbalisé que si la focalisation
   interne est accordée à son agent ; sinon il est **omis et laissé inférable** (I6).

## Sortie produite (fable, deltas d1-d9, focalisation externe + interne CORBEAU)

> Le corbeau est perché sur un arbre, un fromage au bec. Le renard remarque le fromage.
> « Que vous êtes joli ! Si votre ramage égale votre plumage, vous êtes le plus beau des
> hôtes de ces bois », dit le renard. Le corbeau croit le compliment sincère. Alors, le
> corbeau ouvre un large bec pour chanter. Mais le fromage tombe, et le renard s'en
> saisit. « Apprenez que tout flatteur vit aux dépens de celui qui l'écoute », dit le
> renard. Le corbeau comprend alors que le compliment n'était qu'un moyen. Le corbeau se
> jure qu'on ne l'y prendra plus.

Remarques de vérification :
- d3 (intention cachée du renard) est **correctement omise** par la règle 2 : le texte ne
  dit jamais « le renard décide de le flatter » — le lecteur l'infère, comme dans
  l'original. La focalisation est un comportement du système, pas un talent du gabarit.
- Le connecteur « Mais » sur d7 provient mécaniquement de la charge négative du focalisé
  (CORBEAU) : la coloration minimale du discours dérive des charges, pas d'un choix
  stylistique.

## Contre-épreuve (session interactive, d5-d8, focalisation interne PJ)

> Anja force la serrure du quai 7 et charge l'ambre. Mais l'alarme est donnée. Anja porte
> les trois cents ambres à Silas : sa dette est soldée. Anja apprend alors que Mira a été
> arrêtée en couvrant sa fuite.

- d6 (l'arrestation de MIRA, `hidden: [PJ]`) n'apparaît **qu'à d8**, au moment où le PJ
  l'apprend — la focalisation interne stricte reproduit d'elle-même la structure
  « coup de théâtre » sans aucune instruction dramatique dans les gabarits.

## Conclusions E4

1. **Critère atteint** : récit lisible, causalement et épistémiquement cohérent, zéro
   LLM. Le style est plat, comme prévu et accepté.
2. Résultat structurant : **focalisation, omission et connecteurs sont des fonctions du
   système** (scope + charges), pas du générateur de phrases. Autrement dit, la frontière
   Realizer/moteurs tient : on peut brancher un LLM à la place des gabarits pour le
   style, il recevra des deltas déjà filtrés par la focalisation — il ne peut
   *structurellement* pas divulguer un secret qu'on ne lui a pas transmis. C'est la
   traduction opérationnelle de « la logique narrative ne vit jamais dans les prompts ».
3. Limite honnête : les gabarits français demandent de la morphologie (accords, élisions)
   — coût d'ingénierie réel mais borné et sans rapport avec la logique narrative ;
   à traiter en Phase 6 (bibliothèques de réalisation par langue).
