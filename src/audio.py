class Audio:
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def current_instrument(self) -> str: ...

    # Nome auto explicativo.

    @property
    def current_volume(self) -> int: ...

    # Nome auto explicativo.

    @property
    def current_instruction(self) -> str: ...

    # Retorna a instrução do usuário sendo processada no momento.

    def set_instrument(self, instrument: str) -> None: ...

    # Nome auto explicativo.

    def set_volume(self, volume: int) -> None: ...

    # Nome auto explicativo.

    def play(self) -> None: ...

    # Nome auto explicativo.

    def restart(self) -> None: ...

    # Nome auto explicativo.

    def pause(self) -> None: ...

    # Nome auto explicativo.

    def unpause(self) -> None: ...

    # Nome auto explicativo.

    @classmethod
    def from_string(cls, audio_string: str) -> None: ...

    # Inicializa a classe a partir de uma string com caracteres válidos.
    # Aqui será dado como entrada a string do usuário já tratada.

    def _build_audio(self) -> None: ...

    # Itera sobre a string de entrada e constrói a a sua versão sonora.
    # Irá usar o método _map_char_to_midi para fazer isto.

    def _map_char_to_midi(self, char: str) -> int: ...

    # Nome auto explicativo.
