"""Control-layer exceptions surfaced to Boundary callers."""

from __future__ import annotations


class ResolveError(Exception):
    """Raised when Control cannot produce a success vector for a valid-sized grid."""

    def __init__(self, code: str, message: str) -> None:
        """Initialize with a contract error code and message.

        Args:
            code: Machine-readable error code for Boundary mapping.
            message: Human-readable failure description.
        """
        super().__init__(message)
        self.code = code
        self.message = message
