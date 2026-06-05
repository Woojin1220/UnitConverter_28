# Golden Master (UI Track SSOT)

승인된 CLI 출력 기준선과 승인 이력을 보관합니다.

## 구조

```
golden/
├── manifest.yaml              # 전체 케이스 인덱스
├── u_cli_XX_<name>/
│   ├── output.txt          # Golden Master 본문
│   └── approval.yaml          # 승인 이력
└── README.md
```

## 정책

- **변경·재생성:** 사용자 명시 승인 + `CURSOR_GM_APPROVED=1` (Hook)
- **테스트:** `tests/boundary/test_u_cli_*.py` → `golden_loader.load_golden_master(name)`
- **대응 ID:** [reference.md](../.cursor/skills/unit-conversion-tdd/reference.md) U-CLI-*

## 승인 절차

1. UI 테스트 RED 또는 의도적 출력 변경 확인
2. `output.txt` 갱신 + `approval.yaml`에 `approved_at`, `reason`, `commit` 기록
3. `pytest tests/boundary -q` 통과 확인
