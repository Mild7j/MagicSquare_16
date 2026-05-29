"""U-IN-04~08 Boundary input validation RED skeletons (Report/09 Track A)."""

from __future__ import annotations

import pytest

from src.boundary.input_validator import InputValidator

pytestmark = pytest.mark.boundary


class TestUInBlankCountRed:
    """U-IN-04, U-IN-08 — blank count violations (E002)."""

    def test_u_in_04_three_empty_cells_returns_e002(self) -> None:
        """U-IN-04: three zeros → E002 INVALID_BLANK_COUNT."""
        # Given: grid = [[16,2,0,13],[5,0,10,8],[9,7,6,0],[4,14,15,1]]
        # When: InputValidator().validate(grid)
        pytest.fail("RED: U-IN-04 — blank count 3 → E002 envelope")

    def test_u_in_08_one_empty_cell_returns_e002(self) -> None:
        """U-IN-08: single zero → E002 INVALID_BLANK_COUNT."""
        # Given: 4x4 grid with exactly one 0 (FR-01 blank count rule)
        # When: InputValidator().validate(grid)
        pytest.fail("RED: U-IN-08 — blank count 1 → E002 envelope")


class TestUInRangeRed:
    """U-IN-05, U-IN-06 — value range violations (E004)."""

    def test_u_in_05_negative_value_returns_e004(self) -> None:
        """U-IN-05: cell value -1 → E004 OUT_OF_RANGE."""
        # Given: grid = [[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,-1]]
        # When: InputValidator().validate(grid)
        pytest.fail("RED: U-IN-05 — value -1 → E004 envelope")

    def test_u_in_06_seventeen_returns_e004(self) -> None:
        """U-IN-06: cell value 17 → E004 OUT_OF_RANGE (PRD TD-06)."""
        # Given: grid = [[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,17]]
        # When: InputValidator().validate(grid)
        pytest.fail("RED: U-IN-06 — value 17 → E004 envelope")


class TestUInDuplicateRed:
    """U-IN-07 — non-zero duplicate (E005)."""

    def test_u_in_07_duplicate_non_zero_returns_e005(self) -> None:
        """U-IN-07: duplicate 16 → E005 DUPLICATE_NON_ZERO (PRD TD-05)."""
        # Given: grid = [[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,16]]
        # When: InputValidator().validate(grid)
        pytest.fail("RED: U-IN-07 — non-zero duplicate → E005 envelope")
