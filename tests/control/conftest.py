"""Shared fixtures for Control-layer isolation tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.boundary.validator import BoundaryValidator
from src.control.magic_square_service import MagicSquareService
from src.entity.completion_resolver import CompletionResolver


@pytest.fixture
def mock_resolver() -> Mock:
    return Mock(spec=CompletionResolver)


@pytest.fixture
def magic_square_service(mock_resolver: Mock) -> MagicSquareService:
    return MagicSquareService(
        validator=BoundaryValidator(),
        resolver=mock_resolver,
    )
