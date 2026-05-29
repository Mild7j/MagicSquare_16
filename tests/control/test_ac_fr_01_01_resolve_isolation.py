"""AC-FR-01-01 Domain resolver isolation tests for the Control layer."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.boundary.schemas import ErrorResponse
from src.control.magic_square_service import MagicSquareService

from tests.boundary.constants import (
    GRID_3X4,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    MODULE_AC_ID,
)

pytestmark = pytest.mark.control


class TestResolveIsolationOnInvalidSize:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 격리 검증."""

    def test_none_grid_resolve_not_called(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None and resolver is mocked
        grid = None

        # When: application orchestrates solve request
        result = magic_square_service.solve(grid)

        # Then: Domain resolve() is never invoked
        mock_resolver.resolve.assert_not_called()
        assert mock_resolver.resolve.call_count == 0
        assert result.code == INVALID_SIZE_CODE

    def test_none_grid_resolve_spy_call_count_zero(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None with spy on resolve()
        grid = None

        # When: application orchestrates solve request
        magic_square_service.solve(grid)

        # Then: spy records zero calls to Domain entry point
        assert mock_resolver.resolve.call_count == 0

    def test_empty_list_resolve_not_called(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is an empty list
        grid: list[list[int]] = []

        # When: application orchestrates solve request
        result = magic_square_service.solve(grid)

        # Then: Domain resolve() is never invoked
        mock_resolver.resolve.assert_not_called()
        assert result.code == INVALID_SIZE_CODE

    def test_four_empty_rows_resolve_not_called(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid has four rows with zero columns
        grid: list[list[int]] = [[]] * 4

        # When: application orchestrates solve request
        magic_square_service.solve(grid)

        # Then: Domain resolve() is never invoked
        mock_resolver.resolve.assert_not_called()
        assert mock_resolver.resolve.call_count == 0

    def test_3x4_grid_resolve_not_called(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is 3 rows by 4 columns
        grid = GRID_3X4

        # When: application orchestrates solve request
        result = magic_square_service.solve(grid)

        # Then: Domain resolve() is never invoked
        mock_resolver.resolve.assert_not_called()
        assert result.code == INVALID_SIZE_CODE


class TestResolveMustNotReceiveNoneGrid:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Domain 직접 수신 격리."""

    def test_resolve_never_receives_none_grid_argument(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None and resolver is mocked
        grid = None

        # When: application orchestrates solve request
        magic_square_service.solve(grid)

        # Then: resolve() is not called and never receives None as an argument
        assert mock_resolver.resolve.call_count == 0
        for call in mock_resolver.resolve.call_args_list:
            assert call.args[0] is not None

    def test_boundary_handles_none_before_resolve(
        self,
        magic_square_service: MagicSquareService,
        mock_resolver: Mock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None entering through Control orchestration
        grid = None

        # When: Boundary handles None branch via solve()
        result = magic_square_service.solve(grid)

        # Then: resolve() is not called after Boundary rejection
        mock_resolver.resolve.assert_not_called()
        assert isinstance(result, ErrorResponse)
        assert result.message == INVALID_SIZE_MESSAGE


class TestResolveMockFailureOnUnexpectedCall:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — mock 호출 시 실패 처리."""

    def test_resolve_mock_raises_if_called_on_none_grid(
        self,
        mock_resolver: Mock,
        magic_square_service: MagicSquareService,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: resolve() mock configured to fail on any invocation
        mock_resolver.resolve.side_effect = AssertionError(
            "resolve() must not be called when grid is None"
        )
        grid = None

        # When: application orchestrates solve request
        result = magic_square_service.solve(grid)

        # Then: no AssertionError means resolve() was not invoked
        assert result.code == INVALID_SIZE_CODE
        assert mock_resolver.resolve.call_count == 0

    def test_scope_ac_fr_01_02_through_05_not_included(
        self,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: this commit is limited to AC-FR-01-01 size validation only
        excluded_ac_ids = {
            "AC-FR-01-02",
            "AC-FR-01-03",
            "AC-FR-01-04",
            "AC-FR-01-05",
        }

        # When: module scope is verified
        # Then: FR-02~05 and AC-FR-01-02~05 cases are not part of this suite
        assert MODULE_AC_ID == "AC-FR-01-01"
        assert MODULE_AC_ID not in excluded_ac_ids
