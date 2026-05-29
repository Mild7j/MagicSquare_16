"""UIBoundary solve contract tests for blank-count validation and ECB mapping."""

from __future__ import annotations

import pytest

from src.boundary.constants import INVALID_BLANK_COUNT_MESSAGE
from src.boundary.schemas import ErrorResponse
from src.boundary.ui_boundary import UIBoundary
from tests.entity.conftest import GRID_G1

pytestmark = pytest.mark.boundary


class TestUIBoundaryBlankCount:
    """AC-FR01-02 — blank count violations return ErrorResponse at Boundary."""

    def test_all_zero_grid_returns_invalid_blank_count(self) -> None:
        """Blank count 16 → INVALID_BLANK_COUNT without leaking ValueError."""
        # Given: size-valid grid with no valid blank count
        grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # When: UIBoundary.solve(grid)
        result = UIBoundary().solve(grid)
        # Then: structured boundary failure is returned
        assert isinstance(result, ErrorResponse)
        assert result.code == "INVALID_BLANK_COUNT"
        assert result.message == INVALID_BLANK_COUNT_MESSAGE

    def test_g1_grid_returns_success_vector(self) -> None:
        """G1 valid partial grid resolves through Control without entity imports."""
        # Given: Report/02 G1 with exactly two blanks
        grid = [row[:] for row in GRID_G1]
        # When: UIBoundary.solve(grid)
        result = UIBoundary().solve(grid)
        # Then: success vector is returned (FR-05 Attempt-2 for this literal)
        assert result == [2, 2, 10, 3, 3, 7]
