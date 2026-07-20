# E1.2 — *Breaking Bad* S01E01 (pilote, 2008) en ontologie v0

Annotation **analytique** de l'intrigue (grain grossier, ~15 deltas) — l'objet est de
tester l'ontologie sur un long-format moderne, pas de reproduire l'œuvre. On annote la
**fabula** (ordre causal), pas le montage : le pilote ouvre sur un flashforward
(camping-car, pantalon, caméscope) → excellent test de la séparation I1 : ce
flashforward est une opération de **discours** (prolepse, Genette) sur des deltas situés
tard dans la fabula (d13-d15), génératrice de curiosité (Sternberg) — il n'existe pas
comme objet de fabula.

## Agents (extraits)

```yaml
agents:
  WALT:
    beliefs: [ "je vaux plus que ma vie actuelle", "ma famille sera démunie sans moi" ]
    desires:
      want: "laisser sa famille à l'abri du besoin (argent)"
      need: "reconnaître son propre orgueil / se sentir puissant, vivant"
        # NB: le need réel de Walt (orgueil, pouvoir) est *antagoniste* du want affiché —
        # l'ontologie v0 le permet (want/need indépendants) : c'est ce qui fait la tragédie.
    values: [ {axe: famille, poids: 3}, {axe: fierte-humiliation, poids: 3},
              {axe: legalite, poids: 1} ]
    flaw: "orgueil blessé = croyance protégée : « le monde m'a volé ce qui me revenait »"
  SKYLER:  { beliefs: [ "Walt est un mari prévisible et honnête" ] }
  JESSE:   { desires: {want: "argent facile, survie"}, values: [{axe: loyaute, poids: 2}] }
  HANK:    { kind: agent, props: {métier: agent DEA} }   # source d'ironie structurelle
  FAMILLE: { kind: entité-collective, membres: [SKYLER, WALTJR, bébé-à-naître] }  # ⇒ amendement A3
  AUD:     { genreContract: [ "drame criminel ⇒ la transgression aura des conséquences" ] }

valueAxes: [ vie-mort, famille, fierte-humiliation, legalite, verite-mensonge, subsistance ]
norms: [ n1: "fabriquer/vendre de la drogue est illégal et socialement condamné" ]
  # ⇒ la v0 n'a pas d'objet Norm de première classe → amendement A1
```

## Fabula en deltas (grain grossier)

```yaml
deltas:
  d1:  {change: "état initial : WALT, 50 ans, surqualifié, deux emplois humiliants",
        causes: [], charges: [{WALT, fierte-humiliation, -, 2}], scope: {obs: [tous]}, irr: false}
  d2:  {change: "humiliation au lave-auto devant ses élèves",
        causes: [{soc, d1}], charges: [{WALT, fierte-humiliation, -, 2}],
        scope: {obs: [WALT, AUD]}, irr: false}
  d3:  {change: "DIAGNOSTIC : cancer inopérable, pronostic ~2 ans",
        causes: [{phy, exogène}],
        charges: [{WALT, vie-mort, -, 3, anticipée}, {FAMILLE, subsistance, -, 3, anticipée}],
        scope: {obs: [WALT, AUD], hidden: [SKYLER, FAMILLE, HANK]}, irr: true}
        # DISRUPTION (I8) canonique + naissance du SECRET s1 (Walt tait le diagnostic)
        # charges *anticipées* : rien n'a encore changé matériellement ⇒ amendement A2
  d4:  {change: "WALT tait le diagnostic à sa famille",
        causes: [{psy, d3}, {psy, flaw: orgueil}],
        charges: [{WALT, verite-mensonge, -, 1}], scope: {obs: [WALT, AUD]}, irr: false}
  d5:  {change: "ride-along avec HANK : WALT découvre l'argent de la méthamphétamine",
        causes: [{soc, exogène}, {psy, d3}],   # sans d3, cette info resterait inerte
        charges: [{WALT, subsistance, +, 2, anticipée}], scope: {obs: [WALT, HANK, AUD]}, irr: false}
  d6:  {change: "WALT aperçoit JESSE en fuite lors du raid",
        causes: [{phy, d5}], charges: [], scope: {obs: [WALT, AUD], hidden: [HANK]}, irr: false}
        # information asymétrique pure : un secret partagé naît d'une perception non partagée
  d7:  {change: "WALT adopte l'intention : produire de la meth avec JESSE",
        causes: [{psy, d3}, {psy, d5}, {psy, d6}, {psy, d2}],
        charges: [{WALT, legalite, -, 3}, {WALT, fierte-humiliation, +, 2, anticipée}],
        scope: {obs: [WALT, AUD], hidden: [FAMILLE, HANK]}, irr: false}
        # le nœud causal le plus dense de l'épisode — cible principale de l'ablation E2
  d8:  {change: "WALT recrute/contraint JESSE (« ou je te dénonce »)",
        causes: [{psy, d7}, {soc, d6}],
        charges: [{JESSE, liberte, -, 1}], scope: {obs: [WALT, JESSE, AUD]}, irr: false}
        # ⇒ COMMITMENT c2 : partenariat sous menace (contrat, force: coercition)
  d9:  {change: "WALT vole du matériel de labo au lycée",
        causes: [{psy, d7}], charges: [{WALT, legalite, -, 1}],
        scope: {obs: [WALT, AUD]}, irr: false}
  d10: {change: "PREMIÈRE CUISSON dans le désert — produit d'une pureté exceptionnelle",
        causes: [{psy, d7}, {phy, d9}],
        charges: [{WALT, fierte-humiliation, +, 3}, {WALT, legalite, -, 2}],
        scope: {obs: [WALT, JESSE, AUD]}, irr: true}
        # SEUIL (Threshold) : franchissement du monde ordinaire au monde criminel —
        # état antérieur (« Walt n'a jamais transgressé ») définitivement inaccessible
  d11: {change: "Krazy-8 et Emilio menacent de mort WALT et JESSE",
        causes: [{soc, d10}, {soc, réseau de JESSE}],
        charges: [{WALT, vie-mort, -, 3}, {JESSE, vie-mort, -, 3}],
        scope: {obs: [WALT, JESSE, AUD]}, irr: false}
        # CONFLIT dérivé : plans incompatibles (vendre vs voler/tuer) — détectable ✅
  d12: {change: "WALT improvise le gaz phosphine : neutralise les deux dealers (tentative de survie, succès)",
        causes: [{psy, d11}, {psy, savoir de chimiste: d1}],
        charges: [{WALT, vie-mort, +, 2}, {WALT, legalite, -, 3}, {WALT, fierte-humiliation, +, 1}],
        scope: {obs: [WALT, JESSE, AUD]}, irr: true}
        # 2e seuil : violence quasi létale — l'ontologie enchaîne deux seuils sans « actes »
  d13: {change: "fuite paniquée en camping-car, enregistrement caméscope (aveux/adieux)",
        causes: [{phy, d12}], charges: [{WALT, verite-mensonge, +, 1}],
        scope: {obs: [WALT, JESSE, AUD]}, irr: false}
        # ← c'est ICI que pointe la prolepse d'ouverture (discours), résolue pour AUD
  d14: {change: "retour au foyer : WALT ment par omission sur sa journée",
        causes: [{psy, d13}, {psy, d4}], charges: [{WALT, verite-mensonge, -, 2}],
        scope: {obs: [WALT, AUD], hidden: [SKYLER]}, irr: false}
  d15: {change: "WALT, transformé, initiative sexuelle inhabituelle — SKYLER : « Walt, c'est bien toi ? »",
        causes: [{psy, d10}, {psy, d12}],
        charges: [{WALT, fierte-humiliation, +, 2}], scope: {obs: [WALT, SKYLER, AUD]}, irr: false}
        # la transformation interne devient perceptible par un agent non informé :
        # SKYLER *infère* un changement sans en connaître la cause (inferableBy ✅)
```

