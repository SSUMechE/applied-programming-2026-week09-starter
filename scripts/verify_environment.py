"""Check the existing course CUDA environment without running student TODOs.

This checks imports, the current checkout and a tiny CUDA tensor calculation.
It does not run Genesis physics, test algorithms or install/replace packages.
"""

import importlib
from importlib.metadata import version
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENT = "applied-programming-cuda"


def fail(messages):
    print("ENVIRONMENT FAIL")
    print("\n".join(messages))
    print("Use Anaconda Prompt, activate applied-programming-cuda and return to this repository.")
    print("Follow README section 2 to add missing Week 9 build/test support and register this checkout.")
    print('python -m pip install "setuptools>=80.9.0" pytest==9.1.1')
    print("python -m pip install -e . --no-deps --no-build-isolation")
    print("Do not replace PyTorch, Genesis, NumPy or the driver to fix this check.")
    print("If the existing CUDA setup differs or fails, stop and ask the instructor with this output.")
    return 1


def main():
    failures = []
    print(f"Python executable: {sys.executable}")
    if Path(sys.prefix).name.casefold() != ENVIRONMENT:
        failures.append(f"Expected the {ENVIRONMENT} interpreter, found {sys.prefix}")
    if sys.version_info[:2] != (3, 12):
        failures.append(f"Python expected 3.12.x, found {sys.version.split()[0]}")
    required = {"pytest": "9.1.1", "numpy": "2.4.6", "genesis-world": "1.3.2"}
    for name, expected in required.items():
        try:
            actual = version(name)
            if actual != expected:
                failures.append(f"{name} expected {expected}, found {actual}")
        except Exception as error:
            failures.append(f"{name}: {error}")
    try:
        from packaging.version import Version
        actual = version("setuptools")
        if Version(actual) < Version("80.9.0"):
            failures.append(f"setuptools requires at least 80.9.0, found {actual}")
    except Exception as error:
        failures.append(f"setuptools build support: {error}")
    for name in ("pytest", "numpy", "ap_week09"):
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
        return fail(failures)

    # Retain the Week 5 version gate before any CUDA operation or Genesis import.
    try:
        torch = importlib.import_module("torch")
        if torch.__version__ != "2.14.0+cu126" or torch.version.cuda != "12.6":
            return fail([
                "Week 5 requires PyTorch 2.14.0+cu126 and CUDA build 12.6.",
                f"Found PyTorch {torch.__version__} and CUDA build {torch.version.cuda}.",
                "The CUDA version displayed by nvidia-smi is not the PyTorch build version.",
            ])
        if not torch.cuda.is_available():
            return fail(["CUDA is unavailable. A CPU run does not satisfy this check."])
        importlib.import_module("genesis")
        path = torch.tensor([[0.0, 0.0], [3.0, 0.0], [3.0, 4.0]],
                            dtype=torch.float32, device="cuda:0")
        if path.device.type != "cuda":
            return fail(["The calculation tensor is not on CUDA."])
        length = torch.linalg.vector_norm(path[1:] - path[:-1], dim=1).sum().item()
        if not math.isfinite(length) or abs(length - 7.0) > 1e-6:
            return fail([f"CUDA calculation expected 7.0, found {length}."])
        print(f"PyTorch: {torch.__version__}, CUDA build: {torch.version.cuda}")
        print(f"CUDA calculation: {length}, tensor device: {path.device}")
    except Exception as error:
        return fail([f"CUDA/Genesis import or CUDA calculation failed: {error}"])
    print("ENVIRONMENT PASS")
    print("Imports, this checkout and a CUDA tensor calculation passed.")
    print("Algorithm correctness and Genesis physical execution are checked separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
