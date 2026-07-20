#!/usr/bin/env python3
"""CLI : valide un ou plusieurs mondes NOS nos-0.2 (conformité statique
+ rejeu complet par le Coherence Engine).
Usage : python3 tools/validate.py testdata/*.json"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from kernel import CoherenceEngine, World, load, validate  # noqa: E402


def main(argv):
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
        n_commits, refusals = CoherenceEngine(world).replay() if not errs else (0, [])
        if errs or refusals:
            failed = True
            print(f"✗ {p} — {len(errs)} erreur(s) statique(s), {len(refusals)} refus de commit :")
            for e in errs:
                print(f"   - {e}")
            for r in refusals:
                print(f"   - {r}")
        else:
            print(f"✓ {p} : conforme nos-0.2, {n_commits} deltas committés sans refus")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
