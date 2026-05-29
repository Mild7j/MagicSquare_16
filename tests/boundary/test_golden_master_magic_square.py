"""GM-2 Golden Master regression tests for Magic Square Solver."""

from __future__ import annotations

import pytest
from src.boundary.schemas import ErrorResponse

from tests.golden_master.approve import assert_golden_master_matches, assert_scenario_matches
from tests.golden_master.contracts import (
    assert_error_contract,
    assert_int_six_format,
    assert_reverse_fallback_combination,
    assert_row_major_blank_order,
    assert_small_first_combination,
    assert_success_contract,
    assert_unsolvable_contract,
    parse_error_code,
    parse_output_vector,
)
from tests.golden_master.scenarios import (
    DUPLICATE_NUMBER_GRID,
    INVALID_BLANK_COUNT_GRID,
    NO_VALID_SOLUTION_GRID,
    NORMAL_SUCCESS_GRID,
    REVERSE_SUCCESS_GRID,
    capture_solve_result,
)

pytestmark = [pytest.mark.boundary, pytest.mark.golden_master]


class TestGoldenMasterMagicSquareDocument:
    """Full-document Golden Master approve regression."""

    def test_golden_master_expected_file_matches_live_solver(
        self,
        approve_golden_master: bool,
    ) -> None:
        """Entire ``golden_master_expected.txt`` matches live API serialization."""
        assert_golden_master_matches(approve=approve_golden_master)


class TestGoldenMasterMagicSquare:
    """GM-TC-01~05 — per-scenario Golden Master tests with contract checks."""

    def test_gm_tc_01_normal_success(
        self,
        approve_golden_master: bool,
    ) -> None:
        """GM-TC-01: 정상 조합 성공 — int[6], row-major, 1-index, small-first."""
        expected_section = assert_scenario_matches("GM-TC-01", approve=approve_golden_master)
        result = capture_solve_result(NORMAL_SUCCESS_GRID)
        assert isinstance(result, list)
        vector = parse_output_vector(expected_section)
        assert result == vector
        assert_success_contract(NORMAL_SUCCESS_GRID, vector)
        assert_small_first_combination(NORMAL_SUCCESS_GRID, vector)

    def test_gm_tc_02_reverse_success(
        self,
        approve_golden_master: bool,
    ) -> None:
        """GM-TC-02: reverse 조합 성공 — Attempt 1 fail, Attempt 2 fallback."""
        expected_section = assert_scenario_matches("GM-TC-02", approve=approve_golden_master)
        result = capture_solve_result(REVERSE_SUCCESS_GRID)
        assert isinstance(result, list)
        vector = parse_output_vector(expected_section)
        assert result == vector
        assert_success_contract(REVERSE_SUCCESS_GRID, vector)
        assert_reverse_fallback_combination(REVERSE_SUCCESS_GRID, vector)

    def test_gm_tc_03_invalid_blank_count(
        self,
        approve_golden_master: bool,
    ) -> None:
        """GM-TC-03: INVALID_BLANK_COUNT error contract."""
        expected_section = assert_scenario_matches("GM-TC-03", approve=approve_golden_master)
        result = capture_solve_result(INVALID_BLANK_COUNT_GRID)
        expected_code = parse_error_code(expected_section)
        assert_error_contract(result, expected_code)
        assert isinstance(result, ErrorResponse)
        assert result.code == "INVALID_BLANK_COUNT"

    def test_gm_tc_04_duplicate_number(
        self,
        approve_golden_master: bool,
    ) -> None:
        """GM-TC-04: DUPLICATE_NUMBER error contract (baseline tracks live behavior)."""
        expected_section = assert_scenario_matches("GM-TC-04", approve=approve_golden_master)
        result = capture_solve_result(DUPLICATE_NUMBER_GRID)
        expected_code = parse_error_code(expected_section)
        assert_error_contract(result, expected_code)

    def test_gm_tc_05_no_valid_magic_square(
        self,
        approve_golden_master: bool,
    ) -> None:
        """GM-TC-05: NO_VALID_MAGIC_SQUARE / UNSOLVABLE error contract."""
        expected_section = assert_scenario_matches("GM-TC-05", approve=approve_golden_master)
        result = capture_solve_result(NO_VALID_SOLUTION_GRID)
        expected_code = parse_error_code(expected_section)
        assert_error_contract(result, expected_code)
        assert isinstance(result, ErrorResponse)
        assert result.code == "UNSOLVABLE"
        assert_unsolvable_contract(NO_VALID_SOLUTION_GRID)


class TestGoldenMasterMagicSquareOutputShape:
    """Cross-cutting output shape checks derived from Golden Master success paths."""

    @pytest.mark.parametrize(
        "grid",
        [NORMAL_SUCCESS_GRID, REVERSE_SUCCESS_GRID],
        ids=["GM-TC-01", "GM-TC-02"],
    )
    def test_success_vector_int_six_and_row_major(
        self,
        grid: list[list[int]],
    ) -> None:
        """Success vectors satisfy int[6], 1-index, and row-major blank ordering."""
        result = capture_solve_result(grid)
        assert isinstance(result, list)
        assert_int_six_format(result)
        row1, col1, _, row2, col2, _ = result
        assert_row_major_blank_order(grid, row1, col1, row2, col2)
