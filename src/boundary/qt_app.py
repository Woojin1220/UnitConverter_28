"""PyQt GUI boundary — formatting only; logic via control (cli.process)."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from boundary.cli import process
from control.converter import supported_units

MIN_WIDTH = 460
MIN_HEIGHT = 380
ERROR_COLOR = "#c0392b"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        intro = QLabel(
            "값과 단위를 선택한 뒤 변환하면, 입력 단위를 제외한 모든 단위로 변환합니다."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("값"))
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("예: 2.5")
        self.value_input.returnPressed.connect(self.convert)
        input_row.addWidget(self.value_input, stretch=2)

        input_row.addWidget(QLabel("단위"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(supported_units())
        input_row.addWidget(self.unit_combo, stretch=1)
        layout.addLayout(input_row)

        button_row = QHBoxLayout()
        self.convert_button = QPushButton("변환")
        self.convert_button.clicked.connect(self.convert)
        button_row.addWidget(self.convert_button)

        clear_button = QPushButton("지우기")
        clear_button.clicked.connect(self.clear)
        button_row.addWidget(clear_button)
        button_row.addStretch()
        layout.addLayout(button_row)

        layout.addWidget(QLabel("결과"))
        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)
        self.result_view.setPlaceholderText("변환 결과가 여기에 표시됩니다.")
        layout.addWidget(self.result_view)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {ERROR_COLOR};")
        layout.addWidget(self.status_label)

    def clear(self) -> None:
        self.value_input.clear()
        self.result_view.clear()
        self.status_label.clear()
        self.value_input.setFocus()

    def convert(self) -> None:
        self.status_label.clear()
        self.result_view.clear()

        raw_value = self.value_input.text().strip()
        if not raw_value:
            self.status_label.setText("값을 입력하세요.")
            return

        unit = self.unit_combo.currentText()
        raw = f"{unit}:{raw_value}"
        result = process(raw, format_numbers=True)

        if not result.ok:
            self.status_label.setText(result.lines[0])
            return

        self.result_view.setPlainText("\n".join(result.lines))

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Unit Converter")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
