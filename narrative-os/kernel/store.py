"""World State Store — event sourcing sur les deltas (architecture §2.1).

L'état est un ensemble de triplets (sujet, prédicat, objet) ; l'historique des
deltas committés EST la fabula. Le store applique sans vérifier : c'est le
Coherence Engine qui garde le commit (séparation des responsabilités). En
contrepartie, tout état passé est reconstructible (time-travel), exigence posée
dès la Phase 1 (le twist relit le passé ; débogage narratif façon rollback Ren'Py).
"""

from __future__ import annotations


def _triple(a):
    return (a["subject"], a["predicate"], a.get("object"))


class Store:
    def __init__(self):
        self.state = set()          # triplets courants
        self.history = []           # [(t, delta_id, removes, adds)] dans l'ordre de commit

    def apply(self, delta):
        removes = [_triple(a) for a in delta.get("change", {}).get("assertions_remove", [])]
        adds = [_triple(a) for a in delta.get("change", {}).get("assertions_add", [])]
        for tr in removes:
            self.state.discard(tr)
        for tr in adds:
            self.state.add(tr)
        self.history.append((delta["t"], delta["id"], removes, adds))

    def rollback(self):
        """Défait le dernier delta committé (time-travel arrière)."""
        if not self.history:
            return None
        t, did, removes, adds = self.history.pop()
        for tr in adds:
            self.state.discard(tr)
        for tr in removes:
            self.state.add(tr)
        return did

    def state_at(self, t):
        """État reconstruit juste après le dernier delta de temps logique <= t."""
        s = set()
        for ht, _, removes, adds in self.history:
            if ht > t:
                break
            for tr in removes:
                s.discard(tr)
            for tr in adds:
                s.add(tr)
        return s

    def facts(self, subject=None, predicate=None, obj=None, at=None):
        source = self.state if at is None else self.state_at(at)
        return {tr for tr in source
                if (subject is None or tr[0] == subject)
                and (predicate is None or tr[1] == predicate)
                and (obj is None or tr[2] == obj)}

    def holds(self, subject, predicate, obj=None, at=None):
        return bool(self.facts(subject, predicate, obj, at))
