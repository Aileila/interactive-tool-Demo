"""Coherence Engine — gardien du commit (architecture §2.3).

`propose(delta)` vérifie un delta candidat contre l'historique committé et
l'état courant, et rend soit le commit, soit une liste de REFUS MOTIVÉS
(règle, message, éléments en cause) — la sortie clé qui rend le système
explicable et « éduque » un Proposer (LLM ou autre).

Catalogue des règles (docs/phase-3) :
  R-CAUS-1  cause vers un delta non committé
  R-CAUS-2  précondition dure (requires) non committée
  R-CAUS-3  R1 : dispositions/engagements sans déclencheur événementiel
  R-CAUS-4  ordre des temps logiques non croissant
  R-EPIS-1  l'acteur réagit (cause psy) à un delta hors de son champ épistémique
  R-EPIS-2  scope observed/hidden non disjoints
  R-EPIS-3  A4 : le PJ observe sans son joueur
  R-VOCAB-1 prédicat inconnu (ni noyau Q8, ni extension déclarée)
  R-STATE-1 retrait d'une assertion absente de l'état
  R-STATE-2 ajout d'une assertion déjà présente
  R-STATE-3 prédicat fonctionnel : seconde valeur pour le même sujet
  R-STATE-4 objet exclusif : second sujet pour le même objet (double possession)
"""

from __future__ import annotations

from dataclasses import dataclass

from .causality import event_causes
from .store import Store, _triple
from .vocabulary import build_vocabulary


@dataclass
class Refusal:
    rule: str
    message: str

    def __str__(self):
        return f"[{self.rule}] {self.message}"


class CoherenceEngine:
    def __init__(self, world):
        self.world = world
        self.store = Store()
        self.vocab, _ = build_vocabulary(world)
        self.committed = {}          # delta_id -> delta
        self.last_t = -1

    # ------------------------------------------------------------------ epistémique

    def _actor_knows(self, actor, cause_id):
        """L'acteur a-t-il accès au delta cause_id ? Par observation/inférence,
        ou par une révélation déjà committée qui le lui a transmis."""
        cause = self.committed[cause_id]
        sc = cause.get("scope", {})
        if actor in set(sc.get("observed", [])) | set(sc.get("inferable", [])):
            return True
        for r in self.world.revelations.values():
            if (r.get("reveals_delta") == cause_id and actor in r["to"]
                    and r["delta"] in self.committed):
                return True
        return False

    # ------------------------------------------------------------------ vérification

    def check(self, delta):
        refusals = []
        ref = refusals.append
        did = delta.get("id", "?")

        if delta.get("t", 0) < self.last_t:
            ref(Refusal("R-CAUS-4",
                        f"{did} : t={delta.get('t')} antérieur au dernier commit (t={self.last_t})"))

        froms, exo = event_causes(delta)
        has_standing = any(("disposition" in c or "commitment" in c)
                           for c in delta.get("causes", []))
        for c in delta.get("causes", []):
            if "from" in c and c["from"] not in self.committed:
                ref(Refusal("R-CAUS-1", f"{did} : cause '{c['from']}' non committée"))
        if has_standing and not froms and not exo:
            ref(Refusal("R-CAUS-3",
                        f"{did} : dispositions/engagements sans déclencheur événementiel (R1)"))
        for r in delta.get("requires", []):
            if r not in self.committed:
                ref(Refusal("R-CAUS-2", f"{did} : précondition dure '{r}' non committée"))

        sc = delta.get("scope", {})
        obs, hid = set(sc.get("observed", [])), set(sc.get("hidden", []))
        if obs & hid:
            ref(Refusal("R-EPIS-2", f"{did} : observed/hidden non disjoints ({obs & hid})"))
        for b in self.world.bindings:
            if b["agent"] in obs and b["audience"] not in obs:
                ref(Refusal("R-EPIS-3",
                            f"{did} : {b['agent']} observe sans {b['audience']} (A4)"))
        actor = delta.get("actor")
        if actor:
            for c in delta.get("causes", []):
                if c.get("type") == "psy" and "from" in c and c["from"] in self.committed:
                    if not self._actor_knows(actor, c["from"]):
                        ref(Refusal("R-EPIS-1",
                                    f"{did} : {actor} réagit (psy) à '{c['from']}' "
                                    f"qui lui est caché — un agent n'agit pas sur ce qu'il ignore"))

        # état : simulation séquentielle removes puis adds
        sim = set(self.store.state)
        for a in delta.get("change", {}).get("assertions_remove", []):
            tr = _triple(a)
            if a["predicate"] not in self.vocab:
                ref(Refusal("R-VOCAB-1", f"{did} : prédicat inconnu '{a['predicate']}'"))
                continue
            if tr not in sim:
                ref(Refusal("R-STATE-1",
                            f"{did} : retrait d'une assertion absente {tr}"))
            sim.discard(tr)
        for a in delta.get("change", {}).get("assertions_add", []):
            tr = _triple(a)
            if a["predicate"] not in self.vocab:
                ref(Refusal("R-VOCAB-1", f"{did} : prédicat inconnu '{a['predicate']}'"))
                continue
            if tr in sim:
                ref(Refusal("R-STATE-2", f"{did} : assertion déjà présente {tr}"))
            flags = self.vocab[tr[1]]
            if flags.get("functional"):
                clash = {x for x in sim if x[0] == tr[0] and x[1] == tr[1] and x[2] != tr[2]}
                if clash:
                    ref(Refusal("R-STATE-3",
                                f"{did} : '{tr[1]}' fonctionnel — {tr[0]} a déjà {clash}"))
            if flags.get("exclusiveObject"):
                clash = {x for x in sim if x[1] == tr[1] and x[2] == tr[2] and x[0] != tr[0]}
                if clash:
                    ref(Refusal("R-STATE-4",
                                f"{did} : objet exclusif — {tr[2]} déjà tenu par {clash}"))
            sim.add(tr)
        return refusals

    # ------------------------------------------------------------------ commit

    def propose(self, delta):
        """Vérifie puis committe. Retourne (accepté, refus)."""
        refusals = self.check(delta)
        if refusals:
            return False, refusals
        self.store.apply(delta)
        self.committed[delta["id"]] = delta
        self.last_t = delta["t"]
        return True, []

    def replay(self):
        """Rejoue la fabula entière dans l'ordre logique. Retourne (nb commits, refus)."""
        all_refusals = []
        n = 0
        for d in self.world.ordered_deltas():
            ok, refs = self.propose(d)
            if ok:
                n += 1
            else:
                all_refusals.extend(refs)
        return n, all_refusals
