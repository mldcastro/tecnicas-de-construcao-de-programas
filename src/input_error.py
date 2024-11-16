from typing import Optional
from PyQt6 import QtWidgets


class InputErrorBox(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)

        self._error_label = QtWidgets.QLabel()
        self._error_label.setStyleSheet("color: red;")

        self._layout.addWidget(self._error_label)

        self._value: Optional[str] = None

    @property
    def value(self) -> Optional[str]:
        return self._value

    def set_text(self, text: str) -> None:
        self._value = text
        self._error_label.setText(self._value)

    def display(self) -> None:
        self.show()

    def hide(self) -> None:
        self._value = None
        self._error_label.clear()


class InputException(Exception):
    pass
