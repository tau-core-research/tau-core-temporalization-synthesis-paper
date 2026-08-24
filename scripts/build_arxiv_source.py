#!/usr/bin/env python3
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "temporalization_synthesis_submission_source"

with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(SOURCE.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "main.pdf" or path.suffix in {".aux", ".bbl", ".blg", ".log", ".out", ".toc"}:
            continue
        archive.write(path, path.relative_to(SOURCE))

print("TEMPORALIZATION_SYNTHESIS_ARXIV_SOURCE_BUILT")
