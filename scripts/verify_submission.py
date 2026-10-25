"""Check the local protected files and the three permitted edit regions.

This does not run tests again and does not check GitHub access or LMS submission.
"""

import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
contract = json.loads((ROOT / "scripts" / "protected_contract.json").read_text(encoding="utf-8"))
failures = []
for name, expected in contract["protected_files"].items():
    path = ROOT / name
    if not path.is_file():
        failures.append(f"missing supplied file: {name}")
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failures.append(f"supplied file changed: {name}")
target = ROOT / "src" / "ap_week09" / "traversal.py"
try:
    source = target.read_text(encoding="utf-8")
    normalized = source.replace("\r\n", "\n")
    pattern = r"(?m)(    # BEGIN TODO [123]: [^\n]+\n).*?(    # END TODO [123])"
    matches = list(re.finditer(pattern, normalized, flags=re.DOTALL))
    if len(matches) != 3:
        failures.append("keep all three BEGIN/END TODO markers")
    masked = re.sub(pattern, r"\1    <STUDENT REGION>\n\2", normalized, flags=re.DOTALL)
    if hashlib.sha256(masked.encode()).hexdigest() != contract["traversal_outside_regions_sha256"]:
        failures.append("traversal.py changed outside the three algorithm regions")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
            if isinstance(node.exc.func, ast.Name) and node.exc.func.id == "NotImplementedError":
                failures.append("an algorithm region still raises NotImplementedError")
except Exception as error:
    failures.append(f"cannot inspect traversal.py: {error}")
if failures:
    print("LOCAL FILE CHECK FAIL")
    print("\n".join(failures))
    raise SystemExit(1)
print("LOCAL FILE CHECK PASS")
print("Supplied files and edit boundaries are intact. Check tests, GitHub and LMS separately.")
