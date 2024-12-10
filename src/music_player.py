from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from .user_input import UserInputWidget
from .command_list import CommandListBox
from .audio import Audio
from .control_board import ControlBoard


class MusicPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout(self)

        self._command_list_box = CommandListBox()

        self._user_input_widget = UserInputWidget()
        self._user_input_widget.value_changed.connect(self._feed_string_to_audio_manager)

        self._audio_manager = Audio()
        self._audio_manager.finished.connect(self._on_music_ended)

        self._control_board_widget = ControlBoard()

        self._control_board_widget.play.connect(self._user_input_widget.block)
        self._control_board_widget.play.connect(self._on_play_clicked)

        self._control_board_widget.pause.connect(self._audio_manager.pause)
        self._control_board_widget.pause.connect(self._user_input_widget.unblock)

        self._control_board_widget.restart.connect(self._audio_manager.restart)

        self._layout.addWidget(self._user_input_widget, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(self._command_list_box, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(
            self._control_board_widget, 0, 1, Qt.AlignmentFlag.AlignCenter
        )

        self._command_list_box.display()

    def _feed_string_to_audio_manager(self) -> None:
        self._audio_manager.set_sequence(self._user_input_widget.value)

    def _on_play_clicked(self) -> None:
        self._audio_manager.set_should_play(True)
        self._audio_manager.play()

    def _on_music_ended(self) -> None:
        self._control_board_widget.to_play_state()
        self._audio_manager.restart()
