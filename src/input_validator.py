from .command_list import Commands
from .input_error import InputException


class InputValidator:
    EMPTY_INPUT_ERROR_MESSAGE = "A entrada não pode ser vazia."
    NO_MANDATORY_COMMAND_ERROR_MESSAGE = (
        "A entrada deve conter pelo menos uma nota ou comandos de repetição definidos."
    )

    @staticmethod
    def _has_at_least_one_mandatory_command_defined(input_str: str) -> bool:
        return any(command in input_str.lower() for command in Commands.mandatory())

    @classmethod
    def validate(cls, input_str: str) -> None:
        if not input_str:
            raise InputException(cls.EMPTY_INPUT_ERROR_MESSAGE)

        if not cls._has_at_least_one_mandatory_command_defined(input_str):
            raise InputException(cls.NO_MANDATORY_COMMAND_ERROR_MESSAGE)
