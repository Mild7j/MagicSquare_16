"""D-VAL-01~06 magic square validation RED skeletons (Report/09 Track B)."""

from __future__ import annotations

import pytest

from src.entity.services.magic_square_validator import is_magic_square

pytestmark = pytest.mark.entity


class TestDValMagicSquareRed:
    """D-VAL-01~06 — is_magic_square on G0 and mutations (Domain Mock 금지)."""

    def test_d_val_01_g0_complete_grid_returns_true(self) -> None:
        """D-VAL-01: G0 complete grid → True (I1~I5)."""
        # Given: GRID_G0 from tests/entity/conftest
        # When: is_magic_square(grid)
        pytest.fail("RED: D-VAL-01 — G0 complete magic square → true")

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        """D-VAL-02: row sum violation → False (I1)."""
        # Given: G0 with row-1 sum broken
        # When: is_magic_square(grid)
        pytest.fail("RED: D-VAL-02 — row sum mismatch → false")

    def test_d_val_03_col_sum_mismatch_returns_false(self) -> None:
        """D-VAL-03: column sum violation → False (I2)."""
        # Given: G0 with column-1 sum broken
        # When: is_magic_square(grid)
        pytest.fail("RED: D-VAL-03 — column sum mismatch → false")

    def test_d_val_04_diagonal_sum_mismatch_returns_false(self) -> None:
        """D-VAL-04: diagonal sum violation → False (I3)."""
        # Given: G0 with main diagonal sum broken
        # When: is_magic_square(grid)
        pytest.fail("RED: D-VAL-04 — diagonal sum mismatch → false")

    def test_d_val_05_value_set_violation_returns_false(self) -> None:
        """D-VAL-05: 1~16 set violation / duplicate → False (I4)."""
        # Given: G0 with duplicate or out-of-set value
        # When: is_magic_square(grid)
        pytest.fail("RED: D-VAL-05 — value set {1..16} violation → false")

    def test_d_val_06_zero_in_complete_grid_returns_false(self) -> None:
        """D-VAL-06: zero present in complete candidate → False (I4)."""
        # Given: G0 with one cell replaced by 0
        # When: is_magic_square(grid)
        pytest.fail("RED: D-VAL-06 — zero in complete grid → false")
