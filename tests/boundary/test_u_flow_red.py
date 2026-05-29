"""U-FLOW-02 extended — Domain execute isolation RED skeletons (Report/09 Track A)."""

from __future__ import annotations

import pytest

from src.boundary.ui_boundary import UIBoundary

pytestmark = pytest.mark.boundary


class TestUFlow02ExecuteIsolationRed:
    """U-FLOW-02 — invalid input must not call SolvePartialMagicSquare.execute."""

    def test_u_flow_02_null_grid_execute_call_count_zero(self) -> None:
        """U-FLOW-02a: matrix=null → execute.call_count==0."""
        # Given: matrix = None; spy on SolvePartialMagicSquare.execute (Control mock)
        # When: UIBoundary().solve(matrix)
        pytest.fail("RED: U-FLOW-02 — null input → execute 0 calls")

    def test_u_flow_02_invalid_blank_count_execute_call_count_zero(self) -> None:
        """U-FLOW-02b: E002 path → execute.call_count==0."""
        # Given: grid with blank count != 2; execute spy
        # When: UIBoundary().solve(grid)
        pytest.fail("RED: U-FLOW-02 — invalid blank count → execute 0 calls")

    def test_u_flow_02_out_of_range_execute_call_count_zero(self) -> None:
        """U-FLOW-02c: E004 path → execute.call_count==0."""
        # Given: grid with value 17 (PRD TD-06); execute spy
        # When: UIBoundary().solve(grid)
        pytest.fail("RED: U-FLOW-02 — out-of-range input → execute 0 calls")

    def test_u_flow_02_duplicate_non_zero_execute_call_count_zero(self) -> None:
        """U-FLOW-02d: E005 path → execute.call_count==0."""
        # Given: grid with duplicate non-zero (PRD TD-05); execute spy
        # When: UIBoundary().solve(grid)
        pytest.fail("RED: U-FLOW-02 — duplicate non-zero → execute 0 calls")
