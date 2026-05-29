"""D-SOL-01~04 two-cell solver tests (Report/09 Track B)."""

from __future__ import annotations

import pytest

from src.entity.services.two_cell_solver import solution

pytestmark = pytest.mark.entity


class TestDSolTwoCellSolverRed:
    """D-SOL-01~04 — solution() use case (Domain Mock 금지)."""

    def test_d_sol_01_g1_step_a_success_int_six(self, grid_g1: list[list[int]]) -> None:
        """D-SOL-01: G1 FR-05 resolve → [2,2,10,3,3,7] (Attempt-2 success)."""
        # Given: GRID_G1 from tests/entity/conftest
        grid = grid_g1
        # When: solution(grid)
        result = solution(grid)
        # Then: FR-05 success vector for Report/02 G1 literal
        assert result == [2, 2, 10, 3, 3, 7]

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
