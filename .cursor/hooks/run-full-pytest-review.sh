#!/usr/bin/env bash
# stop: full pytest -q review loop gate at end of agent turn
set -euo pipefail

HOOK_STDIN=$(cat)
export HOOK_STDIN

python - <<'PY'
import json
import os
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

status = hook_input.get("status", "completed")
loop_count = hook_input.get("loop_count", 0)

if status != "completed":
    print("{}")
    sys.exit(0)

try:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=Path.cwd(),
    )
except subprocess.TimeoutExpired:
    print(json.dumps({
        "followup_message": "[Hook/Review] pytest -q TIMEOUT. Phase 종료 전 전체 테스트를 확인하세요."
    }, ensure_ascii=True))
    sys.exit(0)

if result.returncode != 0:
    tail = (result.stdout + result.stderr).strip().splitlines()
    excerpt = "\n".join(tail[-12:]) if tail else "(no output)"
    print(json.dumps({
        "followup_message": (
            f"[Hook/Review] pytest -q FAILED (exit {result.returncode}, loop {loop_count}).\n"
            f"REFACTOR/릴리스 게이트 미충족. 실패를 수정한 뒤 다시 pytest -q 를 통과시키세요.\n\n"
            f"{excerpt}"
        )
    }, ensure_ascii=True))
else:
    print("{}")
PY
