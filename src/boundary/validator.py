"""Boundary input validation for Magic Square grids."""

from __future__ import annotations

from src.boundary.constants import (
    GRID_DIMENSION,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)
from src.boundary.schemas import ErrorResponse


class BoundaryValidator:
    """Validates external input contracts before Domain processing."""

    def validate_size(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Verify that the grid is exactly 4x4.

        Args:
            grid: Input matrix, or None when absent.

        Returns:
            ErrorResponse when size is invalid; None when size is 4x4.
        """
        if not _has_valid_dimensions(grid):
            return ErrorResponse(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return None


def _has_valid_dimensions(grid: list[list[int]] | None) -> bool:
    """Return True only when grid is a 4x4 matrix."""
    if grid is None or not isinstance(grid, list):
        return False
    if len(grid) != GRID_DIMENSION:
        return False
    return all(isinstance(row, list) and len(row) == GRID_DIMENSION for row in grid)
