from PyQt6.QtCore import QThread, pyqtSignal
import pygame.midi
import time
import random


class Audio(QThread):
    VOLUME_DEFAULT=30
    NOTE_DEFAULT=69
    VELOCITY_DEFAULT=60  #em BPM
    INSTRUMENT_DEFAULT=27  #Guitarra Elétrica (Clean)
    OITAVA=12
    VOLUME_MAX=127
    instrumentos = {
    1: 0,  # Piano acústico
    2: 27,  # Guitarra Elétrica (Clean)
    3: 40,  # Violino
    4: 73,  # Flauta
    5: 65,  # Saxofone
    }
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
           
        }
    finished = pyqtSignal()  # Emitido ao final da execução
    current_note = pyqtSignal(int, int)  # Emite a nota e o instrumento atuais

    def __init__(self, sequence=""):
        super().__init__()
        self.sequence = sequence  # Sequência de caracteres fornecida pelo usuário
        self.current_char_index = 0
        self.current_volume=Audio.VOLUME_DEFAULT
        self.current_note_playing =Audio.NOTE_DEFAULT
        self.current_velocity=Audio.VELOCITY_DEFAULT   #em BPM
        self.current_instrument_playing =Audio.INSTRUMENT_DEFAULT
        self.remaining_time = 0.0  # Tempo restante da nota atual
        self.is_paused = False
        self.is_running = True
        
    def setNewNote(self):
        index = self.current_char_index
        current_substr = self.sequence[index:(index+4)]  # Substring de até 4 caracteres para verificar 'BPM+'
    
        if current_substr == "BPM+":
            return
        elif self.sequence[index:(index+2)] == "R+":
            self.current_note_playing += Audio.OITAVA
        elif self.sequence[index:(index+2)] == "R-":
            self.current_note_playing -= Audio.OITAVA
        elif self.sequence[index] in Audio.char_to_midi:
            self.current_note_playing = Audio.char_to_midi[self.sequence[index]]
        elif self.sequence[index].upper() in ['I', 'O', 'U']:
            if not (self.sequence[index-1] in Audio.char_to_midi and self.sequence[index-1] != ' '):
                self.current_note_playing = 125
        elif self.sequence[index] == "?":
            # Gerar número aleatório entre 1 e 7
            random_index = random.randint(1, 7)
            self.current_note_playing = Audio.nota_midi[random_index]


    def set_new_instrument(self):
        index=self.current_char_index
        if(self.sequence[index] == "\n"):
            index_instrumento=random.randint(1, 5)
            self.current_instrument_playing=Audio.instrumentos[index_instrumento]
        return
            
        

    def set_new_velocity(self):
        index=self.current_char_index
        if(self.sequence[index:(index+4)] == "BPM+"):
            self.current_velocity+=80
        elif(self.sequence[index]==";"):
            self.current_velocity=random.randint(50, 100)
        return

            
    def setNewCharIndex(self):
        if self.sequence[self.current_char_index:self.current_char_index + 4] == "BPM+":
            self.current_char_index += 4
        elif self.sequence[self.current_char_index:self.current_char_index + 2] in {"R+", "R-"}:
            self.current_char_index += 2
        else:
            self.current_char_index += 1


    def current_char_is_space(self)->bool:
        if(self.sequence[self.current_char_index]==" "):
            return True
        else:
            return False
    
    def set_new_volume(self):
        if(self.sequence[self.current_char_index]=="+"):
            volume=2*self.current_volume
            if(volume>Audio.VOLUME_MAX):
                self.current_volume=Audio.VOLUME_MAX
            else:
                self.current_volume=volume
        elif(self.sequence[self.current_char_index]=="-"):
            self.current_volume=Audio.VOLUME_DEFAULT
        
    

    def inicia_execucao_nota_atual(self, player: pygame.midi.Output): 
        if(self.current_char_is_space()):
            self.current_note.emit(0,0)
        else:
            player.set_instrument(self.current_instrument_playing)
            self.current_note.emit(self.current_instrument_playing, self.current_note_playing)
            # Toca ou retoma a nota
            player.note_on(self.current_note_playing, self.current_volume)
    
    def termina_execucao_nota_atual(self, player: pygame.midi.Output):
        if not (self.current_char_is_space()):
            player.note_off(self.current_note_playing, self.current_volume)
    
    def aguarda_pause(self):
        while self.is_paused:
            if not self.is_running:
                return
            time.sleep(0.1)

    def controla_execucao_nota_atual(self, player: pygame.midi.Output):     
        self.inicia_execucao_nota_atual(player)
        start_time = time.time()
        currentTime=start_time
        timeMax=60/self.current_velocity
        while (currentTime-start_time) < timeMax:
            if not self.is_running:  # Interrompe execução
                self.termina_execucao_nota_atual(player)
                return

            if self.is_paused:  # Pausa execução
                currentTime=time.time()
                timeMax -= (currentTime - start_time) # atualiza tempo limite, considerando novo limite de tempo restante depois de pausar
                self.termina_execucao_nota_atual(player) # Encerra a nota ao pausar
                if(self.is_paused):
                    self.aguarda_pause()
                # Ao retomar, inicia a nota novamente
                start_time = time.time()
                currentTime=start_time
                self.inicia_execucao_nota_atual(player)
            else:
                currentTime=time.time() #se a nota continuar tocando, atualiza o tempo de execucao até o tempo limite

        # Encerra a nota ao final do tempo
        self.termina_execucao_nota_atual(player)

            

            
    
        




    def run(self):
        pygame.midi.init()
        try:
            player = pygame.midi.Output(0)  # Inicializa saída MIDI

            while self.is_running and self.current_char_index < len(self.sequence):
                 # Configura nova nota
                

                self.setNewNote()
                self.set_new_instrument()
                self.set_new_velocity()
                self.set_new_volume()
                self.remaining_time = 60/self.current_velocity
                self.controla_execucao_nota_atual(player)
                self.setNewCharIndex()  # Avança para a próxima nota

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
