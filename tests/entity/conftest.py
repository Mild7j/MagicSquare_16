"""Shared grid fixtures for Entity/Logic tests (Report/02 SSOT)."""

from __future__ import annotations

import pytest

# G0 — complete valid 4x4 magic square (no zeros)
GRID_G0: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

# G1 — partial grid; blanks (2,2),(3,3) 1-index, missing {7, 10}
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """Return Report/02 G1 partial grid."""
    return [row[:] for row in GRID_G1]
