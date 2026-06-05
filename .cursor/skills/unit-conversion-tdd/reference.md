# D-* 테스트 ID (Logic Track)

## Loop 1 — 변환 정확성 (SC1, SC3)

| ID | Layer | 요약 |
|----|-------|------|
| D-CONV-01 | entity | meter → feet 변환 |
| D-CONV-02 | entity | meter → yard 변환 |
| D-CONV-03 | entity | feet → yard (meter 경유) |
| D-CONV-04 | control | 단일 입력 → 전 단위 변환 결과 반환 |
| D-CONV-05 | control | 입력 단위 제외 출력 목록 |

## Loop 2 — 입력 검증 (SC3)

| ID | Layer | 요약 |
|----|-------|------|
| D-VAL-01 | entity | 음수 값 거부 |
| D-VAL-02 | entity | 잘못된 숫자 거부 |
| D-VAL-03 | entity | 미등록 단위 거부 |
| D-VAL-04 | control | 콜론 없는 형식 거부 |
| D-VAL-05 | control | `단위:값` 파싱 성공 |

## Loop 3 — 확장성 (SC2)

| ID | Layer | 요약 |
|----|-------|------|
| D-EXT-01 | entity | 새 단위 등록 후 전체 변환 |
| D-EXT-02 | entity | 기존 변환 로직 수정 없이 등록만으로 확장 |
