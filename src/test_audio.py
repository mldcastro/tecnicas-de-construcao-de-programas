import time
import pytest
from collections import deque
from audio import Audio


# Teste para execução sem pausa ou stop
'''
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
        '''

def test_setNewCharIndex():
    audio = Audio(sequence="BPM+R-ABCBPM+R- R+; \nR-OU")
    index_array_test = [0, 4, 6, 7, 8, 9, 13, 15, 16, 18, 19, 20, 21, 23, 24]
    for index in index_array_test:
        assert index==audio.current_char_index
        audio.setNewCharIndex()

def test_setNewNote():
    audio = Audio(sequence="ABCDEFG +- CUIR+R+R-OI?BFE\nBPM+;BPM+D2J920?;")
    flag_random_note=-1
    flag_mantem_nota=-2
     #69   Lá
     #71   Si
     #60   Dó
     #62   Ré
     #64   Mi
     #65   Fá
     #67   Sol
     
    notes_A_to_G=[69,71,60,62,64,65,67]
    note_array_test=[69,71,60,62,64,65,67,67,67,67,67,60,60,125,137,149,137,125,125,flag_random_note,
                     71,65,64,64,64,64,64,62,62,62,62,62,62,flag_random_note,flag_mantem_nota]
    i=0
    for note in note_array_test:
        i=i+1
        print(i)
        if(note==flag_random_note):
            audio.setNewNote()
            assert audio.current_note_playing in notes_A_to_G
        elif(note==flag_mantem_nota):
            previous_note=audio.current_note_playing
            audio.setNewNote()
            assert previous_note==audio.current_note_playing
        else:
            audio.setNewNote()
            assert note==audio.current_note_playing
        audio.setNewCharIndex()

def test_setNewInstrument():
    audio = Audio(sequence="ABC;'A-BPM+R-C9CKQ\nADELA;.2\n")
    instAtual=Audio.INSTRUMENT_DEFAULT
    instrumentos = [0,27,40,73,65]
    while(audio.current_char_index < len(audio.sequence)):
        char=audio.sequence[audio.current_char_index]
        audio.set_new_instrument()
        if(char=='\n'):
            assert audio.current_instrument_playing in instrumentos
            instAtual=audio.current_instrument_playing
        else:
            assert instAtual == audio.current_instrument_playing
        audio.setNewCharIndex()

def test_set_new_velocity():
    audio = Audio(sequence="ABDBPM+-A'A;QBPM+AL;ASBPM+;")
    velAtual = Audio.VELOCITY_DEFAULT
    while audio.current_char_index < len(audio.sequence):
        strIndex = audio.current_char_index
        audio.set_new_velocity()
        if audio.sequence[strIndex:(strIndex+4)] == "BPM+":
            velAtual+=80
            assert velAtual==audio.current_velocity
        elif(audio.sequence[strIndex]==";"):
            instAux=audio.current_velocity
            assert (instAux>=50 and instAux<=100)
            velAtual=audio.current_velocity
        else:
            assert velAtual==audio.current_velocity
        audio.setNewCharIndex()

def test_set_new_volume():
    audio = Audio(sequence="ABD-++-BPM+-A'A;QBPR-++M+AL;AS-BPM+;?++")
    volAtual=Audio.VOLUME_DEFAULT
    while audio.current_char_index < len(audio.sequence):
        char = audio.sequence[audio.current_char_index]
        audio.set_new_volume()
        if char == '+':
            volAux=2*volAtual
            if(volAux<Audio.VOLUME_MAX):
                volAtual=volAux
            else:
                volAtual=audio.VOLUME_MAX
            assert volAtual==audio.current_volume
        elif char=='-':
            volAtual=audio.VOLUME_DEFAULT
            assert volAtual==audio.current_volume
        else:
            assert volAtual==audio.current_volume
        audio.setNewCharIndex()
# Funções de mock
def mock_note_on(note_on_mock, filaTNoteOn):
    def _note_on(*args, **kwargs):
        filaTNoteOn.append(time.time())
        note_on_mock(*args, **kwargs)
    return _note_on

def mock_set_instrument(note_on_mock, filaInstNoteOn):
    def _set_instrument(*args, **kwargs):
        instrument = args[0]
        filaInstNoteOn.append(instrument)
        note_on_mock(*args, **kwargs)
    return _set_instrument

def mock_note_off(note_off_mock, filaTNoteOff):
    def _note_off(*args, **kwargs):
        filaTNoteOff.append(time.time())
        note_off_mock(*args, **kwargs)
    return _note_off

def test_stop(mocker):
    note_on_mock = mocker.MagicMock()
    note_off_mock = mocker.MagicMock()
    time_note_on=deque()
    time_note_off=deque()
    mocker.patch('pygame.midi.Output.note_on', side_effect=mock_note_on(note_on_mock,time_note_on))
    mocker.patch('pygame.midi.Output.note_off', side_effect=mock_note_off(note_off_mock,time_note_off))
    player = Audio(sequence="APZP")
    test_time_note_on=[0,1.0,2.0,3.0]
    test_time_note_off=[1.0,2.0,3.0,3.5]
    
    player.start()
    while not time_note_on:
        time.sleep(0.01)
    time.sleep(3.5)
    player.stop()
    assert len(time_note_on)==4 and len(time_note_off)==4
    startTime=time_note_on[0]
    for i in range (0,4):
        assert pytest.approx(test_time_note_on[i], abs=0.2) == (time_note_on.popleft()-startTime)
        assert pytest.approx(test_time_note_off[i], abs=0.2) == (time_note_off.popleft()-startTime)

def test_pause_and_resume(mocker):
    note_on_mock = mocker.MagicMock()
    note_off_mock = mocker.MagicMock()
    time_note_on=deque()
    time_note_off=deque()
    mocker.patch('pygame.midi.Output.note_on', side_effect=mock_note_on(note_on_mock,time_note_on))
    mocker.patch('pygame.midi.Output.note_off', side_effect=mock_note_off(note_off_mock,time_note_off))
    player = Audio(sequence="APZP")
    test_time_note_on=[0,1.0,2.0,4.2,5.8,6.8]
    test_time_note_off=[1.0,2.0,2.5,4.7,6.8,7.5]
    
    player.start()
    while not time_note_on:
        time.sleep(0.01)

    time.sleep(2.5)
    player.pause()
    time.sleep(1.7)
    player.resume()
    time.sleep(0.5)
    player.pause()
    time.sleep(1.1)
    player.resume()
    time.sleep(1.7)
    player.stop()
    assert len(time_note_on)==6 and len(time_note_off)==6
    startTime=time_note_on[0]
    for i in range (0,5):
        assert pytest.approx(test_time_note_on[i], abs=0.2) == (time_note_on.popleft()-startTime)
        assert pytest.approx(test_time_note_off[i], abs=0.2) == (time_note_off.popleft()-startTime)
        

     
     

        
    
    
    
   




