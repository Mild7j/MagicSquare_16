"""U-OUT-01~03 Boundary output contract RED skeletons (Report/09 Track A)."""

from __future__ import annotations

import pytest

from src.boundary.ui_boundary import UIBoundary

pytestmark = pytest.mark.boundary


class TestUOutSuccessFormatRed:
    """U-OUT-01~03 — success int[6] output contract."""

    def test_u_out_01_success_result_length_is_six(self) -> None:
        """U-OUT-01: valid G1 input → len(result)==6."""
        # Given: G1 surrogate grid (FR-01 pass)
        # When: UIBoundary().solve(grid)  # Control mock may stub domain success
        pytest.fail("RED: U-OUT-01 — success result array length must be 6")

    def test_u_out_02_success_coordinates_are_one_indexed(self) -> None:
        """U-OUT-02: r,c fields ∈ [1,4] (1-index)."""
        # Given: G1 surrogate + expected [2,2,7,3,3,10] or SSOT int[6]
        # When: UIBoundary().solve(grid)
        pytest.fail("RED: U-OUT-02 — coordinates r,c must be 1-index in [1,4]")

    def test_u_out_03_success_field_order_r1_c1_n1_r2_c2_n2(self) -> None:
        """U-OUT-03: tuple order [r1,c1,n1,r2,c2,n2] (BR-13)."""
        # Given: G1 surrogate success path
        # When: UIBoundary().solve(grid)
        pytest.fail("RED: U-OUT-03 — result field order [r1,c1,n1,r2,c2,n2]")
