from prettytable import PrettyTable
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from .commands import Commands


class CommandListBox(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self._text = QtWidgets.QLabel()
        self._text.setWordWrap(True)
        self._text.setTextFormat(Qt.TextFormat.RichText)
        self._text.setFixedHeight(430)

        self._layout.addWidget(self._text)

    def display(self) -> None:
        self._text.setText(self._commands_explanation_to_html())
        self.show()

    @staticmethod
    def _commands_explanation_as_list(col_separator: str) -> list[list[str]]:
        lines = [s.strip() for s in Commands.explanation().splitlines()]
        rows = [line.split(col_separator) for line in lines]
        return [col for col in rows if col != [""]]

    def _commands_explanation_to_html(self, col_separator: str = ":") -> str:
        explanation_as_list = self._commands_explanation_as_list(col_separator)

        table = PrettyTable(
            field_names=["Comando", "Descrição"],
            title="LISTA DE COMANDOS",
            align="l",
            right_padding_width=3,
        )
        table.add_rows(explanation_as_list)

        # The get_html_string method does not takes into account the left-alignment
        # we did before, so here we replace the "center" alignment with "left" to
        # ensure the left-alignment is preserved.
        return table.get_html_string(format=True).replace("center", "left")
