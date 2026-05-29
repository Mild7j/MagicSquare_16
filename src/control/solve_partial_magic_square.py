"""Control-layer entry point for partial Magic Square resolution."""

from __future__ import annotations

from src.entity.services.blank_locator import find_blank_coords
from src.entity.services.missing_number_finder import find_not_exist_nums
from src.entity.services.two_cell_solver import solution


class SolvePartialMagicSquare:
    """Orchestrates Domain resolution for a size-valid partial grid."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Resolve blank cells into a contract success vector.

        Args:
            grid: A 4x4 input matrix that passed Boundary validation.

        Returns:
            Six-element success vector in contract order.
        """
        find_blank_coords(grid)
        find_not_exist_nums(grid)
        return solution(grid)
