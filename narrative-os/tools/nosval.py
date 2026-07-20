"""nosval — validateur et requêtes causales pour les mondes NOS v0.1.

Python pur, aucune dépendance. Deux rôles :
1. validate(world) : contrôles structurels (miroir du schéma normatif
   schema/nos-world.schema.json) + règles sémantiques (R1, intégrité causale,
   portées épistémiques, cycle de vie des engagements, liaison joueur A4) que
   JSON Schema ne peut pas exprimer.
2. Requêtes : ancestors (« pourquoi ? »), descendants, ablate (E2), criticality (R4).

La sémantique implémentée ici est définie dans
docs/phase-2/01-semantique-operationnelle.md — ce fichier en est l'exécutable.
"""

from __future__ import annotations

import json

CAUSE_TYPES = {"phy", "psy", "soc", "them"}
AGENT_KINDS = {"agent", "audience", "collective"}
FORCES = {"contract", "oath", "threat", "implicit", "moral", "genre"}
STATUSES = {"open", "honored", "betrayed", "cancelled"}
FAMILIES = {"epistemique", "contractuelle", "conflictuelle", "relationnelle",
            "transformationnelle", "disruption", "discours"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class World:
    def __init__(self, data):
        self.data = data
        self.deltas = {d["id"]: d for d in data.get("deltas", [])}
        self.agents = {a["id"]: a for a in data.get("agents", [])}
        self.entities = {e["id"]: e for e in data.get("entities", [])}
        self.norms = {n["id"]: n for n in data.get("norms", [])}
        self.mechanics = {m["id"]: m for m in data.get("mechanics", [])}
        self.commitments = {c["id"]: c for c in data.get("commitments", [])}
        self.secrets = {s["id"]: s for s in data.get("secrets", [])}
        self.revelations = {r["id"]: r for r in data.get("revelations", [])}
        self.axes = set(data.get("valueAxes", []))
        self.bindings = data.get("bindings", [])

    # ------------------------------------------------------------------ requêtes

    def event_causes(self, d):
        """Origines événementielles d'un delta : refs de deltas + exogènes (R1).
        Les arêtes thématiques (`them`) sont exclues : elles relient sans causer
        (règle E2 « les arêtes them seules ne suffisent pas à causer ») —
        un delta dont il ne reste que des arêtes them est orphelin."""
        froms = [c["from"] for c in d.get("causes", [])
                 if "from" in c and c.get("type") != "them"]
        exo = [c for c in d.get("causes", [])
               if c.get("exogenous") and c.get("type") != "them"]
        return froms, exo

    def ancestors(self, delta_id):
        """Fermeture causale amont (« pourquoi ? ») : deltas seulement ;
        dispositions et engagements co-causes sont retournés à part."""
        seen, dispositions, commitments = set(), set(), set()
        stack = [delta_id]
        while stack:
            d = self.deltas[stack.pop()]
            for c in d.get("causes", []):
                if "from" in c and c["from"] not in seen:
                    seen.add(c["from"])
                    stack.append(c["from"])
                if "disposition" in c:
                    dispositions.add(c["disposition"])
                if "commitment" in c:
                    commitments.add(c["commitment"])
        return seen, dispositions, commitments

    def descendants(self, delta_id):
        out = set()
        for d in self.deltas.values():
            froms, _ = self.event_causes(d)
            if delta_id in froms:
                out.add(d["id"])
        closure = set(out)
        for x in list(out):
            closure |= self.descendants(x)
        return closure

    def ablate(self, delta_id):
        """Sémantique d'ablation (E2) : un delta est invalidé si
        (a) un de ses `requires` est retiré (précondition dure), ou
        (b) il avait ≥1 cause événementielle de type delta et toutes ses causes
            événementielles retirables (refs de deltas) sont retirées SANS
            qu'aucune cause exogène ne subsiste.
        Cascade jusqu'au point fixe. Retourne (deltas retirés, engagements
        impactés, révélations impactées, secrets impactés)."""
        removed = {delta_id}
        changed = True
        while changed:
            changed = False
            for d in self.deltas.values():
                if d["id"] in removed:
                    continue
                froms, exo = self.event_causes(d)
                if any(r in removed for r in d.get("requires", [])):
                    removed.add(d["id"]); changed = True; continue
                if froms and all(f in removed for f in froms) and not exo:
                    removed.add(d["id"]); changed = True
        commitments = {c["id"] for c in self.commitments.values()
                       if c.get("opened_by") in removed or c.get("resolved_by") in removed}
        revelations = {r["id"] for r in self.revelations.values()
                       if r["delta"] in removed or r.get("reveals_delta") in removed}
        secrets = {s["id"] for s in self.secrets.values()
                   if s.get("opened_by") in removed or s.get("revealed_by") in removed}
        return removed, commitments, revelations, secrets

    def criticality(self, delta_id):
        """R4 (candidate) : charge narrative portée = somme des magnitudes des
        charges des deltas invalidés par l'ablation + 2 par engagement impacté.
        Mesure la portance (load-bearing), PAS la nécessité dramatique —
        cf. sémantique opérationnelle §7."""
        removed, commitments, _, _ = self.ablate(delta_id)
        score = sum(ch["magnitude"] for did in removed
                    for ch in self.deltas[did].get("charges", []))
        return score + 2 * len(commitments)


# ---------------------------------------------------------------------- validation

def validate(world: World):
    errors = []
    err = errors.append
    w = world
    epistemic_ids = set(w.agents)          # sujets épistémiques : agents (audience incluse)
    referable = epistemic_ids | set(w.entities)

    # unicité globale des ids
    all_ids = (list(w.deltas) + list(w.agents) + list(w.entities) + list(w.norms)
               + list(w.mechanics) + list(w.commitments) + list(w.secrets)
               + list(w.revelations))
    dupes = {i for i in all_ids if all_ids.count(i) > 1}
    # même id autorisé entre familles ? non : un espace de noms unique, plus sûr
    for fam_a, fam_b in ((w.deltas, w.commitments), (w.commitments, w.secrets)):
        pass  # couvert par le comptage global ci-dessous
    seen = set()
    for i in all_ids:
        if i in seen:
            err(f"id dupliqué : {i}")
        seen.add(i)

    if not w.data.get("schema") == "nos-0.1":
        err("champ schema absent ou différent de 'nos-0.1'")
    for a in w.agents.values():
        if a.get("kind") not in AGENT_KINDS:
            err(f"agent {a['id']} : kind invalide {a.get('kind')}")
        for v in a.get("values", []):
            if v["axis"] not in w.axes:
                err(f"agent {a['id']} : axe inconnu {v['axis']}")

    if not any(a.get("kind") == "audience" for a in w.agents.values()):
        err("aucun agent de kind 'audience' (I6 : l'audience est un agent épistémique requis)")

    for b in w.bindings:
        if b["agent"] not in w.agents or w.agents[b["agent"]]["kind"] != "agent":
            err(f"binding : agent invalide {b['agent']}")
        if b["audience"] not in w.agents or w.agents[b["audience"]]["kind"] != "audience":
            err(f"binding : audience invalide {b['audience']}")

    for n in w.norms.values():
        if "emitter" in n and n["emitter"] not in referable:
            err(f"norme {n['id']} : émetteur inconnu {n['emitter']}")

    prev_ids = set()
    for d in sorted(w.deltas.values(), key=lambda x: x["t"]):
        did = d["id"]
        for req in ("id", "t", "change", "causes", "charges", "scope", "irreversible"):
            if req not in d:
                err(f"delta {did} : champ requis manquant '{req}'")
        if "summary" not in d.get("change", {}):
            err(f"delta {did} : change.summary manquant")

        froms, exo = w.event_causes(d)
        has_standing = any(("disposition" in c or "commitment" in c) for c in d.get("causes", []))
        for c in d.get("causes", []):
            if c.get("type") not in CAUSE_TYPES:
                err(f"delta {did} : type de cause invalide {c.get('type')}")
            origins = [k for k in ("from", "disposition", "commitment", "exogenous") if k in c]
            if len(origins) != 1:
                err(f"delta {did} : cause à origine non unique {c}")
            if "from" in c:
                if c["from"] not in w.deltas:
                    err(f"delta {did} : cause vers delta inconnu {c['from']}")
                elif w.deltas[c["from"]]["t"] >= d["t"]:
                    err(f"delta {did} : cause {c['from']} non antérieure (t)")
            if "commitment" in c and c["commitment"] not in w.commitments:
                err(f"delta {did} : cause vers engagement inconnu {c['commitment']}")
        # R1 : une disposition/un engagement n'est jamais cause suffisante
        if has_standing and not froms and not exo:
            err(f"delta {did} : viole R1 — dispositions/engagements sans déclencheur événementiel")

        for r in d.get("requires", []):
            if r not in w.deltas:
                err(f"delta {did} : requires inconnu {r}")
            elif w.deltas[r]["t"] >= d["t"]:
                err(f"delta {did} : requires {r} non antérieur (t)")

        for ch in d.get("charges", []):
            if ch["agent"] not in epistemic_ids:
                err(f"delta {did} : charge sur agent inconnu {ch['agent']}")
            if ch["axis"] not in w.axes:
                err(f"delta {did} : charge sur axe inconnu {ch['axis']}")
            if not 1 <= ch["magnitude"] <= 3:
                err(f"delta {did} : magnitude hors bornes {ch['magnitude']}")
            if ch.get("mode", "realized") not in ("realized", "anticipated"):
                err(f"delta {did} : mode de charge invalide {ch.get('mode')}")
            if ch["polarity"] not in ("+", "-"):
                err(f"delta {did} : polarité invalide {ch['polarity']}")

        sc = d.get("scope", {})
        obs, hid = set(sc.get("observed", [])), set(sc.get("hidden", []))
        for aid in obs | hid | set(sc.get("inferable", [])):
            if aid not in epistemic_ids:
                err(f"delta {did} : scope référence un id non-agent {aid}")
        if obs & hid:
            err(f"delta {did} : scope observed/hidden non disjoints {obs & hid}")
        # A4 : ce que le PJ observe, son joueur (audience liée) l'observe aussi
        for b in w.bindings:
            if b["agent"] in obs and b["audience"] not in obs:
                err(f"delta {did} : viole A4 — {b['agent']} observe sans {b['audience']}")

        if "via" in d and d["via"] not in w.mechanics:
            err(f"delta {did} : mécanique inconnue {d['via']}")
        for nid in d.get("violates_norms", []):
            if nid not in w.norms:
                err(f"delta {did} : norme inconnue {nid}")
        if "choice" in d:
            by = d["choice"]["by"]
            if by not in {b["player"] for b in w.bindings}:
                err(f"delta {did} : choice.by {by} n'est pas un joueur lié (A4)")
            if d["choice"]["chosen"] not in d["choice"]["options"]:
                err(f"delta {did} : choix retenu hors options")
        prev_ids.add(did)

    for c in w.commitments.values():
        cid = c["id"]
        if c.get("force") not in FORCES:
            err(f"engagement {cid} : force invalide {c.get('force')}")
        if c.get("status") not in STATUSES:
            err(f"engagement {cid} : statut invalide {c.get('status')}")
        if c.get("force") != "genre" and "debtor" not in c:
            err(f"engagement {cid} : débiteur requis (force != genre)")
        for role in ("debtor",):
            if role in c and c[role] not in epistemic_ids:
                err(f"engagement {cid} : {role} inconnu {c[role]}")
        creditors = c["creditor"] if isinstance(c["creditor"], list) else [c["creditor"]]
        for cr in creditors:
            if cr not in epistemic_ids:
                err(f"engagement {cid} : créancier inconnu {cr}")
        for ref in ("opened_by", "resolved_by"):
            if ref in c and c[ref] not in w.deltas:
                err(f"engagement {cid} : {ref} vers delta inconnu {c[ref]}")
        if c["status"] == "open" and "resolved_by" in c:
            err(f"engagement {cid} : open mais resolved_by présent")
        if c["status"] in ("honored", "betrayed", "cancelled") and "resolved_by" not in c:
            err(f"engagement {cid} : statut {c['status']} sans resolved_by")
        if "opened_by" in c and "resolved_by" in c:
            if w.deltas[c["resolved_by"]]["t"] < w.deltas[c["opened_by"]]["t"]:
                err(f"engagement {cid} : résolu avant ouverture")

    for s in w.secrets.values():
        sid = s["id"]
        if s["holder"] not in epistemic_ids:
            err(f"secret {sid} : détenteur inconnu {s['holder']}")
        for aid in s["hidden_from"]:
            if aid not in epistemic_ids:
                err(f"secret {sid} : hidden_from inconnu {aid}")
        for ref in ("opened_by", "revealed_by"):
            if ref in s and s[ref] not in w.deltas:
                err(f"secret {sid} : {ref} vers delta inconnu {s[ref]}")
        if "opened_by" in s and "revealed_by" in s:
            if w.deltas[s["revealed_by"]]["t"] <= w.deltas[s["opened_by"]]["t"]:
                err(f"secret {sid} : révélé avant (ou avec) son ouverture")

    for r in w.revelations.values():
        rid = r["id"]
        if r["delta"] not in w.deltas:
            err(f"révélation {rid} : delta inconnu {r['delta']}")
        if "reveals_secret" in r and r["reveals_secret"] not in w.secrets:
            err(f"révélation {rid} : secret inconnu {r['reveals_secret']}")
        if "reveals_delta" in r:
            if r["reveals_delta"] not in w.deltas:
                err(f"révélation {rid} : reveals_delta inconnu {r['reveals_delta']}")
            elif w.deltas[r["reveals_delta"]]["t"] >= w.deltas[r["delta"]]["t"]:
                err(f"révélation {rid} : révèle un delta non antérieur")
        for aid in r["to"]:
            if aid not in epistemic_ids:
                err(f"révélation {rid} : destinataire inconnu {aid}")

    for arc in w.data.get("arcs", []):
        if arc["agent"] not in w.agents:
            errors.append(f"arc : agent inconnu {arc['agent']}")
        for did in arc["deltas"]:
            if did not in w.deltas:
                errors.append(f"arc {arc['agent']} : delta inconnu {did}")
            elif not w.deltas[did]["irreversible"]:
                errors.append(f"arc {arc['agent']} : delta {did} non irréversible (I9)")
        for th in arc.get("thresholds", []):
            if th not in arc["deltas"]:
                errors.append(f"arc {arc['agent']} : seuil {th} hors de l'arc")
        sr = arc.get("self_revelation")
        if sr and sr not in arc["deltas"]:
            errors.append(f"arc {arc['agent']} : self_revelation {sr} hors de l'arc")

    for m in w.mechanics.values():
        if m.get("family") not in FAMILIES:
            errors.append(f"mécanique {m['id']} : famille invalide {m.get('family')}")

    return errors


def main(argv):
    import glob
    paths = []
    for a in argv:
        paths.extend(glob.glob(a))
    if not paths:
        print("usage: validate.py <monde.json>…")
        return 2
    failed = False
    for p in sorted(paths):
        world = World(load(p))
        errs = validate(world)
        n = len(world.deltas)
        if errs:
            failed = True
            print(f"✗ {p} ({n} deltas) — {len(errs)} erreur(s) :")
            for e in errs:
                print(f"   - {e}")
        else:
            print(f"✓ {p} ({n} deltas, {len(world.commitments)} engagements) : conforme nos-0.1")
    return 1 if failed else 0
