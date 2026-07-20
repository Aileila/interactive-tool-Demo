#!/usr/bin/env python3
"""Suite de tests du noyau symbolique (Phase 3).

Vérifie : (a) le rejeu intégral des 3 mondes de référence par le Coherence
Engine (34 commits, 0 refus) ; (b) l'état final et le time-travel du Store ;
(c) le rollback ; (d) le catalogue de refus motivés — chaque règle R-* doit
refuser le bon delta corrompu avec la bonne raison ; (e) la connaissance par
révélation (un acteur peut réagir à un delta caché qu'on lui a révélé).

Usage : python3 tools/run_kernel_tests.py
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from kernel import CoherenceEngine, World, load  # noqa: E402

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


def engine_through(w, last_delta_id):
    """Moteur ayant committé la fabula jusqu'à last_delta_id inclus."""
    e = CoherenceEngine(w)
    for d in w.ordered_deltas():
        ok, refs = e.propose(d)
        assert ok, f"préparation : {d['id']} refusé : {refs}"
        if d["id"] == last_delta_id:
            break
    return e


def rules_of(refusals):
    return {r.rule for r in refusals}


print("— Rejeu intégral par le Coherence Engine —")
engines = {}
for label, fname, n in (("fable", "corbeau-renard.json", 9),
                        ("breaking-bad", "breaking-bad-s01e01.json", 15),
                        ("cite-ambre", "cite-ambre.json", 10)):
    w = world(fname)
    e = CoherenceEngine(w)
    commits, refusals = e.replay()
    check(f"{label} : {n} commits, 0 refus", commits == n and not refusals,
          f"({commits} commits ; {[str(r) for r in refusals[:3]]})")
    engines[label] = e

print("— World State Store : état final et time-travel —")
st = engines["fable"].store
check("fable : à la fin, RENARD possède le fromage",
      ("RENARD", "possède", "fromage") in st.state
      and ("CORBEAU", "possède", "fromage") not in st.state)
check("fable : time-travel — à t=6 le CORBEAU possède encore le fromage",
      st.holds("CORBEAU", "possède", "fromage", at=6))
check("fable : la misbelief existe à t=6, éteinte à la fin (révélation d8)",
      st.holds("CORBEAU", "croit", "le compliment est sincère", at=6)
      and not st.holds("CORBEAU", "croit", "le compliment est sincère"))
st = engines["breaking-bad"].store
check("bb : la menace de mort existe à t=11 et est levée par d12",
      st.holds("WALT", "est", "menacé de mort", at=11)
      and not st.holds("WALT", "est", "menacé de mort"))
check("bb : à la fin, Walt est cuisinier de méthamphétamine et cache sa journée",
      st.holds("WALT", "est", "cuisinier de méthamphétamine")
      and st.holds("WALT", "cache", "sa journée criminelle"))
st = engines["cite-ambre"].store
check("ambre : fin — PJ détenu, MIRA libre (plus détenue), SILAS payé",
      st.holds("PJ", "est", "détenu") and st.holds("MIRA", "est", "libre")
      and not st.holds("MIRA", "est", "détenue")
      and st.holds("SILAS", "possède", "300 ambres"))
check("ambre : l'irréversibilité est narrative, pas factuelle — la détention de "
      "MIRA (état) prend fin, son arrestation (delta d6) reste dans l'historique",
      any(h[1] == "d6" for h in st.history))

print("— Rollback (time-travel arrière) —")
e = engine_through(world("corbeau-renard.json"), "d9")
last = e.store.rollback()
check("fable : rollback défait d9 — le serment disparaît de l'état",
      last == "d9" and not e.store.holds("CORBEAU", "croit",
                                         "il ne faut plus écouter les flatteurs"))

print("— Catalogue de refus motivés —")
w = world("corbeau-renard.json")

e = engine_through(w, "d3")
bad = {"id": "x1", "t": 4, "actor": "CORBEAU",
       "change": {"summary": "le corbeau riposte au plan du renard"},
       "causes": [{"type": "psy", "from": "d3"}], "charges": [],
       "scope": {"observed": ["CORBEAU"]}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-EPIS-1 : le CORBEAU ne peut pas réagir à l'intention secrète du RENARD",
      not ok and "R-EPIS-1" in rules_of(refs), str(rules_of(refs)))

