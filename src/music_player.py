from PyQt6 import QtWidgets

from .user_input import UserInputArea


class MusicPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout(self)

        self._user_input_box = UserInputArea()

        self._layout.addWidget(self._user_input_box, 0, 0)
