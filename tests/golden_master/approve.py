"""Approve-pattern loader and comparator for Golden Master baseline files."""

from __future__ import annotations

import difflib
import re
from pathlib import Path

from tests.golden_master.scenarios import (
    GOLDEN_SCENARIOS,
    SECTION_SEPARATOR,
    build_golden_master_document,
    run_scenario,
)

DEFAULT_GOLDEN_MASTER_PATH = Path(__file__).resolve().parent.parent / "golden_master_expected.txt"
_SECTION_HEADER = re.compile(r"^\[(?P<section>[A-Za-z0-9_-]+)\]\s*$", re.MULTILINE)


def golden_master_path(path: Path | None = None) -> Path:
    """Return the canonical Golden Master baseline file path.

    Args:
        path: Optional override for tests or scripts.

    Returns:
        Path to ``tests/golden_master_expected.txt``.
    """
    return path or DEFAULT_GOLDEN_MASTER_PATH


def parse_golden_master_document(text: str) -> dict[str, str]:
    """Parse a Golden Master document into section-keyed scenario bodies.

    Args:
        text: Full baseline file contents.

    Returns:
        Mapping of section name to serialized scenario text (without outer separators).
    """
    matches = list(_SECTION_HEADER.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        section = match.group("section")
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[section] = text[start:end].rstrip()
    return sections


def format_golden_master_diff(expected: str, actual: str) -> str:
    """Format a unified diff for Golden Master failures.

    Args:
        expected: Baseline section or document text.
        actual: Live solver serialization.

    Returns:
        Unified diff prefixed with ``--- expected`` / ``+++ actual`` blocks.
    """
    diff_lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    return "".join(diff_lines) + SECTION_SEPARATOR + "\n"


def write_golden_master(path: Path | None = None) -> Path:
    """Generate and persist the Golden Master baseline from current solver output.

    Args:
        path: Optional output path override.

    Returns:
        Path to the written baseline file.
    """
    target = golden_master_path(path)
    actual_document = build_golden_master_document()
    approve_golden_master(
        actual_document,
        target,
        auto_create=True,
        force_update=True,
    )
    return target


def approve_golden_master(
    actual: str,
    path: Path | None = None,
    *,
    auto_create: bool = True,
    force_update: bool = False,
    mismatch_hint: str = "Re-run without --check to update baseline.",
) -> str:
    """Compare or update a Golden Master baseline file.

    Args:
        actual: Live solver serialization to compare or persist.
        path: Target baseline path; defaults to ``tests/golden_master_expected.txt``.
        auto_create: When True, create the baseline if it does not exist.
        force_update: When True, overwrite the baseline even when content differs.
        mismatch_hint: Guidance appended when comparison fails.

    Returns:
        ``"ok"`` when content matches, ``"created"`` on first write,
        or ``"updated"`` after a forced refresh.

    Raises:
        FileNotFoundError: When the baseline is missing and ``auto_create`` is False.
        AssertionError: When content differs and ``force_update`` is False.
    """
    target = golden_master_path(path)

    if not target.exists():
        if not auto_create:
            raise FileNotFoundError(
                f"Golden master baseline not found: {target}. "
                "Run without --check to generate it."
            )
        target.write_text(actual, encoding="utf-8")
        return "created"

    expected = target.read_text(encoding="utf-8")
    if actual == expected:
        return "ok"

    if force_update:
        target.write_text(actual, encoding="utf-8")
        return "updated"

    diff_text = format_golden_master_diff(expected, actual)
    raise AssertionError(f"Golden Master mismatch. {mismatch_hint}\n{diff_text}")


def read_expected_section(section: str, path: Path | None = None) -> str:
    """Read one scenario section from the baseline file.

    Args:
        section: Section key such as ``GM-TC-01``.
        path: Optional baseline path override.

    Returns:
        Serialized section text including ``[section]`` header.

    Raises:
        FileNotFoundError: When the baseline file does not exist.
        KeyError: When the section is missing from the baseline.
    """
    target = golden_master_path(path)
    document = target.read_text(encoding="utf-8")
    sections = parse_golden_master_document(document)
    if section not in sections:
        raise KeyError(f"Missing section [{section}] in {target}")
    return sections[section]


def assert_golden_master_matches(
    path: Path | None = None,
    *,
    approve: bool = False,
) -> None:
    """Compare actual solver output against the Golden Master baseline.

    When ``approve`` is True or the baseline file is missing, the current output
    is written to disk and the assertion passes.

    Args:
        path: Optional baseline path override.
        approve: When True, overwrite the baseline with current output.

    Raises:
        AssertionError: When actual and expected differ and ``approve`` is False.
    """
    target = golden_master_path(path)
    actual_document = build_golden_master_document()
    approve_golden_master(
        actual_document,
        target,
        auto_create=True,
        force_update=approve,
        mismatch_hint="Re-run with GOLDEN_MASTER_APPROVE=1 to update baseline.",
    )


def assert_scenario_matches(
    section: str,
    *,
    approve: bool = False,
    path: Path | None = None,
) -> str:
    """Compare one scenario section against the stored baseline.

    Args:
        section: Scenario section key.
        approve: When True, rewrite the full baseline from current solver output.
        path: Optional baseline path override.

    Returns:
        The approved or matched expected section text.

    Raises:
        AssertionError: When the scenario body differs and ``approve`` is False.
        KeyError: When the section is unknown in scenario registry.
    """
    scenario = next(item for item in GOLDEN_SCENARIOS if item.section == section)
    actual_section = run_scenario(scenario.section, scenario.grid)

    if approve:
        write_golden_master(path)
        return actual_section

    target = golden_master_path(path)
    if not target.exists():
        write_golden_master(path)
        return actual_section

    expected_document = target.read_text(encoding="utf-8")
    expected_sections = parse_golden_master_document(expected_document)
    expected_section = expected_sections.get(section)
    if expected_section is None:
        raise AssertionError(f"Missing section [{section}] in {target}")

    if actual_section == expected_section:
        return expected_section

    diff_text = format_golden_master_diff(expected_section, actual_section)
    raise AssertionError(
        f"Golden Master mismatch for [{section}]. "
        "Re-run with GOLDEN_MASTER_APPROVE=1 to update baseline.\n"
        f"{diff_text}"
    )
