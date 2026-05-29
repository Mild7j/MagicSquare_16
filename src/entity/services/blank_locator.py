"""Locate blank cell coordinates in a partial Magic Square grid."""

from __future__ import annotations

from src.entity.value_objects.grid_size import GRID_SIZE
from src.entity.value_objects.magic_constant import BLANK_VALUE


def find_blank_coords(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """Return two blank coordinates in row-major order (1-index).

    Args:
        matrix: FR-01-valid 4x4 grid with exactly two zeros.

    Returns:
        Two (row, col) pairs using 1-index coordinates.
    """
    coords: list[tuple[int, int]] = []
    for row_index in range(GRID_SIZE):
        for col_index in range(GRID_SIZE):
            if matrix[row_index][col_index] == BLANK_VALUE:
                coords.append((row_index + 1, col_index + 1))
    return coords
