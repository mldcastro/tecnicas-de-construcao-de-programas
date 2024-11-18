import pytest

from src.input_validator import InputValidator
from src.command_list import Commands
from src.input_error import InputException


def test_raises_exception_if_input_is_empty():
    with pytest.raises(InputException, match=InputValidator.EMPTY_INPUT_ERROR_MESSAGE):
        InputValidator.validate("")


def test_raises_exception_if_input_has_no_mandatory_commands():
    with pytest.raises(
        InputException, match=InputValidator.NO_MANDATORY_COMMAND_ERROR_MESSAGE
    ):
        InputValidator.validate("--")


@pytest.mark.parametrize("command", Commands.mandatory())
def test_returns_none_for_input_with_one_mandatory_command_only(command):
    assert InputValidator.validate(command.value) is None


def test_returns_none_for_valid_input_with_chars_not_defined_in_commands():
    assert InputValidator.validate("A 123") is None
