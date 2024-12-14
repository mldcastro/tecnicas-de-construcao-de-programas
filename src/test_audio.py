import time
import pytest
from collections import deque
from audio import Audio

# Funções de mock
def mock_note_on(note_on_mock, filaTNoteOn, filaNotaNoteOn):
    def _note_on(*args, **kwargs):
        filaTNoteOn.append(time.time())
        note = args[0]
        filaNotaNoteOn.append(note)
        note_on_mock(*args, **kwargs)
    return _note_on

def mock_set_instrument(note_on_mock, filaInstNoteOn):
    def _set_instrument(*args, **kwargs):
        instrument = args[0]
        filaInstNoteOn.append(instrument)
        note_on_mock(*args, **kwargs)
    return _set_instrument

def mock_note_off(note_off_mock, filaTNoteOff, filaNotaNoteOff):
    def _note_off(*args, **kwargs):
        filaTNoteOff.append(time.time())
        note = args[0]
        filaNotaNoteOff.append(note)
        note_off_mock(*args, **kwargs)
    return _note_off

# Teste para execução sem pausa ou stop
def test_play_notes_without_pause_or_stop(mocker):
    note_on_mock = mocker.MagicMock()
    note_off_mock = mocker.MagicMock()
    set_instrument_mock = mocker.MagicMock()

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

    # Usando mocker para fazer o patch
    mocker.patch('pygame.midi.Output.note_on', side_effect=mock_note_on(note_on_mock, filaTNoteOn, filaNotaNoteOn))
    mocker.patch('pygame.midi.Output.note_off', side_effect=mock_note_off(note_off_mock, filaTNoteOff, filaNotaNoteOff))
    mocker.patch('pygame.midi.Output.set_instrument', side_effect=mock_set_instrument(set_instrument_mock, filaInstNoteOn))

    player = Audio(sequence="APZA")
    filaNotaNoteOnTest.extend([60, 50, 40, 60])
    filaInstNoteOnTest.extend([110, 100, 90, 110])
    filaNotaNoteOffTest.extend([60, 50, 40, 60])

    intervalo = 2.0
    for i in range(4):
        filaTNoteOnTest.append(intervalo * i)
        filaTNoteOffTest.append(intervalo * (i + 1))

    player.start()
    player.wait()

    tempoIniBase = filaTNoteOn[0]

    while filaNotaNoteOn:
        NotaOn = filaNotaNoteOn.popleft()
        NotaTesteOn = filaNotaNoteOnTest.popleft()
        assert NotaTesteOn == NotaOn

        NotaOff = filaNotaNoteOff.popleft()
        NotaTesteOff = filaNotaNoteOffTest.popleft()
        assert NotaTesteOff == NotaOff

        InstOn = filaInstNoteOn.popleft()
        InstTesteOn = filaInstNoteOnTest.popleft()
        assert InstTesteOn == InstOn

        TimeOn = filaTNoteOn.popleft()
        TimeTesteOn = filaTNoteOnTest.popleft()
        assert pytest.approx(TimeTesteOn, abs=0.2) == (TimeOn - tempoIniBase)

        TimeOff = filaTNoteOff.popleft()
        TimeTesteOff = filaTNoteOffTest.popleft()
        assert pytest.approx(TimeTesteOff, abs=0.2) == (TimeOff - tempoIniBase)

# Teste com pausa
def test_play_notes_with_pause(mocker):
    note_on_mock = mocker.MagicMock()
    note_off_mock = mocker.MagicMock()
    set_instrument_mock = mocker.MagicMock()

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

    # Usando mocker para fazer o patch
    mocker.patch('pygame.midi.Output.note_on', side_effect=mock_note_on(note_on_mock, filaTNoteOn, filaNotaNoteOn))
    mocker.patch('pygame.midi.Output.note_off', side_effect=mock_note_off(note_off_mock, filaTNoteOff, filaNotaNoteOff))
    mocker.patch('pygame.midi.Output.set_instrument', side_effect=mock_set_instrument(set_instrument_mock, filaInstNoteOn))

    player = Audio(sequence="APZP")
    filaNotaNoteOnTest.extend([60, 50, 50, 50, 40, 50])
    filaInstNoteOnTest.extend([110, 100, 90, 100])
    filaNotaNoteOffTest.extend([60, 50, 50, 50, 40, 50])
    filaTNoteOnTest.extend([0, 2, 4.2, 5.8, 6.8, 8.8])
    filaTNoteOffTest.extend([2, 2.5, 4.7, 6.8, 8.8, 10.8])

    player.start()

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

    player.wait()

    tempoIniBase = filaTNoteOn[0]

    for i in range(4):
        InstOn = filaInstNoteOn.popleft()
        InstTesteOn = filaInstNoteOnTest.popleft()
        assert InstTesteOn == InstOn

    for i in range(6):
        NotaOn = filaNotaNoteOn.popleft()
        NotaTesteOn = filaNotaNoteOnTest.popleft()
        assert NotaTesteOn == NotaOn

        NotaOff = filaNotaNoteOff.popleft()
        NotaTesteOff = filaNotaNoteOffTest.popleft()
        assert NotaTesteOff == NotaOff

        TimeOn = filaTNoteOn.popleft()
        TimeTesteOn = filaTNoteOnTest.popleft()
        assert pytest.approx(TimeTesteOn, abs=0.2) == (TimeOn - tempoIniBase)

        TimeOff = filaTNoteOff.popleft()
        TimeTesteOff = filaTNoteOffTest.popleft()
        assert pytest.approx(TimeTesteOff, abs=0.2) == (TimeOff - tempoIniBase)
