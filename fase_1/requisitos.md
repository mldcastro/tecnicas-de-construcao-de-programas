# Requisitos do programa Music Player

## Visível ao usuário

O(a) usuário(a) irá digitar uma sequência de caracteres em uma caixa de texto. Após isso, irá
apertar play, e a música irá tocar. Ele(a) poderá pausar a música a qualquer instante.

- Caixa de texto para o usuário digitar o comando desejado;
  - Botão de `Ok` para finalizar input.
- Uma lista dos comandos aceitos pelo programa;
- Um texto (ou marcador) para mostrar a nota sendo tocada no momento;
- Botão ou tecla de play;
- Botão ou tecla de pause;
- Botão ou tecla de reiniciar;
- Sinalização de erros no texto de entrada;
- Bloquear a caixa de texto durante a execução da música;
- Bloquear a caixa de texto durante o pause;
- Sinalizar o instrumento MIDI atual;
- Sinalizar que a música está tocando;
- Quando a música acaba, se o usuário clicar play, volta do início;

## Para os desenvolvedores

- Definir tempo de duração de cada nota;
- Definir um instrumento MIDI default;
- Implementar a lógica para bloquear e desbloquear os botões de controle (Play, Pause, Reiniciar) em diferentes estados do programa (por exemplo, bloquear "Play" durante a execução da música e desbloquear "Pause");
- Otimizar o uso de recursos para garantir que a música toque sem interrupções ou travamentos;

## Possíveis bibliotecas

- Pygame;
- PyQt.

## Interface

Classes planejadas:

```python
class Audio(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def current_instrument(self) -> str: ...

    @property
    def current_volume(self) -> int: ...

    @property
    def current_instruction(self) -> str: ...

    def set_instrument(self, instrument: str) -> None: ...

    def set_volume(self, volume: int) -> None: ...

    def play(self) -> None: ...

    def restart(self) -> None: ...

    def pause(self) -> None: ...

    def unpause(self) -> None: ...

    @classmethod
    def from_string(cls, audio_string: str) -> None: ...

    def _build_audio(self) -> None: ...

    def _map_char_to_midi(self, char: str) -> int: ...


class UserInputBox(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def value(self) -> str: ...

    @property
    def is_blocked(self) -> bool: ...

    def _validate_input(self) -> None:
        ...
        raise InputException("Invalid input")

    def _on_ok_pressed(self) -> None: ...

    def block(self) -> None: ...

    def unblock(self) -> None: ...


class InputException(Exception):
    pass


class InputErrorBox(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def value(self) -> str: ...

    def display(self) -> None: ...

    def hide(self) -> None: ...


class CommandListBox(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def value(self) -> str: ...

    def display(self) -> None: ...

    def hide(self) -> None: ...


class MidiInstrumentBox(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def value(self) -> str: ...

    def set_instrument(self, instrument: str) -> None: ...

    def display(self) -> None: ...

    def hide(self) -> None: ...


class ControlBoard(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def is_playing(self) -> bool: ...

    def play(self) -> None: ...

    def pause(self) -> None: ...

    def unpause(self) -> None: ...

    def restart(self) -> None: ...

    def block_play(self) -> None: ...

    def unblock_play(self) -> None: ...

    def block_pause(self) -> None: ...

    def unblock_pause(self) -> None: ...

    def block_restart(self) -> None: ...

    def unblock_restart(self) -> None: ...

```

## Croqui

![croqui](./croqui.png)
