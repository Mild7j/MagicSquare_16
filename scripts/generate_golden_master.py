#!/usr/bin/env python3
"""Generate or refresh ``tests/golden_master_expected.txt`` from live solver output.

Usage:
    python scripts/generate_golden_master.py
    python scripts/generate_golden_master.py --check   # compare only, exit 1 on diff
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master.approve import (  # noqa: E402
    approve_golden_master,
    golden_master_path,
)
from tests.golden_master.scenarios import build_golden_master_document  # noqa: E402


def main() -> int:
    """Capture solver output and write or verify the golden master baseline.

    Returns:
        Process exit code (0 on success, 1 on check failure).
    """
    parser = argparse.ArgumentParser(
        description="Generate Magic Square Golden Master baseline (GM-1).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=golden_master_path(),
        help="Target baseline file path.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare only; exit 1 when baseline differs (no write).",
    )
    args = parser.parse_args()

    actual = build_golden_master_document()

    if args.check:
        try:
            status = approve_golden_master(
                actual,
                args.output,
                auto_create=False,
                force_update=False,
            )
        except (AssertionError, FileNotFoundError) as exc:
            print(exc, file=sys.stderr)
            return 1
        print(f"Golden master OK ({status}): {args.output}")
        return 0

    status = approve_golden_master(
        actual,
        args.output,
        auto_create=True,
        force_update=True,
    )
    print(f"Golden master {status}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
