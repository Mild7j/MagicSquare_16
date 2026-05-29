"""D-LOC-01 blank coordinate discovery RED skeleton (Report/09 Track B)."""

from __future__ import annotations

import pytest

from src.entity.services.blank_locator import find_blank_coords

pytestmark = pytest.mark.entity


class TestDLocBlankCoordsRed:
    """D-LOC-01 — row-major blank coordinates from G1."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        """D-LOC-01: G1 → [(2,2),(3,3)] 1-index row-major (Domain Mock 금지)."""
        # Given: GRID_G1 from tests/entity/conftest (Report/02 SSOT)
        # When: find_blank_coords(grid)
        pytest.fail("RED: D-LOC-01 — G1 row-major blanks (2,2) and (3,3)")
