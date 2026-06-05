#!/usr/bin/env bash
# beforeShellExecution: block Golden Master / snapshot regen without approval
set -euo pipefail

HOOK_STDIN=$(cat)
export HOOK_STDIN

python - <<'PY'
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

raw = os.environ.get("HOOK_STDIN", "")
try:
    hook_input = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    hook_input = {}

command = hook_input.get("command", "")
approved = os.environ.get("CURSOR_GM_APPROVED", "0") == "1"

BLOCK_PATTERNS = [
    r"--snapshot-update",
    r"--update-snapshots",
    r"snapshot.*update",
    r"tests/boundary/fixtures/",
    r"pytest.*--force",
]

if approved:
    print(json.dumps({"permission": "allow"}, ensure_ascii=True))
    sys.exit(0)

for pattern in BLOCK_PATTERNS:
    if re.search(pattern, command, re.IGNORECASE):
        print(json.dumps({
            "permission": "deny",
            "user_message": "Golden Master/fixture regen requires user approval (CURSOR_GM_APPROVED=1).",
            "agent_message": f"Hook blocked snapshot/fixture regen. Set CURSOR_GM_APPROVED=1 after user approval. Command: {command[:200]}",
        }, ensure_ascii=True))
        sys.exit(0)

print(json.dumps({"permission": "allow"}, ensure_ascii=True))
PY
