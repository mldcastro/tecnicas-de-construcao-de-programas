from PyQt5.QtCore import QThread, pyqtSignal
import pygame.midi
import time
import random


class Audio(QThread):
    OITAVA=12
    nota_midi = {
    1: 69,  # Lá
    2: 71,  # Si
    3: 60,  # Dó
    4: 62,  # Ré
    5: 64,  # Mi
    6: 65,  # Fá
    7: 67   # Sol
    }
    char_to_midi = {
           'A': 69, 'a': 69,  # Nota Lá
           'B': 71, 'b': 71,  # Nota Si
           'C': 60, 'c': 60,  # Nota Dó
           'D': 62, 'd': 62,  # Nota Ré
           'E': 64, 'e': 64,  # Nota Mi
           'F': 65, 'f': 65,  # Nota Fá
           'G': 67, 'g': 67,  # Nota Sol
           ' ': None           # Silêncio ou pausa
        }
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
        
    def getNewNote(self):
        index=self.current_char_index
        if(self.sequence[index:(index+4)] == "BPM+"):
            return
        elif(self.sequence[index:(index+2)]=="R+"):
            self.current_note+=Audio.OITAVA
            return
        elif(self.sequence[index:(index+2)]=="R-"):
            self.current_note-=Audio.OITAVA
            return
        elif self.sequence[index] in Audio.char_to_midi:
            self.current_note_playing = Audio.char_to_midi[self.sequence[index]]
            return
        elif(self.sequence[index].upper()=='I' or self.sequence[index].upper()=='O'
        or self.sequence[index].upper()=='U'):
            if not ((self.sequence[index-1] in Audio.char_to_midi) and self.sequence[index-1]!=' '):
                self.current_note_playing=125
            return
        elif(self.sequence[index]=="?"):
            # Gerar número aleatório entre 1 e 7
            random_index = random.randint(1, 7)

            # Obter a nota MIDI correspondente
            nota = Audio.nota_midi[random_index]
            self.current_note_playing=nota
            return
    def getNewInstrument():
        """."""

    def getNewVelocity():
        """."""
            
    
        




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
                currentTime=start_time
                timeMax=2.0
                while (currentTime-start_time) < timeMax:
                    if not self.is_running:  # Interrompe execução
                        player.note_off(self.current_note_playing, 127)
                        return

                    if self.is_paused:  # Pausa execução
                        currentTime=time.time()
                        timeMax -= (currentTime - start_time)
                        player.note_off(self.current_note_playing, 127)  # Encerra a nota ao pausar
                        while self.is_paused:
                            if not self.is_running:
                                return
                            time.sleep(0.1)
                        # Ao retomar, inicia a nota novamente
                        start_time = time.time()
                        currentTime=start_time
                        player.note_on(self.current_note_playing, 127)
                    else:
                        currentTime=time.time()

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
