"""Noyau symbolique du Narrative OS (Phase 3) — mode symbolique pur, zéro dépendance.

Modules :
- model       : World (chargement, index) — la fabula comme données.
- vocabulary  : vocabulaire de prédicats (noyau commun Q8 + extensions déclarées).
- validation  : conformité statique d'un monde nos-0.2 (miroir du schéma + règles).
- causality   : Causality Engine — ancestors / descendants / ablate / criticality.
- store       : World State Store — event sourcing sur les deltas, time-travel.
- coherence   : Coherence Engine — gardien de commit, refus motivés (catalogue R-*).
"""
from .model import World, load                      # noqa: F401
from .vocabulary import build_vocabulary, CORE      # noqa: F401
from .validation import validate                    # noqa: F401
from .store import Store                            # noqa: F401
from .coherence import CoherenceEngine, Refusal     # noqa: F401
