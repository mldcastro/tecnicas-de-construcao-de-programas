from PyQt6 import QtWidgets

from .user_input import UserInputWidget
from .command_list import CommandListBox


class MusicPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout(self)

        self._user_input_widget = UserInputWidget()
        self._command_list_box = CommandListBox()

        self._layout.addWidget(self._user_input_widget, 0, 0)
        self._layout.addWidget(self._command_list_box, 1, 0)

        self._command_list_box.display()
