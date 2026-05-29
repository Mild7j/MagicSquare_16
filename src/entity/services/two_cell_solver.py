"""Solve a partial Magic Square by trying two number assignments."""

from __future__ import annotations

from copy import deepcopy

from src.entity.services.blank_locator import find_blank_coords
from src.entity.services.magic_square_validator import is_magic_square
from src.entity.services.missing_number_finder import find_not_exist_nums


class UnsolvableDomainError(Exception):
    """Raised when neither assignment attempt yields a valid magic square."""


def _filled_grid(
    matrix: list[list[int]],
    first: tuple[int, int, int],
    second: tuple[int, int, int],
) -> list[list[int]]:
    """Return a copy of matrix with two blank cells filled.

    Args:
        matrix: Source partial grid.
        first: (row, col, value) using 1-index coordinates.
        second: (row, col, value) using 1-index coordinates.

    Returns:
        New 4x4 grid with both blanks replaced.
    """
    filled = deepcopy(matrix)
    for row, col, value in (first, second):
        filled[row - 1][col - 1] = value
    return filled


def solution(matrix: list[list[int]]) -> list[int]:
    """Resolve two blank cells using Attempt-1 then Attempt-2 ordering.

    Args:
        matrix: FR-01-valid 4x4 grid with exactly two zeros.

    Returns:
        Six-element contract vector [r1, c1, n1, r2, c2, n2] with 1-index coords.

    Raises:
        UnsolvableDomainError: When both attempts fail.
    """
    (row1, col1), (row2, col2) = find_blank_coords(matrix)
    smaller, larger = find_not_exist_nums(matrix)

    attempt_one = _filled_grid(
        matrix,
        (row1, col1, smaller),
        (row2, col2, larger),
    )
    if is_magic_square(attempt_one):
        return [row1, col1, smaller, row2, col2, larger]

    attempt_two = _filled_grid(
        matrix,
        (row1, col1, larger),
        (row2, col2, smaller),
    )
    if is_magic_square(attempt_two):
        return [row1, col1, larger, row2, col2, smaller]

    raise UnsolvableDomainError("Neither assignment attempt yields a valid magic square.")
