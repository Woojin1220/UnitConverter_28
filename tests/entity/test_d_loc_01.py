"""D-LOC-01 — FR-2: convert_length (G1 meter → feet)."""

import pytest


def test_d_loc_01_blank_coords_row_major(g1_meter_to_feet):
    # Given: G1 — 2.5 meter (g1_meter_to_feet 픽스처)
    # When: convert_length(2.5, "meter", "feet") 호출
    # Then: 8.2021 feet 반환 (2.5 × 3.28084)
    pytest.fail("RED: D-LOC-01 — 구현 없음, 의도적 실패")
