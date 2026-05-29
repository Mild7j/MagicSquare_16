"""D-MIS-01 missing number discovery RED skeleton (Report/09 Track B)."""

from __future__ import annotations

import pytest

from src.entity.services.missing_number_finder import find_not_exist_nums

pytestmark = pytest.mark.entity


class TestDMisMissingNumbersRed:
    """D-MIS-01 — missing numbers ascending from G1."""

    def test_d_mis_01_g1_missing_numbers_sorted(self) -> None:
        """D-MIS-01: G1 → [7, 10] ascending (Domain Mock 금지)."""
        # Given: GRID_G1 from tests/entity/conftest
        # When: find_not_exist_nums(grid)
        pytest.fail("RED: D-MIS-01 — G1 missing numbers {7,10} ascending")
