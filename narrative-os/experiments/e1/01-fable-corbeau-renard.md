# E1.1 — *Le Corbeau et le Renard* (La Fontaine, 1668) en ontologie v0

Récit minimal fermé. Texte source : domaine public. Annotation complète (grain fin).

## Entités et agents

```yaml
entities:
  fromage: {kind: objet, props: {comestible: true}}
  arbre:   {kind: lieu}

agents:
  CORBEAU:
    beliefs: [ "je tiens un fromage", "mon plumage est beau (incertain, à confirmer)" ]
    desires:
      want: "être admiré"            # désir conscient (objet : l'admiration)
      need: "juger la flatterie avec lucidité"   # besoin, inconscient
    values: [ {axe: estime-de-soi, poids: 3}, {axe: subsistance, poids: 2} ]
    flaw: "vanité = croyance protégée : « les compliments qu'on me fait sont sincères »"
  RENARD:
    beliefs: [ "le corbeau tient un fromage", "le corbeau est vaniteux" ]   # théorie de l'esprit
    desires: { want: "obtenir le fromage" }
    values: [ {axe: subsistance, poids: 3}, {axe: verite-mensonge, poids: -1} ]  # la ruse prime
  AUD: {kind: AudienceModel, genreContract: [ "fable ⇒ une morale sera délivrée" ]}

valueAxes: [ subsistance, estime-de-soi, verite-mensonge, lucidite-aveuglement ]
```

## Fabula en deltas

```yaml
deltas:
  d1: {change: "CORBEAU possède fromage, perché sur arbre",
       causes: [], charges: [{CORBEAU, subsistance, +, 1}],
       scope: {obs: [CORBEAU, RENARD, AUD]}, irr: false}          # état d'équilibre initial

  d2: {change: "RENARD forme le désir du fromage",
       causes: [{psy, d1}],                                       # « alléché par l'odeur »
       charges: [{RENARD, subsistance, +, 1}],                    # gain anticipé
       scope: {obs: [RENARD, AUD], hidden: [CORBEAU]}, irr: false}

  d3: {change: "RENARD adopte l'intention : obtenir le fromage PAR flatterie",
       causes: [{psy, d2}, {psy, belief: "le corbeau est vaniteux"}],
       charges: [{RENARD, verite-mensonge, -, 1}],
       scope: {obs: [RENARD, AUD], hidden: [CORBEAU]}, irr: false}
       # ⇒ SECRET s1 ; ⇒ IRONIE DRAMATIQUE : AUD sait, CORBEAU non (I6)

  d4: {change: "RENARD flatte : « votre ramage égale votre plumage » (assertion fausse-en-intention)",
       causes: [{psy, d3}],
       charges: [{CORBEAU, estime-de-soi, +, 2}],                 # charge illusoire
       scope: {obs: [CORBEAU, RENARD, AUD]}, irr: false}          # ⇒ LIE l1 installée

  d5: {change: "CORBEAU croit la flatterie (misbelief : « il est sincère, je chante bien »)",
       causes: [{psy, d4}, {psy, flaw: CORBEAU.vanité}],          # la faiblesse est la co-cause (Truby)
       charges: [{CORBEAU, lucidite-aveuglement, -, 2}],
       scope: {obs: [CORBEAU], inferable: [RENARD, AUD]}, irr: false}

  d6: {change: "CORBEAU ouvre un large bec pour chanter (tentative : obtenir l'admiration)",
       causes: [{psy, d5}],                                       # triade de Bremond : actualisation
       charges: [{CORBEAU, estime-de-soi, +, 1}],
       scope: {obs: [tous]}, irr: false}

  d7: {change: "le fromage tombe ; RENARD s'en saisit",
       causes: [{phy, d6}],                                       # conséquence physique
       charges: [{CORBEAU, subsistance, -, 2}, {CORBEAU, estime-de-soi, -, 2},
                 {RENARD, subsistance, +, 2}],
       scope: {obs: [tous]}, irr: true}                           # achèvement : succès RENARD / échec CORBEAU

  d8: {change: "RENARD révèle la manœuvre : « tout flatteur vit aux dépens de celui qui l'écoute »",
       causes: [{psy, d7}, {them, d3}],                           # lie le succès au secret initial
       charges: [{CORBEAU, estime-de-soi, -, 1}, {AUD, verite-mensonge, +, 1}],
       scope: {obs: [tous]}, irr: true}
       # ⇒ REVELATION r1 = anagnorisis du CORBEAU : ré-évaluation causale de d4-d6
       #   (le compliment était un moyen) — définition v0 du twist, vérifiée ici

  d9: {change: "CORBEAU met à jour sa croyance sur lui-même et « jure qu'on ne l'y prendrait plus »",
       causes: [{psy, d8}],
       charges: [{CORBEAU, lucidite-aveuglement, +, 2}],
       scope: {obs: [tous]}, irr: true}
       # ⇒ SELF-REVELATION (le need est atteint, au prix du want et du fromage)
       # ⇒ COMMITMENT c2 : serment (débiteur CORBEAU, créancier soi+AUD, échéance ∞)
```

## Objets dérivés — vérification de détectabilité

- **Secret s1** = d3.scope.hidden ∋ CORBEAU sur une intention active → détecté ✅.
- **Conflict k1** (dérivé) : intention RENARD (posséder fromage) incompatible avec état
  possédé-par-CORBEAU → interférence de plans détectable dès d3 ✅. Aucun dilemme : la
  fable est mono-conflit (limite attendue du cas minimal).
- **Ironie dramatique** : `knows(AUD, d3) ∧ ¬knows(CORBEAU, d3)` de d3 à d8 → requête
  épistémique directe ✅ (c'est la source principale de tension : suspense faible,
  anticipation forte).
- **Commitments** : c1 = contrat de genre (fable ⇒ morale ; créancier AUD), **honoré**
  par d8 ; c2 = serment final, laissé **ouvert** (canonique : la fable se clôt sur une
  dette d'apprentissage). Dette narrative : 1→0→1 ✅ mesurable.
- **Arc(CORBEAU)** : chaîne irréversible d7→d8→d9 sur `beliefs`/`identity` :
  aveuglement → lucidité, coût = fromage + humiliation. Seuil : d7. ✅
- **Arc(RENARD)** : aucun delta irréversible sur son identité → personnage plat,
  fonction de donateur-inversé (agresseur au sens de Propp). Conforme : l'ontologie
  n'oblige pas chaque agent à avoir un arc.

## Constats E1.1

1. **Couverture totale** : aucun recours à scène/acte ; les 9 deltas couvrent chaque
   événement signifiant du texte, morale comprise.
2. La **co-causalité flaw + action adverse** (d5 : flatterie × vanité) est exactement la
   « attaque de la faiblesse » de Truby — l'ontologie l'exprime sans objet nouveau.
3. La triade de Bremond apparaît deux fois, enchâssée (tentative RENARD englobe la
   tentative CORBEAU) — le patron d'enchâssement fonctionne.
4. Micro-manque : la charge de d2 est un **gain anticipé**, pas réalisé — l'ontologie v0
   ne distingue pas charges réalisées/anticipées → **amendement A2** (cf.
   `../resultats-et-amendements.md`).
```

Compte d'objets (pour E5) : 4 axes, 3 agents (+AUD), 2 entités, 9 deltas, 1 secret,
1 mensonge, 1 révélation, 2 engagements, 1 conflit dérivé, 2 arcs (dont 1 vide).
