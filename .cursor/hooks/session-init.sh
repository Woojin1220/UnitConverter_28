#!/usr/bin/env bash
# UnitConverter - sessionStart hook
# Injects ECB + Dual-Track TDD context and session env for subsequent hooks.
set -euo pipefail

HOOK_STDIN=$(cat)
export HOOK_STDIN

python - <<'PY'
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

hook_input: dict = {}
raw = os.environ.get("HOOK_STDIN", "")
if raw.strip():
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        pass

composer_mode = hook_input.get("composer_mode", "unknown")
session_id = hook_input.get("session_id", "")

context = f"""[UnitConverter - Session Init]
프로젝트: ECB + Dual-Track TDD 단위 변환기
세션: {session_id or "n/a"} | 모드: {composer_mode}

## 아키텍처 (ECB)
- 의존: boundary → control → entity (단방향)
- entity: 상위 import 금지 | control: entity만 | boundary: control만

## Dual-Track
- Logic (D-*): tests/entity, tests/control — Domain Mock 금지
- UI (U-*): tests/boundary — control·I/O mock 허용, entity mock 금지

## TDD
- RED → GREEN → REFACTOR | 구현 순서: entity → control → boundary
- 응답 첫 줄: Phase: RED|GREEN|REFACTOR | Layer: entity|control|boundary | Track: Logic|UI
- 정책: .cursorrules | 절차: .cursor/skills/unit-conversion-tdd/SKILL.md

## pytest (Review Loop)
- Layer: pytest tests/<layer> -q
- 전체: pytest -q

## Golden Master
- fixtures: tests/boundary/fixtures/
- 재생성: 사용자 명시 승인 후 CURSOR_GM_APPROVED=1 일 때만

## 참고
- D-* ID: .cursor/skills/unit-conversion-tdd/reference.md
- ECB 리뷰(수정 금지): /review-ecb
"""

output = {
    "env": {
        "UNIT_CONVERTER_PROJECT": "1",
        "CURSOR_GM_APPROVED": os.environ.get("CURSOR_GM_APPROVED", "0"),
    },
    "additional_context": context,
}

print(json.dumps(output, ensure_ascii=False))
PY