e = engine_through(w, "d1")
bad = {"id": "x2", "t": 2, "change": {"summary": "le renard a déjà le fromage",
       "assertions_add": [{"subject": "RENARD", "predicate": "possède", "object": "fromage"}]},
       "causes": [{"type": "phy", "from": "d1"}], "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-STATE-4 : double possession du fromage refusée",
      not ok and "R-STATE-4" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x3", "t": 2, "change": {"summary": "le corbeau est aussi au sol",
       "assertions_add": [{"subject": "CORBEAU", "predicate": "situé-à", "object": "sol"}]},
       "causes": [{"type": "phy", "from": "d1"}], "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-STATE-3 : seconde localisation (prédicat fonctionnel) refusée",
      not ok and "R-STATE-3" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x4", "t": 2, "change": {"summary": "retrait d'un fait inexistant",
       "assertions_remove": [{"subject": "RENARD", "predicate": "possède", "object": "fromage"}]},
       "causes": [{"type": "phy", "from": "d1"}], "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-STATE-1 : retrait d'une assertion absente refusé",
      not ok and "R-STATE-1" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x5", "t": 2, "change": {"summary": "télépathie soudaine",
       "assertions_add": [{"subject": "CORBEAU", "predicate": "télépathie", "object": "RENARD"}]},
       "causes": [{"type": "phy", "from": "d1"}], "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-VOCAB-1 : prédicat hors vocabulaire refusé",
      not ok and "R-VOCAB-1" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x6", "t": 2, "change": {"summary": "cause fantôme"},
       "causes": [{"type": "phy", "from": "d99"}], "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-CAUS-1 : cause vers un delta non committé refusée",
      not ok and "R-CAUS-1" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x7", "t": 2, "change": {"summary": "la vanité agit toute seule"},
       "causes": [{"type": "psy", "disposition": "CORBEAU.flaw:vanité"}],
       "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-CAUS-3 : disposition sans déclencheur refusée (R1)",
      not ok and "R-CAUS-3" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x8", "t": 0, "change": {"summary": "retour en arrière du temps logique"},
       "causes": [], "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-CAUS-4 : temps logique non croissant refusé",
      not ok and "R-CAUS-4" in rules_of(refs), str(rules_of(refs)))

bad = {"id": "x9", "t": 2, "change": {"summary": "précondition dure absente"},
       "causes": [{"type": "phy", "from": "d1"}], "requires": ["d7"],
       "charges": [], "scope": {}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-CAUS-2 : requires non committé refusé",
      not ok and "R-CAUS-2" in rules_of(refs), str(rules_of(refs)))

wa = world("cite-ambre.json")
e = engine_through(wa, "d3")
bad = {"id": "x10", "t": 4, "change": {"summary": "le PJ observe sans son joueur"},
       "causes": [{"type": "phy", "from": "d3"}], "charges": [],
       "scope": {"observed": ["PJ", "MIRA"]}, "irreversible": False}
ok, refs = e.propose(bad)
check("R-EPIS-3 : le PJ observe sans le JOUEUR (A4) refusé",
      not ok and "R-EPIS-3" in rules_of(refs), str(rules_of(refs)))

print("— Connaissance par révélation (le refus s'éteint quand l'information circule) —")
e = CoherenceEngine(wa)
e.replay()
probe = {"id": "x11", "t": 11, "actor": "PJ",
         "change": {"summary": "PJ repense à la capture de MIRA (d6, caché mais révélé par r1/d8)"},
         "causes": [{"type": "psy", "from": "d6"}], "charges": [],
         "scope": {"observed": ["PJ", "JOUEUR"]}, "irreversible": False}
ok, refs = e.propose(probe)
check("ambre : PJ peut réagir à d6 (caché) car la révélation r1 (d8) est committée",
      ok, str([str(r) for r in refs]))
e2 = engine_through(copy.deepcopy(wa) and world("cite-ambre.json"), "d7")  # avant d8/r1
probe2 = dict(probe, t=8, id="x12")
ok, refs = e2.propose(probe2)
check("ambre : la même réaction AVANT la révélation est refusée (R-EPIS-1)",
      not ok and "R-EPIS-1" in rules_of(refs), str(rules_of(refs)))

print(f"\n{PASS} réussi(s), {FAIL} échec(s)")
sys.exit(1 if FAIL else 0)
