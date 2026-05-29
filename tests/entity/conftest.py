"""Shared grid fixtures for Entity/Logic RED skeleton tests (Report/09).

G0~G3 literals are placeholders until Report/02 SSOT is published.
Uncomment and wire fixtures during GREEN phase.
"""

from __future__ import annotations

# G0 — complete valid 4x4 magic square (no zeros)
# GRID_G0: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 15, 1],
# ]

# G1 — partial grid; SSOT blanks (2,2),(3,3) 1-index, missing {7, 10}
# Surrogate (PRD TD-01): blanks (1,3),(3,4), missing {3, 12}
# GRID_G1: list[list[int]] = [
#     [16, 2, 0, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 0],
#     [4, 14, 15, 1],
# ]

# G2 — Attempt-2 success path (PRD TD-02); exact expected int[6] TBD
# GRID_G2: list[list[int]] = [
#     [0, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 15, 0],
# ]

# G3 — unsolvable partial grid (Report/02 placeholder)
# GRID_G3: list[list[int]] = [...]
