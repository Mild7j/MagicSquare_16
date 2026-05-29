"""AC-FR-01-01 invalid size verification tests for the Boundary layer."""

from __future__ import annotations

import pytest

from src.boundary.schemas import ErrorResponse
from src.boundary.validator import BoundaryValidator

from tests.boundary.constants import (
    GRID_3X4,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    MODULE_AC_ID,
)

pytestmark = pytest.mark.boundary


class TestInvalidSizeFailureReturn:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 정상 실패 반환."""

    def test_none_grid_returns_invalid_size_error(
        self,
        boundary_validator: BoundaryValidator,
        expected_invalid_size_error: ErrorResponse,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None (matrix absent)
        grid = None

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: failure response matches INVALID_SIZE contract
        assert result == expected_invalid_size_error

    def test_none_grid_returns_exact_invalid_size_code(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: code is exactly "INVALID_SIZE"
        assert result.code == INVALID_SIZE_CODE

    def test_none_grid_returns_error_response_type(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: return type is the specified failure result struct
        assert isinstance(result, ErrorResponse)


class TestInvalidSizeBoundaryValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 경계값."""

    def test_empty_list_returns_invalid_size_error(
        self,
        boundary_validator: BoundaryValidator,
        expected_invalid_size_error: ErrorResponse,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is an empty list (zero rows)
        grid: list[list[int]] = []

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: failure response matches INVALID_SIZE contract
        assert result == expected_invalid_size_error

    def test_four_empty_rows_returns_invalid_size_error(
        self,
        boundary_validator: BoundaryValidator,
        expected_invalid_size_error: ErrorResponse,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid has four rows with zero columns
        grid: list[list[int]] = [[]] * 4

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: failure response matches INVALID_SIZE contract
        assert result == expected_invalid_size_error

    def test_3x4_grid_returns_invalid_size_error(
        self,
        boundary_validator: BoundaryValidator,
        expected_invalid_size_error: ErrorResponse,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is 3 rows by 4 columns
        grid = GRID_3X4

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: failure response matches INVALID_SIZE contract
        assert result == expected_invalid_size_error

    @pytest.mark.parametrize(
        ("grid", "case_id"),
        [
            (None, "none"),
            ([], "empty_list"),
            ([[]] * 4, "four_empty_rows"),
            (GRID_3X4, "3x4"),
        ],
        ids=["none", "empty_list", "four_empty_rows", "3x4"],
    )
    def test_invalid_size_grids_return_invalid_size_code(
        self,
        boundary_validator: BoundaryValidator,
        grid: list[list[int]] | None,
        case_id: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is an invalid-size matrix (<case_id>)
        _ = case_id

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: code is exactly "INVALID_SIZE"
        assert result.code == INVALID_SIZE_CODE


class TestInvalidSizeMessageExactMatch:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 메시지 동일성."""

    def test_none_grid_message_exact_match(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid is None and PRD §8.1 message is fixed
        grid = None
        expected_message = "Grid must be 4x4."

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: message matches PRD §8.1 wording character-by-character
        assert result.message == expected_message
        assert len(result.message) == len(expected_message)
        assert list(result.message) == list(expected_message)

    @pytest.mark.parametrize(
        "grid",
        [None, [], [[]] * 4, GRID_3X4],
        ids=["none", "empty_list", "four_empty_rows", "3x4"],
    )
    def test_invalid_size_grids_message_exact_match(
        self,
        boundary_validator: BoundaryValidator,
        grid: list[list[int]] | None,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: grid violates 4x4 size contract
        expected_message = INVALID_SIZE_MESSAGE

        # When: Boundary validates input size
        result = boundary_validator.validate_size(grid)

        # Then: message is character-identical to PRD §8.1 wording
        assert result.message == expected_message


class TestInvalidSizeScopeLimit:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 범위 제한."""

    OUT_OF_SCOPE_AC_IDS: frozenset[str] = frozenset(
        {
            "AC-FR-01-02",
            "AC-FR-01-03",
            "AC-FR-01-04",
            "AC-FR-01-05",
            "FR-02",
            "FR-03",
            "FR-04",
            "FR-05",
        }
    )

    OUT_OF_SCOPE_ERROR_CODES: frozenset[str] = frozenset(
        {
            "INVALID_BLANK_COUNT",
            "ERR_INVALID_BLANK_COUNT",
            "OUT_OF_RANGE",
            "ERR_OUT_OF_RANGE",
            "DUPLICATE_NON_ZERO",
            "ERR_DUPLICATE_NON_ZERO",
            "ERR_UNSOLVABLE",
        }
    )

    def test_module_covers_only_ac_fr_01_01(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: this module is scoped to AC-FR-01-01 only
        # When: module AC identifier is inspected
        # Then: only AC-FR-01-01 is declared as in-scope
        assert MODULE_AC_ID == "AC-FR-01-01"
        assert "AC-FR-01-02" not in {MODULE_AC_ID}

    def test_invalid_size_cases_never_return_out_of_scope_error_codes(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: size-only invalid grids (AC-FR-01-02~05, FR-02~05 excluded)
        size_invalid_grids: list[list[list[int]] | None] = [
            None,
            [],
            [[]] * 4,
            GRID_3X4,
        ]

        for grid in size_invalid_grids:
            # When: Boundary validates input size
            result = boundary_validator.validate_size(grid)

            # Then: only INVALID_SIZE is returned, never out-of-scope codes
            assert result.code == INVALID_SIZE_CODE
            assert result.code not in self.OUT_OF_SCOPE_ERROR_CODES

    def test_out_of_scope_ac_ids_are_documented_as_excluded(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # AC-FR-01-01
        # Given: AC-FR-01-02~05 and FR-02~05 are explicitly out of scope
        # When: out-of-scope AC registry is read
        # Then: current AC-FR-01-01 is not listed among excluded IDs
        assert "AC-FR-01-01" not in self.OUT_OF_SCOPE_AC_IDS
        assert len(self.OUT_OF_SCOPE_AC_IDS) >= 4
