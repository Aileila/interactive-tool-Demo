#!/usr/bin/env python3
"""CLI : valide un ou plusieurs mondes NOS v0.1.
Usage : python3 tools/validate.py testdata/*.json"""
import sys
from nosval import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
