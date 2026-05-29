"""Golden Master contract validators for solver output shape and rules."""

from __future__ import annotations

import re

from src.boundary.schemas import ErrorResponse
from src.entity.services.blank_locator import find_blank_coords
from src.entity.services.magic_square_validator import is_magic_square
from src.entity.services.missing_number_finder import find_not_exist_nums
from src.entity.services.two_cell_solver import UnsolvableDomainError, solution


_OUTPUT_BLOCK_PATTERN = re.compile(r"^Output:\n\[(?P<body>[\d,]+)\]$", re.MULTILINE)


def parse_output_vector(section_text: str) -> list[int]:
    """Parse an ``Output:`` block from a Golden Master section.

    Args:
        section_text: Serialized scenario section text.

    Returns:
        Six-element success vector.

    Raises:
        ValueError: When the section does not contain a valid output block.
    """
    match = _OUTPUT_BLOCK_PATTERN.search(section_text)
    if match is None:
        raise ValueError("Section does not contain a valid Output block.")
    return [int(part) for part in match.group("body").split(",")]


def parse_error_code(section_text: str) -> str:
    """Parse an ``Error:`` block from a Golden Master section.

    Args:
        section_text: Serialized scenario section text.

    Returns:
        Error code or exception type name.

    Raises:
        ValueError: When the section does not contain a valid error block.
    """
    marker = "Error:\n"
    if marker not in section_text:
        raise ValueError("Section does not contain a valid Error block.")
    return section_text.rsplit(marker, maxsplit=1)[-1].strip()


def assert_int_six_format(vector: list[int]) -> None:
    """Verify success vector length and numeric type contract.

    Args:
        vector: Solver success output.

    Raises:
        AssertionError: When the vector violates ``int[6]`` contract.
    """
    assert isinstance(vector, list), "Success result must be a list."
    assert len(vector) == 6, f"Success vector must have length 6, got {len(vector)}."
    assert all(isinstance(value, int) for value in vector), "All elements must be int."


def assert_one_index_coordinates(row1: int, col1: int, row2: int, col2: int) -> None:
    """Verify blank coordinates use 1-index grid addressing.

    Args:
        row1: First blank row.
        col1: First blank column.
        row2: Second blank row.
        col2: Second blank column.

    Raises:
        AssertionError: When any coordinate is outside 1..4.
    """
    for name, value in (("r1", row1), ("c1", col1), ("r2", row2), ("c2", col2)):
        assert 1 <= value <= 4, f"{name} must be 1-indexed in 1..4, got {value}."


def assert_row_major_blank_order(
    grid: list[list[int]],
    row1: int,
    col1: int,
    row2: int,
    col2: int,
) -> None:
    """Verify blanks appear in row-major order in the success vector.

    Args:
        grid: Input partial grid.
        row1: Reported first blank row.
        col1: Reported first blank column.
        row2: Reported second blank row.
        col2: Reported second blank column.

    Raises:
        AssertionError: When reported blanks differ from row-major scan order.
    """
    expected = find_blank_coords(grid)
    assert (row1, col1) == expected[0], (
        f"First blank must be row-major {expected[0]}, got ({row1},{col1})."
    )
    assert (row2, col2) == expected[1], (
        f"Second blank must be row-major {expected[1]}, got ({row2},{col2})."
    )


def _filled_grid(
    grid: list[list[int]],
    row1: int,
    col1: int,
    n1: int,
    row2: int,
    col2: int,
    n2: int,
) -> list[list[int]]:
    """Return a copy of ``grid`` with two blanks filled using 1-index coordinates."""
    filled = [row[:] for row in grid]
    filled[row1 - 1][col1 - 1] = n1
    filled[row2 - 1][col2 - 1] = n2
    return filled


def assert_small_first_combination(grid: list[list[int]], vector: list[int]) -> None:
    """Verify Attempt 1 (smaller missing first) produced the reported success vector.

    Args:
        grid: Input partial grid.
        vector: Solver success output.

    Raises:
        AssertionError: When Attempt 1 ordering or magic property is violated.
    """
    row1, col1, n1, row2, col2, n2 = vector
    smaller, larger = find_not_exist_nums(grid)
    attempt_one = _filled_grid(grid, row1, col1, smaller, row2, col2, larger)
    assert is_magic_square(attempt_one), "Attempt 1 (small-first) must yield a magic square."
    assert vector == [row1, col1, smaller, row2, col2, larger], (
        "Success vector must follow small-first Attempt 1 ordering "
        f"[r1,c1,smaller,r2,c2,larger] -> "
        f"[{row1},{col1},{smaller},{row2},{col2},{larger}]."
    )


def assert_reverse_fallback_combination(grid: list[list[int]], vector: list[int]) -> None:
    """Verify Attempt 1 failed and Attempt 2 (reverse) produced the success vector.

    Args:
        grid: Input partial grid.
        vector: Solver success output.

    Raises:
        AssertionError: When reverse fallback rules are violated.
    """
    row1, col1, n1, row2, col2, n2 = vector
    smaller, larger = find_not_exist_nums(grid)
    attempt_one = _filled_grid(grid, row1, col1, smaller, row2, col2, larger)
    attempt_two = _filled_grid(grid, row1, col1, larger, row2, col2, smaller)
    assert not is_magic_square(attempt_one), "Attempt 1 must fail before reverse fallback."
    assert is_magic_square(attempt_two), "Attempt 2 (reverse) must yield a magic square."
    assert vector == [row1, col1, larger, row2, col2, smaller], (
        "Success vector must follow reverse Attempt 2 ordering "
        f"[r1,c1,larger,r2,c2,smaller] -> "
        f"[{row1},{col1},{larger},{row2},{col2},{smaller}]."
    )


def assert_success_contract(grid: list[list[int]], vector: list[int]) -> None:
    """Apply all success-path Golden Master contract checks.

    Args:
        grid: Input partial grid.
        vector: Solver success output.
    """
    assert_int_six_format(vector)
    row1, col1, _, row2, col2, _ = vector
    assert_one_index_coordinates(row1, col1, row2, col2)
    assert_row_major_blank_order(grid, row1, col1, row2, col2)
    assert vector == solution(grid), "Live solver output must match domain oracle."


def assert_error_contract(result: ErrorResponse | BaseException, expected_code: str) -> None:
    """Verify error-path contract against the Golden Master error code.

    Args:
        result: Observed boundary failure or captured exception.
        expected_code: Code recorded in the baseline file.

    Raises:
        AssertionError: When the error contract does not match expectation.
    """
    if isinstance(result, ErrorResponse):
        assert result.code == expected_code, (
            f"Error code mismatch: expected {expected_code}, got {result.code}."
        )
        assert result.message, "ErrorResponse.message must be non-empty."
        return
    if isinstance(result, BaseException):
        assert type(result).__name__ == expected_code, (
            f"Exception type mismatch: expected {expected_code}, "
            f"got {type(result).__name__}."
        )
        return
    raise AssertionError(f"Expected error outcome, got success vector {result!r}.")


def assert_unsolvable_contract(grid: list[list[int]]) -> None:
    """Verify that the domain reports no valid assignment for the grid.

    Args:
        grid: Input partial grid.

    Raises:
        AssertionError: When a solution exists contrary to unsolvable expectation.
    """
    try:
        solution(grid)
    except UnsolvableDomainError:
        return
    raise AssertionError("Grid must be unsolvable at Domain layer.")
