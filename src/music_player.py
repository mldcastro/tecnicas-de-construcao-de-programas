from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from .user_input import UserInputWidget
from .command_list import CommandListBox
from .audio import Audio
from .control_board import ControlBoard
from .midi import MidiInstrumentBox
from .midi_file_processor import MidiFileProcessor


class MusicPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout(self)

        self._command_list_box = CommandListBox()

        self._user_input_widget = UserInputWidget()
        self._user_input_widget.value_changed.connect(self._feed_string)

        self._audio_manager = Audio()
        self._audio_manager.finished.connect(self._on_music_ended)

        self._midi_processor = MidiFileProcessor()

        self._midi_instrument_box = MidiInstrumentBox()
        self._audio_manager.instrument_changed.connect(
            self._midi_instrument_box.set_instrument
        )

        self._control_board_widget = ControlBoard()
        self._control_board_widget.play.connect(self._on_play_clicked)
        self._control_board_widget.play.connect(self._audio_manager.start)
        self._control_board_widget.pause.connect(self._audio_manager.pause)
        self._control_board_widget.pause.connect(self._user_input_widget.unblock)

        self._control_board_widget.restart.connect(self._audio_manager.restart)

        self._control_board_widget.save.connect(self._save)
        self._user_input_widget.value_changed.connect(
            self._control_board_widget.unblock_save_button
        )

        self._layout.addWidget(self._user_input_widget, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(self._command_list_box, 1, 0, 1, 2)
        self._layout.addWidget(
            self._control_board_widget, 0, 1, Qt.AlignmentFlag.AlignCenter
        )
        self._layout.addWidget(self._midi_instrument_box, 0, 1, Qt.AlignmentFlag.AlignTop)

        self._command_list_box.display()

    def _feed_string(self) -> None:
        self._audio_manager.set_sequence(self._user_input_widget.value)
        self._midi_processor.convert_user_input_to_midi(
            self._user_input_widget.value, self
        )

    def _on_play_clicked(self) -> None:
        self._user_input_widget.block()
        self._audio_manager.set_should_play(True)
        self._audio_manager.play()

    def _on_music_ended(self) -> None:
        self._control_board_widget.to_play_state()
        self._audio_manager.restart()

    def _save(self) -> None:
        self._midi_processor._save_midi_file(self)
