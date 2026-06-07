#!/usr/bin/env python3
"""Regenerate every study module by running each generator in ``generators/``.

Each ``generators/gen_<topic>.py`` script writes its own
``modules/<NN>_<topic>/index.html`` and ``study_guide.ipynb``. This script is a
thin orchestrator: it discovers every generator and runs it in a subprocess so
one failing generator can't abort the rest.

Usage::

    python generate_all.py              # rebuild all modules
    python generate_all.py numpy sql    # rebuild only matching generators

Requires Python 3.10+. No external dependencies — standard library only.
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
GEN_DIR = ROOT / "generators"


def main(argv: list[str]) -> int:
    gens = sorted(GEN_DIR.glob("gen_*.py"))
    if argv:
        wanted = [a.lower().removeprefix("gen_") for a in argv]
        gens = [g for g in gens if any(w in g.stem for w in wanted)]
        if not gens:
            print(f"No generators matched: {argv}")
            return 1

    failures: list[str] = []
    for g in gens:
        print(f"→ {g.name}")
        res = subprocess.run(
            [sys.executable, str(g)], capture_output=True, text=True
        )
        if res.returncode != 0:
            failures.append(g.name)
            if res.stdout:
                print(res.stdout.rstrip())
            if res.stderr:
                print(res.stderr.rstrip())
            print(f"  ✗ {g.name} failed")
        else:
            last = res.stdout.strip().splitlines()
            print(f"  ✓ {last[-1] if last else 'done'}")

    ok = len(gens) - len(failures)
    print(f"\n{ok}/{len(gens)} generators succeeded.")
    if failures:
        print("Failed:", ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
