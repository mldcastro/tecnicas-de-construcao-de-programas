import mido
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import random
from src.commands import Commands


class MidiFileProcessor:
    _DEFAULT_VOLUME = 50
    _DEFAULT_OCTAVE = 0
    _MAX_VOLUME = 127
    _MAX_OCTAVE = 48
    _MIN_OCTAVE = -48
    _DEFAULT_BPM = 80
    _MAX_BPM = 600
    _DEFAULT_INSTRUMENT = 0  # Grand Piano

    def __init__(self):
        self.midi_file = mido.MidiFile()
        self.ticks_per_beat = self.midi_file.ticks_per_beat

        self.track = mido.MidiTrack()
        self.midi_file.tracks.append(self.track)

        self.bpm = self._DEFAULT_BPM
        self.octave = self._DEFAULT_OCTAVE
        self.instrument = self._DEFAULT_INSTRUMENT
        self.note_duration = self.ticks_per_beat
        self.volume = self._DEFAULT_VOLUME

    def convert_user_input_to_midi(self, user_input: str, parent_widget=None):
        if not user_input:
            QMessageBox.warning(
                parent_widget,
                "Erro de Entrada",
                "Nenhuma entrada fornecida para a conversão em MIDI.",
            )
            return

        user_input = user_input.lower()

        microseconds_per_beat = mido.bpm2tempo(self.bpm)
        self.track.append(mido.MetaMessage("set_tempo", tempo=microseconds_per_beat))

        char_to_midi = self._get_note_mapping()

        i = 0
        while i < len(user_input):
            char = user_input[i]
            if user_input.startswith(Commands.INC_BPM_80_UNITS.value.lower(), i):
                self.bpm = self._adjust_bpm(user_input, i, self.bpm)
                microseconds_per_beat = mido.bpm2tempo(self.bpm)
                self.track.append(
                    mido.MetaMessage("set_tempo", tempo=microseconds_per_beat)
                )
                i += len(Commands.INC_BPM_80_UNITS.value)
            elif user_input.startswith(Commands.DEC_BPM_80_UNITS.value.lower(), i):
                self.bpm = self._adjust_bpm(user_input, i, self.bpm, increase=False)
                microseconds_per_beat = mido.bpm2tempo(self.bpm)
                self.track.append(
                    mido.MetaMessage("set_tempo", tempo=microseconds_per_beat)
                )
                i += len(Commands.DEC_BPM_80_UNITS.value)
            elif char in Commands.notes():
                self._process_note(char_to_midi, char)
                i += 1
            elif char == Commands.SILENCE.value:
                self._process_pause()
                i += 1
            elif char == Commands.DOUBLE_VOLUME.value:
                self.volume = min(127, self.volume + self.volume)
                i += 1
            elif char == Commands.RESET_VOLUME.value:
                self.volume = self._DEFAULT_VOLUME
                i += 1
            elif char in Commands.repeat_commands():
                self._process_instrument_change(user_input, i, char_to_midi)
                i += 1
            elif user_input.startswith(Commands.INC_1_OCTAVE.value, i):
                self.octave = min(self._MAX_OCTAVE, self.octave + 12)
                i += len(Commands.INC_1_OCTAVE.value)
            elif user_input.startswith(Commands.DEC_1_OCTAVE.value, i):
                self.octave = max(self._MIN_OCTAVE, self.octave - 12)
                i += len(Commands.DEC_1_OCTAVE.value)
            elif char == Commands.RANDOM_NOTE.value:
                self._process_random_note()
                i += 1
            elif char == Commands.CHANGE_INSTRUMENT.value:
                self._process_new_line()
                i += 1
            elif char == Commands.RANDOM_BPM.value:
                self.bpm = random.randint(40, 200)
                microseconds_per_beat = mido.bpm2tempo(self.bpm)
                self.track.append(
                    mido.MetaMessage("set_tempo", tempo=microseconds_per_beat)
                )
                i += 1
            else:
                i += 1  # Ignora caracteres inválidos

    def _get_note_mapping(self):
        return {
            Commands.NOTE_LA.value: 69,
            Commands.NOTE_SI.value: 71,
            Commands.NOTE_DO.value: 60,
            Commands.NOTE_RE.value: 62,
            Commands.NOTE_MI.value: 64,
            Commands.NOTE_FA.value: 65,
            Commands.NOTE_SOL.value: 67,
        }

    def _adjust_bpm(self, user_input, index, bpm, increase=True):
        adjustment = (
            int(user_input[index + 4 :]) if user_input[index + 4 :].isdigit() else 80
        )
        new_bpm = bpm + adjustment if increase else bpm - adjustment
        if new_bpm <= 0 or new_bpm > self._MAX_BPM:
            return bpm
        else:
            return new_bpm

    def _process_note(self, char_to_midi, char):
        note = char_to_midi[char] + self.octave
        self.track.append(
            mido.Message("note_on", note=note, velocity=self.volume, time=0)
        )
        self.track.append(
            mido.Message(
                "note_off", note=note, velocity=self.volume, time=self.note_duration
            )
        )

    def _process_pause(self):
        self.track.append(
            mido.Message("note_on", note=0, velocity=0, time=self.note_duration)
        )
        self.track.append(
            mido.Message(
                "note_off", note=0, velocity=self.volume, time=self.note_duration
            )
        )

    def _process_instrument_change(self, user_input, index, char_to_midi):
        if user_input[index - 1] in char_to_midi:
            note = char_to_midi[user_input[index - 1]] + self.octave
            self.track.append(
                mido.Message("note_on", note=note, velocity=self.volume, time=0)
            )
            self.track.append(
                mido.Message(
                    "note_off", note=note, velocity=self.volume, time=self.note_duration
                )
            )
        else:
            self.track.append(mido.Message("program_change", program=124, time=0))
            random_note = random.choice([char_to_midi[ch] for ch in char_to_midi])
            self.track.append(
                mido.Message("note_on", note=random_note, velocity=self.volume, time=0)
            )
            self.track.append(
                mido.Message(
                    "note_off",
                    note=random_note,
                    velocity=self.volume,
                    time=self.note_duration,
                )
            )
        self.track.append(mido.Message("program_change", program=0, time=0))

    def _process_random_note(self):
        random_note = random.choice([note for note in range(21, 109)])
        self.track.append(
            mido.Message("note_on", note=random_note, velocity=self.volume, time=0)
        )
        self.track.append(
            mido.Message(
                "note_off",
                note=random_note,
                velocity=self.volume,
                time=self.note_duration,
            )
        )

    def _process_new_line(self):
        self.instrument = random.randint(0, 127)
        self.track.append(mido.Message("program_change", program=self.instrument, time=0))

    def _save_midi_file(self, parent_widget):
        file_name, _ = QFileDialog.getSaveFileName(
            parent_widget, "Salvar Arquivo MIDI", "", "MIDI Files (*.mid)"
        )
        if file_name:
            self.midi_file.save(file_name)
            QMessageBox.information(
                parent_widget, "Salvo", f"Arquivo MIDI salvo em: {file_name}"
            )
