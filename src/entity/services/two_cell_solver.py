"""Solve a partial Magic Square by trying two number assignments."""

from __future__ import annotations


class UnsolvableDomainError(Exception):
    """Raised when neither assignment attempt yields a valid magic square."""


def solution(matrix: list[list[int]]) -> list[int]:
    """Resolve two blank cells using Attempt-1 then Attempt-2 ordering.

    Args:
        matrix: FR-01-valid 4x4 grid with exactly two zeros.

    Returns:
        Six-element contract vector [r1, c1, n1, r2, c2, n2] with 1-index coords.

    Raises:
        UnsolvableDomainError: When both attempts fail.
        NotImplementedError: Domain logic is not implemented yet.
    """
    raise NotImplementedError("solution is not implemented yet.")
