"""Find missing numbers in a partial Magic Square grid."""

from __future__ import annotations

from src.entity.value_objects.magic_constant import (
    BLANK_VALUE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)


def find_not_exist_nums(matrix: list[list[int]]) -> list[int]:
    """Return the two missing values from {1..16} in ascending order.

    Args:
        matrix: FR-01-valid 4x4 grid with exactly two zeros.

    Returns:
        Two missing integers sorted ascending.
    """
    present = {
        value
        for row in matrix
        for value in row
        if value != BLANK_VALUE
    }
    full_set = set(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1))
    return sorted(full_set - present)
