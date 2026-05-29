"""Validate whether a completed grid satisfies Magic Square invariants."""

from __future__ import annotations

from src.entity.value_objects.grid_size import GRID_SIZE
from src.entity.value_objects.magic_constant import (
    BLANK_VALUE,
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)


def is_magic_square(matrix: list[list[int]]) -> bool:
    """Return True when all row/column/diagonal sums equal the magic constant.

    Args:
        matrix: Completed 4x4 candidate without zeros.

    Returns:
        True if the grid is a valid magic square; False otherwise.
    """
    if any(BLANK_VALUE in row for row in matrix):
        return False

    present = {value for row in matrix for value in row}
    if present != set(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)):
        return False

    for row_index in range(GRID_SIZE):
        if sum(matrix[row_index]) != MAGIC_CONSTANT:
            return False

    for col_index in range(GRID_SIZE):
        if sum(matrix[row_index][col_index] for row_index in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False

    main_diagonal = sum(matrix[index][index] for index in range(GRID_SIZE))
    anti_diagonal = sum(
        matrix[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)
    )
    return main_diagonal == MAGIC_CONSTANT and anti_diagonal == MAGIC_CONSTANT
