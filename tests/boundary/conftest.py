"""Shared fixtures for Boundary AC-FR-01-01 tests."""

from __future__ import annotations

import os

import pytest

from src.boundary.schemas import ErrorResponse
from src.boundary.validator import BoundaryValidator

from tests.boundary.constants import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


@pytest.fixture
def approve_golden_master() -> bool:
    """Return True when Golden Master baseline regeneration is requested."""
    return os.environ.get("GOLDEN_MASTER_APPROVE", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }


@pytest.fixture
def boundary_validator() -> BoundaryValidator:
    return BoundaryValidator()


@pytest.fixture
def expected_invalid_size_error() -> ErrorResponse:
    return ErrorResponse(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE)
