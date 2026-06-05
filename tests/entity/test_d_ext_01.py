"""D-EXT-01 — FR-5/FR-9: 새 단위 등록 후 변환 (entity)."""

import pytest


def test_d_ext_01_register_and_convert_all(cubit_registration, cubit_input):
    # Given: cubit 등록 (1 cubit = 0.4572 meter), 값 2.0
    # When: register_unit("cubit", 0.4572) 후 convert_length(2, "cubit", "meter") 등
    # Then: meter·feet·yard 변환 가능 (cubit 기준)
    pytest.fail("RED: D-EXT-01 — 구현 없음, 의도적 실패")
