"""D-EXT-02 — FR-5/SC2: 등록만으로 확장 (OCP)."""

import pytest


def test_d_ext_02_register_without_core_change(cubit_registration, g1_meter_to_feet):
    # Given: cubit 등록 + 기존 G1 meter→feet 케이스
    # When: register_unit("cubit", 0.4572) 후 convert_length(2.5, "meter", "feet")
    # Then: 기존 변환 8.2021 유지 + cubit 변환 가능 (convert_length 본문 수정 없음)
    pytest.fail("RED: D-EXT-02 — 구현 없음, 의도적 실패")
