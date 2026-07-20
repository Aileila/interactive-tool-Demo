"""Causality Engine — requêtes causales normées (sémantique : docs/phase-2 §2-3).

Industrialisation des fonctions validées en Phase 2 (ex-nosval) :
- event_causes : origines événementielles (R1/R1b — les arêtes `them` relient
  sans causer, les dispositions/engagements co-expliquent sans déclencher).
- ancestors    : « pourquoi ? » — fermeture amont, tous types d'arêtes.
- ablate       : « que devient l'histoire sans d ? » — point fixe d'orphelinage
  (requires retirés, ou toutes causes événementielles retirées sans exogène).
- criticality  : R4 — portance (charge des deltas invalidés), pas nécessité.
"""

from __future__ import annotations


def event_causes(d):
    froms = [c["from"] for c in d.get("causes", [])
             if "from" in c and c.get("type") != "them"]
    exo = [c for c in d.get("causes", [])
           if c.get("exogenous") and c.get("type") != "them"]
    return froms, exo


def ancestors(world, delta_id):
    seen, dispositions, commitments = set(), set(), set()
    stack = [delta_id]
    while stack:
        d = world.deltas[stack.pop()]
        for c in d.get("causes", []):
            if "from" in c and c["from"] not in seen:
                seen.add(c["from"])
                stack.append(c["from"])
            if "disposition" in c:
                dispositions.add(c["disposition"])
            if "commitment" in c:
                commitments.add(c["commitment"])
    return seen, dispositions, commitments


def descendants(world, delta_id):
    out = set()
    for d in world.deltas.values():
        froms, _ = event_causes(d)
        if delta_id in froms:
            out.add(d["id"])
    closure = set(out)
    for x in list(out):
        closure |= descendants(world, x)
    return closure


def ablate(world, delta_id):
    removed = {delta_id}
    changed = True
    while changed:
        changed = False
        for d in world.deltas.values():
            if d["id"] in removed:
                continue
            froms, exo = event_causes(d)
            if any(r in removed for r in d.get("requires", [])):
                removed.add(d["id"]); changed = True; continue
            if froms and all(f in removed for f in froms) and not exo:
                removed.add(d["id"]); changed = True
    commitments = {c["id"] for c in world.commitments.values()
                   if c.get("opened_by") in removed or c.get("resolved_by") in removed}
    revelations = {r["id"] for r in world.revelations.values()
                   if r["delta"] in removed or r.get("reveals_delta") in removed}
    secrets = {s["id"] for s in world.secrets.values()
               if s.get("opened_by") in removed or s.get("revealed_by") in removed}
    return removed, commitments, revelations, secrets


def criticality(world, delta_id):
    removed, commitments, _, _ = ablate(world, delta_id)
    score = sum(ch["magnitude"] for did in removed
                for ch in world.deltas[did].get("charges", []))
    return score + 2 * len(commitments)
