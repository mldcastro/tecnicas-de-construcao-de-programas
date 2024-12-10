from PyQt5.QtCore import QThread, pyqtSignal
import pygame.midi
import time


class AudioPlayer(QThread):
    finished = pyqtSignal()  # Emitido ao final da execução
    current_note = pyqtSignal(int, int)  # Emite a nota e o instrumento atuais

    def __init__(self, sequence=""):
        super().__init__()
        self.sequence = sequence  # Sequência de caracteres fornecida pelo usuário
        self.current_char_index = 0
        self.current_note_playing = None
        self.current_instrument_playing = None
        self.remaining_time = 0.0  # Tempo restante da nota atual
        self.NOTE_DURATION = 2.0  # Duração total de cada nota (2 segundos)
        self.is_paused = False
        self.is_running = True

    def run(self):
        pygame.midi.init()
        try:
            player = pygame.midi.Output(0)  # Inicializa saída MIDI

            while self.is_running and self.current_char_index < len(self.sequence):
                if self.current_note_playing is None:  # Configura nova nota
                    char = self.sequence[self.current_char_index]

                    # Define nota e instrumento com base no caractere
                    if 'A' <= char <= 'H':
                        note, instrument = 60, 110
                    elif 'I' <= char <= 'P':
                        note, instrument = 50, 100
                    elif 'Q' <= char <= 'Z':
                        note, instrument = 40, 90
                    else:
                        continue  # Ignora caracteres fora do intervalo

                    self.current_note_playing = note
                    self.current_instrument_playing = instrument
                    self.remaining_time = self.NOTE_DURATION

                player.set_instrument(self.current_instrument_playing)
                self.current_note.emit(self.current_instrument_playing, self.current_note_playing)

                # Toca ou retoma a nota
                player.note_on(self.current_note_playing, 127)

                start_time = time.time()

                while self.remaining_time > 0:
                    if not self.is_running:  # Interrompe execução
                        player.note_off(self.current_note_playing, 127)
                        return

                    if self.is_paused:  # Pausa execução
                        self.remaining_time -= time.time() - start_time
                        player.note_off(self.current_note_playing, 127)  # Encerra a nota ao pausar
                        while self.is_paused:
                            if not self.is_running:
                                return
                            time.sleep(0.1)
                        # Ao retomar, inicia a nota novamente
                        start_time = time.time()
                        player.note_on(self.current_note_playing, 127)

                    elapsed_time = time.time() - start_time
                    if elapsed_time >= self.remaining_time:
                        self.remaining_time = 0
                    else:
                        self.remaining_time -= elapsed_time
                        start_time = time.time()  # Atualiza o início do tempo para a próxima iteração

                # Encerra a nota ao final do tempo
                player.note_off(self.current_note_playing, 127)
                self.current_note_playing = None  # Reseta nota atual
                self.current_char_index += 1  # Avança para a próxima nota

        finally:
            pygame.midi.quit()
            self.finished.emit()

    def pause(self):
        """Pausa a execução."""
        self.is_paused = True

    def resume(self):
        """Retoma a execução."""
        self.is_paused = False

    def stop(self):
        """Interrompe a execução."""
        self.is_running = False
        self.is_paused = False
        self.quit()
        self.wait()
