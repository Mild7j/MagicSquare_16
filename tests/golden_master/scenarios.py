"""Scenario definitions and result serialization for Golden Master tests."""

from __future__ import annotations

from dataclasses import dataclass

from src.boundary.schemas import ErrorResponse
from src.boundary.ui_boundary import UIBoundary

NORMAL_SUCCESS_GRID: list[list[int]] = [
    [16, 2, 0, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 0],
    [4, 14, 15, 1],
]

REVERSE_SUCCESS_GRID: list[list[int]] = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

INVALID_BLANK_COUNT_GRID: list[list[int]] = [
    [16, 2, 0, 13],
    [5, 0, 10, 8],
    [9, 7, 6, 0],
    [4, 14, 15, 1],
]

DUPLICATE_NUMBER_GRID: list[list[int]] = [
    [16, 2, 0, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 0],
    [4, 14, 15, 16],
]

NO_VALID_SOLUTION_GRID: list[list[int]] = [
    [10, 12, 8, 9],
    [2, 13, 15, 0],
    [0, 11, 3, 5],
    [16, 6, 7, 14],
]


@dataclass(frozen=True)
class GoldenScenario:
    """One Golden Master scenario with testcase id, section key, and input grid."""

    testcase_id: str
    section: str
    grid: list[list[int]]
    description: str


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(
        "GM-TC-01",
        "GM-TC-01",
        NORMAL_SUCCESS_GRID,
        "정상 조합 성공 (Attempt 1 small-first)",
    ),
    GoldenScenario(
        "GM-TC-02",
        "GM-TC-02",
        REVERSE_SUCCESS_GRID,
        "reverse 조합 성공 (Attempt 2 fallback)",
    ),
    GoldenScenario(
        "GM-TC-03",
        "GM-TC-03",
        INVALID_BLANK_COUNT_GRID,
        "INVALID_BLANK_COUNT",
    ),
    GoldenScenario(
        "GM-TC-04",
        "GM-TC-04",
        DUPLICATE_NUMBER_GRID,
        "DUPLICATE_NUMBER",
    ),
    GoldenScenario(
        "GM-TC-05",
        "GM-TC-05",
        NO_VALID_SOLUTION_GRID,
        "NO_VALID_MAGIC_SQUARE",
    ),
)

SECTION_SEPARATOR = "________________________________________"


def format_grid(grid: list[list[int]]) -> str:
    """Serialize a 4x4 grid as space-separated rows.

    Args:
        grid: Input matrix.

    Returns:
        Multiline string with one row per line.
    """
    return "\n".join(" ".join(str(value) for value in row) for row in grid)


def format_success_vector(values: list[int]) -> str:
    """Serialize a success vector in compact list form.

    Args:
        values: Six-element solver output.

    Returns:
        Compact list literal without spaces, e.g. ``[3,3,6,4,4,1]``.
    """
    return "[" + ",".join(str(value) for value in values) + "]"


def serialize_solve_result(result: ErrorResponse | list[int] | BaseException) -> str:
    """Serialize a solver outcome into Golden Master body text.

    Args:
        result: ``ErrorResponse``, success vector, or captured exception.

    Returns:
        ``Output:`` or ``Error:`` block body without section header.
    """
    if isinstance(result, ErrorResponse):
        return f"Error:\n{result.code}"
    if isinstance(result, list):
        return f"Output:\n{format_success_vector(result)}"
    if isinstance(result, BaseException):
        return f"Error:\n{type(result).__name__}"
    raise TypeError(f"Unsupported result type: {type(result)!r}")


def serialize_scenario(section: str, grid: list[list[int]], body: str) -> str:
    """Serialize one Golden Master scenario section.

    Args:
        section: Section key, e.g. ``GM-TC-01``.
        grid: Scenario input grid.
        body: ``Output:`` or ``Error:`` block from :func:`serialize_solve_result`.

    Returns:
        Full section text including header and input grid.
    """
    return (
        f"[{section}]\n"
        f"Input:\n"
        f"{format_grid(grid)}\n"
        f"{body}"
    )


def capture_solve_result(grid: list[list[int]]) -> ErrorResponse | list[int] | BaseException:
    """Execute ``UIBoundary.solve`` and capture structured API result.

    Args:
        grid: Input matrix for the scenario.

    Returns:
        Success vector, ``ErrorResponse``, or captured exception.
    """
    try:
        return UIBoundary().solve(grid)
    except BaseException as exc:
        return exc


def run_scenario(section: str, grid: list[list[int]]) -> str:
    """Execute ``UIBoundary.solve`` and serialize the observed outcome.

    Args:
        section: Scenario section key (for traceability only).
        grid: Input matrix for the scenario.

    Returns:
        Full serialized scenario section.
    """
    outcome = capture_solve_result(grid)
    body = serialize_solve_result(outcome)
    return serialize_scenario(section, grid, body)


def build_golden_master_document() -> str:
    """Build the full Golden Master baseline from all registered scenarios.

    Returns:
        Concatenated scenario sections separated by blank lines.
    """
    sections = [run_scenario(scenario.section, scenario.grid) for scenario in GOLDEN_SCENARIOS]
    return "\n\n".join(sections) + "\n"
