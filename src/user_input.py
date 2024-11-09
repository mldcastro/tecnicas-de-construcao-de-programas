from .input_error import InputException


class UserInputBox(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def value(self) -> str: ...

    # Texto contido dentro da caixa de texto.

    @property
    def is_blocked(self) -> bool: ...

    # Nome auto explicativo.

    @property
    def is_valid(self) -> bool: ...

    # O input é válido ou não.

    def _validate_input(self) -> None:
        # Nome auto explicativo.
        ...
        raise InputException("Invalid input")

    def _on_ok_pressed(self) -> None: ...

    # Irá salvar a string, que fará a verificação do texto e envio para o mapeamento.

    def block(self) -> None: ...

    # Nome auto explicativo.

    def unblock(self) -> None: ...

    # Nome auto explicativo.
