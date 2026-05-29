"""D-SOL-01~04 two-cell solver RED skeletons (Report/09 Track B)."""

from __future__ import annotations

import pytest

from src.entity.services.two_cell_solver import solution

pytestmark = pytest.mark.entity


class TestDSolTwoCellSolverRed:
    """D-SOL-01~04 — solution() use case (Domain Mock 금지)."""

    def test_d_sol_01_g1_step_a_success_int_six(self) -> None:
        """D-SOL-01: G1 Attempt-1 → [2,2,7,3,3,10] (I8)."""
        # Given: GRID_G1 from tests/entity/conftest
        # When: solution(grid)
        pytest.fail("RED: D-SOL-01 — G1 Step A success [2,2,7,3,3,10]")

    def test_d_sol_02_g2_step_b_success(self) -> None:
        """D-SOL-02: G2 Attempt-1 fail, Attempt-2 success (I9)."""
        # Given: GRID_G2 TBD (Report/02 / PRD TD-02 surrogate)
        # When: solution(grid)
        pytest.fail("RED: D-SOL-02 — G2 TBD Attempt-2 success path")

    def test_d_sol_03_g3_both_attempts_fail_unsolvable(self) -> None:
        """D-SOL-03: G3 both attempts fail → UnsolvableDomainError (I10)."""
        # Given: GRID_G3 placeholder (Report/02)
        # When: solution(grid)
        pytest.fail("RED: D-SOL-03 — G3 unsolvable → UnsolvableDomainError")

    def test_d_sol_04_success_output_length_and_one_index(self) -> None:
        """D-SOL-04: success → len 6, coords 1-index (I8/I9, AC-FR05-04)."""
        # Given: G1 success path (same as D-SOL-01)
        # When: solution(grid)
        pytest.fail("RED: D-SOL-04 — success output len=6 and 1-index coords")
