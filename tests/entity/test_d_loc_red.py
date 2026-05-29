"""D-LOC-01 blank coordinate discovery tests (Report/09 Track B)."""

from __future__ import annotations

import pytest

from src.entity.exceptions.domain_errors import InvalidBlankCountError
from src.entity.services.blank_locator import find_blank_coords
from tests.entity.conftest import GRID_G1

pytestmark = pytest.mark.entity


class TestDLocBlankCoordsRed:
    """D-LOC-01 — row-major blank coordinates from G1."""

    def test_d_loc_01_g1_row_major_blank_coords(self, grid_g1: list[list[int]]) -> None:
        """D-LOC-01: G1 → [(2,2),(3,3)] 1-index row-major (Domain Mock 금지)."""
        # Given: GRID_G1 from tests/entity/conftest (Report/02 SSOT)
        grid = grid_g1
        # When: find_blank_coords(grid)
        coords = find_blank_coords(grid)
        # Then: row-major 1-index blanks are (2,2) and (3,3)
        assert coords == [(2, 2), (3, 3)]

    def test_d_loc_invalid_blank_count_raises(self) -> None:
        """D-LOC-01 guard: blank count != 2 raises InvalidBlankCountError."""
        # Given: 4x4 grid with zero blanks
        grid = [row[:] for row in GRID_G1]
        for row_index in range(4):
            for col_index in range(4):
                if grid[row_index][col_index] == 0:
                    grid[row_index][col_index] = 1
        # When/Then: domain rejects invalid blank count
        with pytest.raises(InvalidBlankCountError):
            find_blank_coords(grid)
