"""UI Boundary facade for Magic Square solve requests."""

from __future__ import annotations

from src.boundary.schemas import ErrorResponse
from src.boundary.validator import BoundaryValidator
from src.control.solve_partial_magic_square import SolvePartialMagicSquare


class UIBoundary:
    """Orchestrates input validation and Control resolution for external callers."""

    def __init__(
        self,
        validator: BoundaryValidator | None = None,
        solver: SolvePartialMagicSquare | None = None,
    ) -> None:
        """Initialize the boundary facade with injectable dependencies.

        Args:
            validator: Boundary validator for input size contracts.
            solver: Control-layer resolver for size-valid grids.
        """
        self._validator = validator or BoundaryValidator()
        self._solver = solver or SolvePartialMagicSquare()

    def solve(self, matrix: list[list[int]] | None) -> ErrorResponse | list[int]:
        """Validate input size and delegate to Control when the contract passes.

        Args:
            matrix: External 4x4 input grid.

        Returns:
            ErrorResponse when size validation fails; otherwise resolver output.
        """
        size_error = self._validator.validate_size(matrix)
        if size_error is not None:
            return size_error
        return self._solver.resolve(matrix)
