from typing import Optional
from PyQt6 import QtWidgets

from .input_error import InputException, InputErrorBox


class UserInputWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._layout = QtWidgets.QGridLayout()
        self.setLayout(self._layout)

        self._input = QtWidgets.QTextEdit()
        self._input.setFixedHeight(50)
        self._input.setFixedWidth(300)
        self._input.setPlaceholderText("Type here")

        self._ok_button = QtWidgets.QPushButton("OK")
        self._ok_button.setFixedWidth(50)
        self._ok_button.clicked.connect(self._on_ok_pressed)

        self._error_box = InputErrorBox()
        self._error_box.hide()

        self._layout.addWidget(self._input)
        self._layout.addWidget(self._ok_button)
        self._layout.addWidget(self._error_box)

        self._value: Optional[str] = None
        self._is_valid: Optional[bool] = None
        self._is_blocked = False

    @property
    def value(self) -> Optional[str]:
        return self._value

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    @property
    def is_valid(self) -> Optional[bool]:
        return self._is_valid

    def block(self) -> None:
        self._input.setDisabled(True)
        self._ok_button.setDisabled(True)
        self._is_blocked = True

    def unblock(self) -> None:
        self._input.setDisabled(False)
        self._ok_button.setDisabled(False)
        self._is_blocked = False

    def _validate_input(self, input_str: str) -> None:
        if not input_str:
            raise InputException("Invalid input")

    def _show_error(self, e: InputException) -> None:
        self._error_box.set_text(str(e))
        self._error_box.display()

    def _on_ok_pressed(self) -> None:
        try:
            self._validate_input(self._input.toPlainText())
            self._value = self._input.toPlainText()
            self._is_valid = True
            self._error_box.hide()

        except InputException as e:
            self._value = None
            self._is_valid = False
            self._show_error(e)
