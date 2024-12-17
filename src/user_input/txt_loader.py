from pathlib import Path
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal


class TxtLoaderWidget(QtWidgets.QWidget):
    file_loaded = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)

        self._load_button = QtWidgets.QPushButton("Carregar .txt")
        self._load_button.setFixedWidth(80)
        self._load_button.clicked.connect(self._on_load_pressed)

        self._layout.addWidget(self._load_button)

        self._value = ""

    @property
    def value(self) -> str:
        return self._value

    def _on_load_pressed(self) -> None:
        file_path, extension = QtWidgets.QFileDialog.getOpenFileName(
            self,
            directory="./",
            filter="*.txt",
            options=QtWidgets.QFileDialog.Option.DontUseNativeDialog,
        )

        if len(file_path) == 0:
            self._value = ""
        else:
            file_path = Path(file_path).resolve()
            with open(file_path, "r") as file:
                value = file.read()
                self._value = value

        self.file_loaded.emit(self._value)
