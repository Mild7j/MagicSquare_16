"""Full FR-01 input validation for Magic Square grids."""

from __future__ import annotations

from src.boundary.schemas import ErrorResponse


class InputValidator:
    """Validates the complete Boundary input contract before Domain execution."""

    def validate(self, matrix: list[list[int]] | None) -> ErrorResponse | None:
        """Run short-circuit input validation (null → size → blanks → range → dup).

        Args:
            matrix: External 4x4 input grid.

        Returns:
            ErrorResponse on contract violation; None when input is valid.

        Raises:
            NotImplementedError: Full FR-01 validation is not implemented yet.
        """
        raise NotImplementedError("InputValidator.validate is not implemented yet.")
