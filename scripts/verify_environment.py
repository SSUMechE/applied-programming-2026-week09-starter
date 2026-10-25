"""Verify the existing Week 6 core environment and this editable checkout."""

import importlib
from importlib.metadata import version
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = {"pip": "26.2.1", "numpy": "2.4.6", "pytest": "9.1.1", "setuptools": "80.9.0"}
failures = []
if sys.version_info[:3] != (3, 12, 13):
    failures.append(f"Python expected 3.12.13, found {sys.version.split()[0]}")
for name, expected in required.items():
    try:
        actual = version(name)
        if actual != expected:
            failures.append(f"{name} expected {expected}, found {actual}")
    except Exception as error:
        failures.append(f"{name}: {error}")
for name in ("pytest", "ap_week09"):
    try:
        module = importlib.import_module(name)
        if name == "ap_week09":
            loaded = Path(module.__file__).resolve()
            expected = (ROOT / "src" / "ap_week09" / "__init__.py").resolve()
            if loaded != expected:
                failures.append(f"ap_week09 loaded from {loaded}, expected {expected}")
    except Exception as error:
        failures.append(f"import {name}: {error}")
if failures:
    print("ENVIRONMENT FAIL")
    print("\n".join(failures))
    print("Use Anaconda Prompt, activate applied-programming-w06 and return to this repository.")
    print("Run python -m pip install -e . --no-build-isolation, then repeat this check.")
    raise SystemExit(1)
print("ENVIRONMENT PASS")
