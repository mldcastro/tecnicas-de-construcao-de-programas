class CommandListBox(...):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def value(self) -> str: ...

    # Texto contido dentro da caixa de texto.

    def display(self) -> None: ...

    # Mostrar o texto para o usuário.

    def hide(self) -> None: ...

    # Esconder o texto do usuário.