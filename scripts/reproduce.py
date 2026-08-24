#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    print("$", " ".join(map(str, args)))
    subprocess.run(args, cwd=ROOT, check=True)


run(sys.executable, "scripts/build_figures.py")
run(sys.executable, "scripts/audit_temporal_synthesis.py")
run("tectonic", "temporalization_synthesis_submission_source/main.tex")
run(sys.executable, "scripts/build_arxiv_source.py")
run(sys.executable, "-m", "pytest", "-q")
print("TEMPORALIZATION_SYNTHESIS_REPRODUCTION_COMPLETE")
