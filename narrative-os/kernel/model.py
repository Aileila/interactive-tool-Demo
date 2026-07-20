"""World : la fabula chargée et indexée. Les requêtes causales délèguent à causality."""

from __future__ import annotations

import json


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

    def ordered_deltas(self):
        return sorted(self.deltas.values(), key=lambda d: d["t"])

    # Délégations vers le Causality Engine (compatibilité suite Phase 2)
    def event_causes(self, d):
        from . import causality
        return causality.event_causes(d)

    def ancestors(self, delta_id):
        from . import causality
        return causality.ancestors(self, delta_id)

    def descendants(self, delta_id):
        from . import causality
        return causality.descendants(self, delta_id)

    def ablate(self, delta_id):
        from . import causality
        return causality.ablate(self, delta_id)

    def criticality(self, delta_id):
        from . import causality
        return causality.criticality(self, delta_id)
