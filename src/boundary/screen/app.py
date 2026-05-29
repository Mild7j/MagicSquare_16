"""PyQt main window for Magic Square 4x4 manual verification."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.boundary.schemas import ErrorResponse
from src.boundary.screen.grids import GRID_G1
from src.boundary.ui_boundary import UIBoundary
from src.control.solve_partial_magic_square import SolvePartialMagicSquare
from src.entity.value_objects.grid_size import GRID_SIZE
from src.entity.value_objects.magic_constant import BLANK_VALUE, MAX_CELL_VALUE


def _create_spinbox(initial: int) -> QSpinBox:
    """Create a grid cell spin box constrained to 0..16.

    Args:
        initial: Initial cell value.

    Returns:
        Configured QSpinBox instance.
    """
    spinbox = QSpinBox()
    spinbox.setMinimum(BLANK_VALUE)
    spinbox.setMaximum(MAX_CELL_VALUE)
    spinbox.setValue(initial)
    return spinbox


class MagicSquareMainWindow(QMainWindow):
    """Main window with 4x4 grid input and solve action."""

    def __init__(self, ui_boundary: UIBoundary) -> None:
        """Initialize the main window.

        Args:
            ui_boundary: Boundary facade wired at the composition root.
        """
        super().__init__()
        self._ui_boundary = ui_boundary
        self.setWindowTitle("Magic Square 4x4")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        grid_layout = QGridLayout()
        self._spinboxes: list[list[QSpinBox]] = []
        for row_index in range(GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col_index in range(GRID_SIZE):
                spinbox = _create_spinbox(GRID_G1[row_index][col_index])
                grid_layout.addWidget(spinbox, row_index, col_index)
                row_boxes.append(spinbox)
            self._spinboxes.append(row_boxes)
        layout.addLayout(grid_layout)

        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        layout.addWidget(solve_button)

        self._result_label = QLabel("")
        layout.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        """Read current spin box values as a 4x4 matrix.

        Returns:
            Grid values row-major.
        """
        return [
            [spinbox.value() for spinbox in row]
            for row in self._spinboxes
        ]

    def _on_solve_clicked(self) -> None:
        """Invoke UIBoundary.solve and render success or failure text."""
        grid = self._read_grid()
        result = self._ui_boundary.solve(grid)

        if isinstance(result, ErrorResponse):
            self._result_label.setText(f"오류: {result.message}")
            return

        r1, c1, n1, r2, c2, n2 = result
        self._result_label.setText(
            f"결과 (r1, c1, n1, r2, c2, n2): {r1}, {c1}, {n1}, {r2}, {c2}, {n2}"
        )


class VerifyNoneWindow(QMainWindow):
    """Diagnostic window for grid=None rejection (--verify)."""

    def __init__(self, ui_boundary: UIBoundary) -> None:
        """Initialize the verify-only window.

        Args:
            ui_boundary: Boundary facade wired at the composition root.
        """
        super().__init__()
        self.setWindowTitle("Magic Square 4x4 — Verify grid=None")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        result_label = QLabel("")
        layout.addWidget(result_label)

        result = ui_boundary.solve(None)
        if isinstance(result, ErrorResponse):
            result_label.setText(f"오류: {result.message}")
        else:
            result_label.setText(f"Unexpected success: {result}")


def build_ui_boundary() -> UIBoundary:
    """Construct UIBoundary with injected Control resolver.

    Returns:
        Composition-root UIBoundary instance.
    """
    return UIBoundary(solver=SolvePartialMagicSquare())


def run_app(*, verify: bool = False) -> int:
    """Launch the PyQt application.

    Args:
        verify: When True, open grid=None diagnostic window only.

    Returns:
        Process exit code from QApplication.exec().
    """
    app = QApplication(sys.argv)
    ui_boundary = build_ui_boundary()

    if verify:
        window: QMainWindow = VerifyNoneWindow(ui_boundary)
    else:
        window = MagicSquareMainWindow(ui_boundary)

    window.show()
    return app.exec()


def main() -> None:
    """CLI entry point for ``python -m boundary.screen.app``."""
    verify = "--verify" in sys.argv
    raise SystemExit(run_app(verify=verify))
