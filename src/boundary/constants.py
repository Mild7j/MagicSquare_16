"""Named constants for Boundary-layer contracts."""

from __future__ import annotations

GRID_DIMENSION: int = 4
BLANK_VALUE: int = 0
EXPECTED_BLANK_COUNT: int = 2
INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."
INVALID_BLANK_COUNT_CODE: str = "INVALID_BLANK_COUNT"
INVALID_BLANK_COUNT_MESSAGE: str = "입력 오류: 빈칸(0)은 정확히 2개여야 합니다."
UNSOLVABLE_CODE: str = "UNSOLVABLE"
