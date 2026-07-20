"""Shim de compatibilité Phase 2 → Phase 3.

nosval a été industrialisé dans le paquet kernel/ (Phase 3) :
- World, load        → kernel.model
- validate           → kernel.validation
- requêtes causales  → kernel.causality (méthodes déléguées sur World)
Ce module réexporte l'API pour que la suite de conformité Phase 2
(run_tests.py) et les références documentaires restent valides.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from kernel import World, load, validate  # noqa: E402,F401
