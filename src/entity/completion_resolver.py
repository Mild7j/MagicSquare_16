"""Domain resolver for Magic Square completion (Green stub)."""

from __future__ import annotations


class CompletionResolver:
    """Resolves blank cells into a valid Magic Square completion."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Attempt completion for a size-valid grid.

        Args:
            grid: A 4x4 input matrix that passed Boundary size validation.

        Returns:
            Six-element success vector in contract order.

        Raises:
            NotImplementedError: Domain logic is not implemented yet.
        """
        raise NotImplementedError("CompletionResolver.resolve is not implemented yet.")
