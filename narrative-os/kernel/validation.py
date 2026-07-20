"""Conformité statique d'un monde nos-0.2 (miroir du schéma normatif + règles
sémantiques non exprimables en JSON Schema). Hérité de la Phase 2 (nosval),
étendu en Phase 3 : version nos-0.2, champ actor, vocabulaire de prédicats."""

from __future__ import annotations

from .causality import event_causes
from .vocabulary import build_vocabulary

CAUSE_TYPES = {"phy", "psy", "soc", "them"}
AGENT_KINDS = {"agent", "audience", "collective"}
FORCES = {"contract", "oath", "threat", "implicit", "moral", "genre"}
STATUSES = {"open", "honored", "betrayed", "cancelled"}
FAMILIES = {"epistemique", "contractuelle", "conflictuelle", "relationnelle",
            "transformationnelle", "disruption", "discours"}


def _check_assertions(d, vocab, err):
    did = d["id"]
    for key in ("assertions_add", "assertions_remove"):
        for a in d.get("change", {}).get(key, []):
            if "subject" not in a or "predicate" not in a:
                err(f"delta {did} : assertion sans subject/predicate dans {key}")
                continue
            if a["predicate"] not in vocab:
                err(f"delta {did} : prédicat inconnu '{a['predicate']}' (R-VOCAB-1 statique)")


def validate(world):
    errors = []
    err = errors.append
    w = world
    epistemic_ids = set(w.agents)
    referable = epistemic_ids | set(w.entities)
    vocab, vocab_errors = build_vocabulary(w)
    errors.extend(vocab_errors)

    all_ids = (list(w.deltas) + list(w.agents) + list(w.entities) + list(w.norms)
               + list(w.mechanics) + list(w.commitments) + list(w.secrets)
               + list(w.revelations))
    seen = set()
    for i in all_ids:
        if i in seen:
            err(f"id dupliqué : {i}")
        seen.add(i)

    if not w.data.get("schema") == "nos-0.2":
        err("champ schema absent ou différent de 'nos-0.2'")
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

    for d in sorted(w.deltas.values(), key=lambda x: x["t"]):
        did = d["id"]
        for req in ("id", "t", "change", "causes", "charges", "scope", "irreversible"):
            if req not in d:
                err(f"delta {did} : champ requis manquant '{req}'")
        if "summary" not in d.get("change", {}):
            err(f"delta {did} : change.summary manquant")
        if "actor" in d and d["actor"] not in epistemic_ids:
            err(f"delta {did} : actor inconnu {d['actor']}")
        _check_assertions(d, vocab, err)

        froms, exo = event_causes(d)
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

    for c in w.commitments.values():
        cid = c["id"]
        if c.get("force") not in FORCES:
            err(f"engagement {cid} : force invalide {c.get('force')}")
        if c.get("status") not in STATUSES:
            err(f"engagement {cid} : statut invalide {c.get('status')}")
        if c.get("force") != "genre" and "debtor" not in c:
            err(f"engagement {cid} : débiteur requis (force != genre)")
        if "debtor" in c and c["debtor"] not in epistemic_ids:
            err(f"engagement {cid} : debtor inconnu {c['debtor']}")
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
            err(f"arc : agent inconnu {arc['agent']}")
        for did in arc["deltas"]:
            if did not in w.deltas:
                err(f"arc {arc['agent']} : delta inconnu {did}")
            elif not w.deltas[did]["irreversible"]:
                err(f"arc {arc['agent']} : delta {did} non irréversible (I9)")
        for th in arc.get("thresholds", []):
            if th not in arc["deltas"]:
                err(f"arc {arc['agent']} : seuil {th} hors de l'arc")
        sr = arc.get("self_revelation")
        if sr and sr not in arc["deltas"]:
            err(f"arc {arc['agent']} : self_revelation {sr} hors de l'arc")

    for m in w.mechanics.values():
        if m.get("family") not in FAMILIES:
            err(f"mécanique {m['id']} : famille invalide {m.get('family')}")

    return errors
