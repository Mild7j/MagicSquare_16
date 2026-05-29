"""Application service orchestrating Boundary validation and Domain resolution."""

from __future__ import annotations

from src.boundary.schemas import ErrorResponse
from src.boundary.validator import BoundaryValidator
from src.entity.completion_resolver import CompletionResolver


class MagicSquareService:
    """Coordinates input validation and Domain resolver invocation."""

    def __init__(
        self,
        validator: BoundaryValidator,
        resolver: CompletionResolver,
    ) -> None:
        """Initialize the service with injected dependencies.

        Args:
            validator: Boundary validator for input contracts.
            resolver: Domain resolver for completion logic.
        """
        self._validator = validator
        self._resolver = resolver

    def solve(self, grid: list[list[int]] | None) -> ErrorResponse | list[int]:
        """Validate input and delegate to Domain when size contract passes.

        Args:
            grid: Input matrix from the caller.

        Returns:
            ErrorResponse when Boundary validation fails; otherwise resolver output.
        """
        size_error = self._validator.validate_size(grid)
        if size_error is not None:
            return size_error
        return self._resolver.resolve(grid)
