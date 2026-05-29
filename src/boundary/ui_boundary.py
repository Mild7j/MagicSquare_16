"""UI Boundary facade for Magic Square solve requests."""

from __future__ import annotations

from src.boundary.schemas import ErrorResponse
from src.boundary.validator import BoundaryValidator
from src.control.exceptions import ResolveError
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
        """Validate input contracts and delegate to Control when validation passes.

        Args:
            matrix: External 4x4 input grid.

        Returns:
            ErrorResponse when validation or resolution fails; otherwise resolver output.
        """
        size_error = self._validator.validate_size(matrix)
        if size_error is not None:
            return size_error

        assert matrix is not None

        blank_error = self._validator.validate_blank_count(matrix)
        if blank_error is not None:
            return blank_error

        try:
            return self._solver.resolve(matrix)
        except ResolveError as exc:
            return ErrorResponse(code=exc.code, message=exc.message)
