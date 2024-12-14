import unittest
from collections import deque
from unittest.mock import patch, MagicMock
import time
from audio_ import Audio

# O seu teste aqui
class TestAudio(unittest.TestCase):

    def test_play_notes_without_pause_or_stop(self):
        # Seu código de teste
        note_on_mock = MagicMock()
        note_off_mock = MagicMock()
        set_instrument_mock = MagicMock()

        filaTNoteOn = deque()
        filaNotaNoteOn = deque()
        filaInstNoteOn = deque()

        filaTNoteOff = deque()
        filaNotaNoteOff = deque()

        filaTNoteOnTest = deque()
        filaNotaNoteOnTest = deque()
        filaInstNoteOnTest = deque()

        filaTNoteOffTest = deque()
        filaNotaNoteOffTest = deque()

        # Mockando métodos do pygame.midi.Output
        with patch('pygame.midi.Output.note_on', side_effect=mock_note_on(note_on_mock, filaTNoteOn, filaNotaNoteOn)):
            with patch('pygame.midi.Output.note_off', side_effect=mock_note_off(note_off_mock, filaTNoteOff, filaNotaNoteOff)):
                with patch('pygame.midi.Output.set_instrument', side_effect=mock_set_instrument(set_instrument_mock, filaInstNoteOn)):
                    # Instância do objeto a ser testado
                    player = Audio(sequence="APZA")

                    filaNotaNoteOnTest.extend([60, 50, 40, 60])
                    filaInstNoteOnTest.extend([110, 100, 90, 110])
                    filaNotaNoteOffTest.extend([60, 50, 40, 60])

                    intervalo = 2.0
                    for i in range(4):
                        filaTNoteOnTest.append(intervalo * i)
                        filaTNoteOffTest.append(intervalo * (i + 1))

                    player.start()  # Inicia a execução em uma thread
                    player.wait()  # Espera a execução terminar

                    tempoIniBase = filaTNoteOn[0]
                    # Verificação dos resultados
                    while filaNotaNoteOn:
                        NotaOn = filaNotaNoteOn.popleft()
                        NotaTesteOn = filaNotaNoteOnTest.popleft()
                        self.assertEqual(NotaTesteOn, NotaOn, f"Nota iniciada incorreta")

                        NotaOff = filaNotaNoteOff.popleft()
                        NotaTesteOff = filaNotaNoteOffTest.popleft()
                        self.assertEqual(NotaTesteOff, NotaOff, f"Nota finalizada incorreta")

                        InstOn = filaInstNoteOn.popleft()
                        InstTesteOn = filaInstNoteOnTest.popleft()
                        self.assertEqual(InstTesteOn, InstOn, f"Instrumento iniciado incorreto")

                        TimeOn = filaTNoteOn.popleft()
                        TimeTesteOn = filaTNoteOnTest.popleft()
                        self.assertAlmostEqual(TimeTesteOn, (TimeOn - tempoIniBase), delta=0.2, msg=f"Inicializacao no tempo incorreto")

                        TimeOff = filaTNoteOff.popleft()
                        TimeTesteOff = filaTNoteOffTest.popleft()
                        self.assertAlmostEqual(TimeTesteOff, (TimeOff - tempoIniBase), delta=0.2, msg=f"Finalizacao no tempo incorreto")

    def test_play_notes_with_pause(self):
        # Seu código de teste
        note_on_mock = MagicMock()
        note_off_mock = MagicMock()
        set_instrument_mock = MagicMock()

        filaTNoteOn = deque()
        filaNotaNoteOn = deque()
        filaInstNoteOn = deque()

        filaTNoteOff = deque()
        filaNotaNoteOff = deque()

        filaTNoteOnTest = deque()
        filaNotaNoteOnTest = deque()
        filaInstNoteOnTest = deque()

        filaTNoteOffTest = deque()
        filaNotaNoteOffTest = deque()

        # Mockando métodos do pygame.midi.Output
        with patch('pygame.midi.Output.note_on', side_effect=mock_note_on(note_on_mock, filaTNoteOn, filaNotaNoteOn)):
            with patch('pygame.midi.Output.note_off', side_effect=mock_note_off(note_off_mock, filaTNoteOff, filaNotaNoteOff)):
                with patch('pygame.midi.Output.set_instrument', side_effect=mock_set_instrument(set_instrument_mock, filaInstNoteOn)):
                    # Instância do objeto a ser testado
                    player = Audio(sequence="APZP")

                    filaNotaNoteOnTest.extend([60, 50, 50, 50, 40, 50])
                    filaInstNoteOnTest.extend([110, 100,  90, 100])
                    filaNotaNoteOffTest.extend([60, 50, 50, 50, 40, 50])
                    filaTNoteOnTest.extend([0, 2, 4.2, 5.8, 6.8, 8.8])
                    filaTNoteOffTest.extend([2, 2.5, 4.7, 6.8, 8.8, 10.8])
                    
                    player.start()  # Inicia a execução em uma thread
                   
                    
                    while not filaTNoteOn:
                        time.sleep(0.01)
                    
                    
                    time.sleep(2.5)
                    player.pause()
                    time.sleep(1.7)
                    player.resume()
                    time.sleep(0.5)
                    player.pause()
                    time.sleep(1.1)
                    player.resume()

                    player.wait()  # Espera a execução terminar

                    tempoIniBase = filaTNoteOn[0]
                    """ print(filaTNoteOn[0]-tempoIniBase)
                    print(filaTNoteOn[1]-tempoIniBase)
                    print(filaTNoteOn[2]-tempoIniBase)
                    print(filaTNoteOff[0]-tempoIniBase)
                    print(filaTNoteOff[1]-tempoIniBase)

                    print(filaNotaNoteOn[0])
                    print(filaNotaNoteOn[1])
                    print(filaNotaNoteOn[2])
                    print(filaNotaNoteOff[0])
                    print(filaNotaNoteOff[1])

                    print(filaInstNoteOn[0])
                    print(filaInstNoteOn[1])
                    print(filaInstNoteOn[2])"""
                    for i in range(0,4):
                        InstOn = filaInstNoteOn.popleft()
                        InstTesteOn = filaInstNoteOnTest.popleft()
                        self.assertEqual(InstTesteOn, InstOn, f"Instrumento {i+1} iniciado incorreto")
                    # Verificação dos resultados
                    for i in range(0,6):
                        NotaOn = filaNotaNoteOn.popleft()
                        NotaTesteOn = filaNotaNoteOnTest.popleft()
                        self.assertEqual(NotaTesteOn, NotaOn, f"Nota {i+1} iniciada incorreta")

                        NotaOff = filaNotaNoteOff.popleft()
                        NotaTesteOff = filaNotaNoteOffTest.popleft()
                        self.assertEqual(NotaTesteOff, NotaOff, f"Nota {i+1} finalizada incorreta")

                       

                        TimeOn = filaTNoteOn.popleft()
                        TimeTesteOn = filaTNoteOnTest.popleft()
                        self.assertAlmostEqual(TimeTesteOn, (TimeOn - tempoIniBase), delta=0.2, msg=f"Inicializacao {i+1}  no tempo incorreto")

                        TimeOff = filaTNoteOff.popleft()
                        TimeTesteOff = filaTNoteOffTest.popleft()
                        self.assertAlmostEqual(TimeTesteOff, (TimeOff - tempoIniBase), delta=0.2, msg=f"Finalizacao {i+1} no tempo incorreto")

def mock_note_on(note_on_mock, filaTNoteOn, filaNotaNoteOn):
    def _note_on(*args, **kwargs):
        filaTNoteOn.append(time.time())  # Armazena o tempo
        note = args[0]  # Nota está geralmente no primeiro argumento
        filaNotaNoteOn.append(note)  # Armazena a nota
        note_on_mock(*args, **kwargs)  # Chama o método original
    return _note_on

def mock_set_instrument(note_on_mock, filaInstNoteOn):
    def _set_instrument(*args, **kwargs):
        instrument = args[0]
        filaInstNoteOn.append(instrument)  # Armazena o instrumento
        note_on_mock(*args, **kwargs)  # Chama o método original
    return _set_instrument

def mock_note_off(note_off_mock, filaTNoteOff, filaNotaNoteOff):
    def _note_off(*args, **kwargs):
        filaTNoteOff.append(time.time())  # Armazena o tempo
        note = args[0]  # Nota está geralmente no primeiro argumento
        filaNotaNoteOff.append(note)  # Armazena a nota
        note_off_mock(*args, **kwargs)  # Chama o método original
    return _note_off

if __name__ == '__main__':
    unittest.main()  # Garante que os testes serão executados quando o arquivo for chamado diretamente