## Objets dérivés et mesures

- **Secrets** : s1 (diagnostic, d3→) ; s2 (double vie criminelle, d7→) — deux secrets
  emboîtés à créanciers différents ; coût de maintien croissant = pression dramatique
  mesurable (nombre d'agents à qui mentir × interactions).
- **Ironies structurelles** : HANK (DEA) ignorera s2 — `knows(AUD) ∧ ¬knows(HANK)`
  installée dès d5 : l'ontologie capte l'ironie *à long terme* comme simple invariant
  épistémique persistant ✅.
- **Commitments** : c1 (implicite, WALT→FAMILLE : « vous mettre à l'abri » — le *want*
  promu en serment intérieur) ; c2 (WALT↔JESSE, coercitif) ; c3 (contrat de genre :
  la transgression se paiera — ouvert en fin d'épisode : dette narrative élevée,
  conforme à la fonction d'un pilote : **le pilote maximise la dette, la fable la
  soldait** — les deux régimes sont mesurables sur le même axe ✅).
- **Arc(WALT)** : d3 → d7 → d10 (seuil) → d12 (seuil) → d15 : humiliation → puissance ;
  le want (famille) sert de **justification** au need réel (orgueil) — l'écart
  want/need est représentable et c'est lui que la série exploitera 5 saisons.
- **Dilemme** : d7 = dilemme réel (famille+fierté vs légalité+vérité) : incompatibilité
  interne entre valeurs pondérées d'un même agent → détectable par la règle v0 ✅.

## Constats E1.2

1. Couverture correcte au grain choisi, sans scène/acte ; la prolepse d'ouverture
   confirme la nécessité de la couche discours séparée (I1).
2. **Manques identifiés** → amendements : A1 (Norm de première classe : « illégal »
   n'est pas une valeur personnelle mais une norme sociale opposable — CiF le
   confirmait) ; A2 (charges anticipées : d3, d5, d7 en dépendent — lien direct avec
   espoir/peur du modèle OCC) ; A3 (entité collective FAMILLE : créancier d'engagements
   et porteur de charges sans être un agent délibérant).
3. La densité causale de d7 (4 causes) valide le choix d'arêtes multiples ; c'est le
   marqueur formel d'un « tournant » sans aucune notion de plot point paginé.

Compte d'objets (E5) : 6 axes + 1 norme, 6 agents (+AUD), 15 deltas, 2 secrets,
3 engagements, 2 conflits, 1 dilemme, 1 arc, 2 seuils, 1 prolepse (discours).
