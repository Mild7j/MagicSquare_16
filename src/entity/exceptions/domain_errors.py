"""Domain-level errors raised by entity services."""

from __future__ import annotations

INVALID_BLANK_COUNT_MESSAGE = "입력 오류: 빈칸(0)은 정확히 2개여야 합니다."


class InvalidBlankCountError(Exception):
    """Raised when a grid does not contain exactly two blank cells."""

    def __init__(self, message: str = INVALID_BLANK_COUNT_MESSAGE) -> None:
        """Initialize with a human-readable message.

        Args:
            message: Description of the blank-count violation.
        """
        super().__init__(message)
