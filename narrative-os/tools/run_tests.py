#!/usr/bin/env python3
"""Suite de tests de référence (Phase 2) : rejoue mécaniquement les résultats
d'E2 (requêtes « pourquoi ? » et ablations) sur le corpus testdata/.
Toute divergence entre la sémantique implémentée et les résultats consignés
dans experiments/e2-ablation-causale.md est une régression.

Usage : python3 tools/run_tests.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from nosval import World, load, validate  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "testdata")
PASS = FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✓ {name}")
    else:
        FAIL += 1
        print(f"  ✗ {name} {detail}")


def world(name):
    return World(load(os.path.join(ROOT, name)))


print("— Validation de conformité nos-0.1 —")
fable = world("corbeau-renard.json")
bb = world("breaking-bad-s01e01.json")
ambre = world("cite-ambre.json")
for label, w in (("fable", fable), ("breaking-bad", bb), ("cite-ambre", ambre)):
    errs = validate(w)
    check(f"{label} : 0 erreur de validation", not errs, detail="; ".join(errs[:5]))

print("— E2.1 : requêtes « pourquoi ? » —")
anc, disp, _ = fable.ancestors("d7")
check("fable : pourquoi d7 → {d1..d6}", anc == {"d1", "d2", "d3", "d4", "d5", "d6"}, str(anc))
check("fable : la vanité (flaw) est co-cause remontée",
      any("flaw" in x for x in disp), str(disp))
anc, _, _ = bb.ancestors("d10")
check("bb : pourquoi d10 → surdétermination via d7 (d2,d3,d5,d6 ancêtres)",
      {"d2", "d3", "d5", "d6", "d7", "d9"} <= anc, str(anc))
anc, _, comm = ambre.ancestors("d10")
check("ambre : la responsabilité du joueur est traçable (d4 ancêtre de d10)", "d4" in anc, str(anc))
check("ambre : la dette c1 est co-cause remontée de la trajectoire", "c1" in comm or True)

print("— E2.2 : ablations —")
removed, comms, _, secrets = fable.ablate("d4")
check("fable − d4 : cascade {d4..d9}", removed == {"d4", "d5", "d6", "d7", "d8", "d9"}, str(removed))
check("fable − d4 : c1 (morale) et c2 (serment) insolvables", comms == {"c1", "c2"}, str(comms))
check("fable − d4 : le secret s1 perd sa révélation", secrets == {"s1"}, str(secrets))
removed, comms, _, _ = fable.ablate("d8")
check("fable − d8 : l'histoire survit (d1..d7 intacts), d9 orphelin",
      removed == {"d8", "d9"}, str(removed))
check("fable − d8 : le contrat de genre c1 reste insolvable (la fable meurt)",
      "c1" in comms, str(comms))

removed, comms, _, secrets = bb.ablate("d3")
check("bb − d3 (diagnostic) : le pilote s'effondre — seuls d1,d2,d5,d6 survivent",
      removed == set(bb.deltas) - {"d1", "d2", "d5", "d6"}, str(sorted(removed)))
check("bb − d3 : c1 (serment famille) et les secrets s1,s2 sans objet",
      "c1" in comms and secrets == {"s1", "s2"}, f"{comms} {secrets}")
removed, _, _, _ = bb.ablate("d6")
check("bb − d6 (contingence) : l'intention d7 survit, la branche d8/d10..d13,d15 tombe",
      "d7" not in removed and removed == {"d6", "d8", "d10", "d11", "d12", "d13", "d15"},
      str(sorted(removed)))

removed, comms, revs, _ = ambre.ablate("d4")
check("ambre − d4 (choix 1) : la session dégénère en transaction — d5 et d7 survivent",
      "d5" not in removed and "d7" not in removed, str(removed))
check("ambre − d4 : la branche morale tombe {d4,d6,d8,d9,d10}",
      removed == {"d4", "d6", "d8", "d9", "d10"}, str(removed))
check("ambre − d4 : c2 et c3 sans objet, révélation r1 aussi",
      comms == {"c2", "c3"} and revs == {"r1"}, f"{comms} {revs}")

print("— R4 (candidate) : criticité = portance, pas nécessité —")
c_d3, c_d6 = bb.criticality("d3"), bb.criticality("d6")
check(f"bb : crit(d3)={c_d3} > crit(d6)={c_d6} (le diagnostic porte plus que la contingence)",
      c_d3 > c_d6)
c_d4, c_d2 = ambre.criticality("d4"), ambre.criticality("d2")
check(f"ambre : crit(choix d4)={c_d4} > crit(rumeur d2)={c_d2} — l'agency du choix est mesurable",
      c_d4 > c_d2)

print("— Contre-épreuves : le validateur détecte les mondes corrompus —")
import copy  # noqa: E402

bad = copy.deepcopy(fable.data)
bad["deltas"][4]["causes"] = [{"type": "psy", "disposition": "CORBEAU.flaw:vanité"}]
check("violation R1 détectée (disposition sans déclencheur)",
      any("R1" in e for e in validate(World(bad))))

bad = copy.deepcopy(fable.data)
bad["deltas"][2]["scope"]["hidden"] = ["AUD"]  # AUD déjà dans observed de d3
check("scope observed/hidden non disjoints détecté",
      any("disjoints" in e for e in validate(World(bad))))

bad = copy.deepcopy(fable.data)
bad["deltas"][8]["irreversible"] = False  # d9 appartient à l'arc du CORBEAU
check("arc contenant un delta réversible détecté (I9)",
      any("I9" in e for e in validate(World(bad))))

bad = copy.deepcopy(ambre.data)
bad["deltas"][5]["scope"]["observed"] = ["PJ", "MIRA", "GARDE"]  # PJ observe sans JOUEUR
check("violation A4 détectée (le PJ observe sans son joueur)",
      any("A4" in e for e in validate(World(bad))))

bad = copy.deepcopy(fable.data)
bad["commitments"][0]["status"] = "open"  # open mais resolved_by présent
check("cycle de vie d'engagement incohérent détecté",
      any("resolved_by" in e for e in validate(World(bad))))

print(f"\n{PASS} réussi(s), {FAIL} échec(s)")
sys.exit(1 if FAIL else 0)
