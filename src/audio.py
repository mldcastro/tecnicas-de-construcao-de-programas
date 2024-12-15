import pygame.midi
import time
import random

from typing import Optional
from PyQt6.QtCore import QThread, pyqtSignal

from src.commands import Commands


class Audio(QThread):
    _DEFAULT_VOLUME = 50
    _DEFAULT_OCTAVE = 0
    _MAX_VOLUME = 127
    _MAX_OCTAVE = 48
    _MIN_OCTAVE = -48
    _DEFAULT_BPM = 80
    _MAX_BPM = 600
    _DEFAULT_INSTRUMENT = 0  # Grand Piano

    instrument_changed = pyqtSignal(int)

    def __init__(self, sequence: Optional[list[str]] = None) -> None:
        super().__init__()

        self._sequence = sequence
        self._processed_sequence = list()

        self._midi_player: Optional[pygame.midi.Output] = None

        self._current_instrument = self._DEFAULT_INSTRUMENT
        self._current_volume = self._DEFAULT_VOLUME
        self._current_octave = self._DEFAULT_OCTAVE
        self._current_bpm = self._DEFAULT_BPM
        self._note_duration_sec = _bpm_to_period(self._DEFAULT_BPM)

        self._previous_note: Optional[str] = None
        self._current_note: Optional[str] = None
        self._previous_instruction_index: Optional[int] = None
        self._current_instruction_index = 0

        self._should_play = False

    @property
    def current_instrument(self) -> int:
        return self._current_instrument

    @property
    def current_volume(self) -> int:
        return self._current_volume

    @property
    def current_octave(self) -> int:
        return self._current_octave

    @property
    def current_instruction(self) -> Optional[int]:
        if len(self._processed_sequence) == 0:
            return None
        return self._processed_sequence[self._current_instruction_index]

    @property
    def should_play(self) -> bool:
        return self._should_play

    def set_should_play(self, v: bool) -> None:
        self._should_play = v

    def set_instrument(self, instrument: int) -> None:
        self._current_instrument = instrument
        self._midi_player.set_instrument(self._current_instrument)
        self.instrument_changed.emit(self.current_instrument)

    def set_volume(self, volume: int) -> None:
        self._current_volume = min(max(volume, 0), self._MAX_VOLUME)

    def inc_volume(self, inc: int) -> None:
        self._current_volume = min(self._current_volume + inc, self._MAX_VOLUME)

    def dec_volume(self, dec: int) -> None:
        self._current_volume = max(self._current_volume - dec, 0)

    def set_octave(self, octave: int) -> None:
        self._current_octave = min(max(octave, 0), self._MAX_OCTAVE)

    def inc_octave(self, inc: int) -> None:
        self._current_octave = min(self._current_octave + inc, self._MAX_OCTAVE)

    def dec_octave(self, dec: int) -> None:
        self._current_octave = max(self._current_octave - dec, self._MIN_OCTAVE)

    def set_bpm(self, v: int) -> None:
        self._current_bpm = min(v, self._MAX_BPM)
        self._note_duration_sec = _bpm_to_period(self._current_bpm)

    def inc_bpm(self, inc: int) -> None:
        self._current_bpm = min(self._current_bpm + inc, self._MAX_BPM)
        self._note_duration_sec = _bpm_to_period(self._current_bpm)
        self._note_duration_sec = max(self._note_duration_sec, 0.1)

    def dec_bpm(self, dec: int) -> None:
        self._current_bpm = max(self._current_bpm - dec, 10)
        self._note_duration_sec = _bpm_to_period(self._current_bpm)
        self._note_duration_sec = min(self._note_duration_sec, 2)

    def run(self) -> None:
        pygame.midi.init()
        self._midi_player = pygame.midi.Output(0)
        self.set_instrument(self._DEFAULT_INSTRUMENT)

        sequence_len = len(self._processed_sequence)

        while True:
            while self._should_play and self._current_instruction_index < sequence_len:
                command = self._processed_sequence[self._current_instruction_index]

                if command in Commands.mandatory():
                    self._handle_mandatory_command(
                        command,
                        self._get_previous_command(),
                    )
                else:
                    self._run_config_command(command)

                self._previous_instruction_index = self._current_instruction_index
                self._current_instruction_index += 1

            if self._current_instruction_index == sequence_len:
                break

        self._midi_player.close()
        self._midi_player = None
        pygame.midi.quit()

    def play(self) -> None:
        self.start()

    def restart(self) -> None:
        if self._midi_player is not None:
            self.set_instrument(self._DEFAULT_INSTRUMENT)

        self.set_volume(self._DEFAULT_VOLUME)
        self.set_bpm(self._DEFAULT_BPM)
        self.set_octave(self._DEFAULT_OCTAVE)

        self._previous_note = None
        self._current_note = None
        self._previous_instruction_index = 0
        self._current_instruction_index = 0

        self._should_play = False

    def pause(self) -> None:
        self._should_play = False

    def set_sequence(self, audio_string: str) -> None:
        self.set_volume(self._DEFAULT_VOLUME)
        self.set_bpm(self._DEFAULT_BPM)

        self._previous_note = None
        self._current_note = None
        self._previous_instruction_index = None
        self._current_instruction_index = 0

        self._sequence = audio_string
        self._processed_sequence = list()
        self._build_audio()

    def _build_audio(self) -> None:
        length = len(self._sequence)
        max_length_command = max(len(i) for i in Commands)
        start = 0
        end = 0

        while start < length:
            end += max_length_command
            while end - start > 0:
                if self._sequence[start:end].lower() in list(Commands):
                    self._processed_sequence.append(self._sequence[start:end].lower())
                    break
                end -= 1

            if end == start:
                self._processed_sequence.append(self._sequence[start : end + 1].lower())

            start += max(end - start, 1)
            end += start + max_length_command

    def _get_previous_command(self) -> Optional[str]:
        if self._previous_instruction_index is not None:
            return self._processed_sequence[self._previous_instruction_index]

    def _handle_mandatory_command(
        self, command: str, prev_command: Optional[str]
    ) -> None:
        if self._midi_player is None:
            return None

        midi_id = self._map_command_char_to_midi(command)

        if midi_id is None:
            midi_id = self._current_note

            if prev_command not in Commands.notes():
                return self._make_telephone_ring()

        self._previous_note = self._current_note
        self._current_note = midi_id

        self._play_note(midi_id)

    def _map_command_char_to_midi(self, char: str) -> int:
        map_ = {
            Commands.NOTE_DO: 60,
            Commands.NOTE_RE: 62,
            Commands.NOTE_MI: 64,
            Commands.NOTE_FA: 65,
            Commands.NOTE_SOL: 67,
            Commands.NOTE_LA: 69,
            Commands.NOTE_SI: 71,
            Commands.RANDOM_NOTE: random.randint(0, 127),
        }

        return map_.get(char)

    def _make_telephone_ring(self) -> None:
        current_instrument = self.current_instrument

        LA_ID = self._map_command_char_to_midi(Commands.NOTE_LA)
        TELEPHONE_RING_ID = 124

        self.set_instrument(TELEPHONE_RING_ID)
        self._play_note(LA_ID)
        self.set_instrument(current_instrument)

    def _play_note(self, note: int) -> None:
        note = note + (self._current_octave)
        self._midi_player.note_on(note=note, velocity=self._current_volume)
        time.sleep(self._note_duration_sec)
        self._midi_player.note_off(note=note, velocity=self._current_volume)

    def _run_config_command(self, command: str) -> None:
        map_ = {
            Commands.INC_1_OCTAVE: lambda: self.inc_octave(12),
            Commands.DEC_1_OCTAVE: lambda: self.dec_octave(12),
            Commands.INC_BPM_80_UNITS: lambda: self.inc_bpm(80),
            Commands.DEC_BPM_80_UNITS: lambda: self.dec_bpm(80),
            Commands.RANDOM_BPM: lambda: self.set_bpm(random.randint(60, 240)),
            Commands.SILENCE: lambda: time.sleep(0.1),
            Commands.CHANGE_INSTRUMENT: lambda: self.set_instrument(
                random.randint(0, 127)
            ),
            Commands.DOUBLE_VOLUME: lambda: self.inc_volume(self._current_volume),
            Commands.RESET_VOLUME: lambda: self.set_volume(self._DEFAULT_VOLUME),
        }

        command_func = map_.get(command.lower(), lambda: None)
        command_func()


def _bpm_to_period(f: int) -> float:
    ONE_MINUTE_SEC = 60
    return 1 / (f / ONE_MINUTE_SEC)
