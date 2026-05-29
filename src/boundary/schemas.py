"""Pydantic schemas for Boundary-layer responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard failure response returned by the Boundary layer.

    Attributes:
        code: Machine-readable error code.
        message: Human-readable error message.
    """

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
