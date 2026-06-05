# Golden Master (UI Track SSOT)

승인된 CLI 출력 기준선과 승인 이력을 보관합니다.

## 범위 (Dual-Track)

Golden Master는 **boundary(UI Track) 전용**입니다. entity·control(Logic Track, `D-*`)은 숫자·예외·dict 등을 **직접 assert**하고, CLI stdout 전체 계약만 `golden/`에 둡니다.

| Track | Layer | 검증 | Golden Master |
|-------|-------|------|---------------|
| Logic (`D-*`) | entity, control | `tests/entity/`, `tests/control/` | 사용 안 함 |
| UI (`U-*`) | boundary | `tests/boundary/` | `golden/<case>/output.txt` |

향후 JSON/CSV 등 출력 형식이 생겨도 boundary Golden Master로 확장하고, 변환·검증 로직은 Logic Track assert를 유지합니다.

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
- **테스트:** `tests/boundary/test_u_cli_01.py` · `test_u_cli_rejections.py` (U-CLI-02~05 parametrize) → `golden_loader.load_golden_master(name)`
- **대응 ID:** [reference.md](../.cursor/skills/unit-conversion-tdd/reference.md) U-CLI-*

## 승인 절차

1. UI 테스트 RED 또는 의도적 출력 변경 확인
2. `output.txt` 갱신 + `approval.yaml`에 `approved_at`, `reason`, `commit` 기록
3. `pytest tests/boundary -q` 통과 확인