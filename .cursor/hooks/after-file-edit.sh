#!/usr/bin/env bash
# afterFileEdit: Layer pytest + Logic Track TDD violation check (skip/xfail/mock)
set -euo pipefail

HOOK_STDIN=$(cat)
export HOOK_STDIN

python - <<'PY'
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

raw = os.environ.get("HOOK_STDIN", "")
try:
    hook_input = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    hook_input = {}

file_path = hook_input.get("file_path", "")
path = Path(file_path.replace("\\", "/")) if file_path else None
parts = path.parts if path else ()

violations: list[str] = []
pytest_layers: list[str] = []

def layer_from_parts(parts: tuple[str, ...]) -> str | None:
    joined = "/".join(parts).replace("\\", "/")
    for layer in ("entity", "control", "boundary"):
        if f"src/{layer}" in joined or f"tests/{layer}" in joined:
            return layer
    if joined.endswith("UnitConverter.py"):
        return "boundary"
    return None

if path and path.suffix == ".py" and "tests" in parts:
    rel = "/".join(parts[-3:]) if len(parts) >= 3 else str(path)
    if any(p in parts for p in ("entity", "control")):
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            content = ""
        if re.search(r"@pytest\.mark\.(skip|xfail)", content):
            violations.append(f"TDD 금지: skip/xfail in {rel}")
        if re.search(r"(unittest\.mock|from unittest import mock|monkeypatch\.setattr)", content):
            if "tests/boundary" not in "/".join(parts):
                violations.append(f"Logic Track: Domain Mock in {rel}")

layer = layer_from_parts(parts) if parts else None
if layer:
    pytest_layers.append(f"tests/{layer}")

messages: list[str] = []
if violations:
    messages.append("[Hook] TDD/Logic Track violations:\n- " + "\n- ".join(violations))

for target in pytest_layers:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", target, "-q"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path.cwd(),
        )
        summary = (result.stdout + result.stderr).strip().splitlines()
        tail = "\n".join(summary[-8:]) if summary else "(no output)"
        status = "PASS" if result.returncode == 0 else f"FAIL (exit {result.returncode})"
        messages.append(f"[Hook] pytest {target} -q -> {status}\n{tail}")
    except subprocess.TimeoutExpired:
        messages.append(f"[Hook] pytest {target} -q -> TIMEOUT")
    except Exception as exc:
        messages.append(f"[Hook] pytest {target} -q -> ERROR: {exc}")

# afterFileEdit: informational; emit context if supported
if messages:
    print(json.dumps({"additional_context": "\n\n".join(messages)}, ensure_ascii=True))
else:
    print("{}")
PY
