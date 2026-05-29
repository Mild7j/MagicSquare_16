"""UI Boundary facade for Magic Square solve requests."""

from __future__ import annotations

from src.boundary.schemas import ErrorResponse


class UIBoundary:
    """Orchestrates input validation and Domain execution for external callers."""

    def solve(self, matrix: list[list[int]] | None) -> ErrorResponse | list[int]:
        """Validate input and return a contract result or failure envelope.

        Args:
            matrix: External 4x4 input grid.

        Returns:
            Six-element success vector or standard ErrorResponse on failure.

        Raises:
            NotImplementedError: Boundary orchestration is not implemented yet.
        """
        raise NotImplementedError("UIBoundary.solve is not implemented yet.")
