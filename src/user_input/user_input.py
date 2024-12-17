from typing import Optional
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal

from .input_error import InputException, InputErrorBox
from .input_validator import InputValidator
from .txt_loader import TxtLoaderWidget


class UserInputWidget(QtWidgets.QWidget):
    value_changed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self._layout = QtWidgets.QGridLayout()
        self.setLayout(self._layout)

        self._input = QtWidgets.QTextEdit()
        self._input.setFixedHeight(100)
        self._input.setFixedWidth(400)
        self._input.setPlaceholderText("Digite aqui")

        self._ok_button = QtWidgets.QPushButton("OK")
        self._ok_button.setFixedWidth(70)
        self._ok_button.clicked.connect(self._on_ok_pressed)

        self._txt_loader = TxtLoaderWidget()
        self._txt_loader.file_loaded.connect(self._on_file_loaded)

        self._error_box = InputErrorBox()
        self._error_box.hide()

        self._layout.addWidget(self._input)
        self._layout.addWidget(self._ok_button, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(self._txt_loader, 1, 0, Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._error_box, 2, 0)

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
        self._txt_loader.setDisabled(True)
        self._is_blocked = True

    def unblock(self) -> None:
        self._input.setDisabled(False)
        self._ok_button.setDisabled(False)
        self._txt_loader.setDisabled(False)
        self._is_blocked = False

    def _validate_input(self) -> None:
        InputValidator.validate(self._input.toPlainText())

    def _show_error(self, e: InputException) -> None:
        self._error_box.set_text(str(e))
        self._error_box.display()

    def _on_ok_pressed(self) -> None:
        try:
            self._validate_input()
            self._value = self._input.toPlainText()
            self._is_valid = True
            self._error_box.hide()

            self.value_changed.emit(self._value)

        except InputException as e:
            self._value = None
            self._is_valid = False
            self._show_error(e)

    def _on_file_loaded(self) -> None:
        self._input.setText(self._txt_loader.value)
        self._error_box.hide()
