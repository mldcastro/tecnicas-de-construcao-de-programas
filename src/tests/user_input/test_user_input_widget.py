import pytest

from src.user_input import UserInputWidget, InputException, InputValidator
from src.commands import Commands


def test_none_value_at_start(qtbot):
    user_input_widget = UserInputWidget()
    assert user_input_widget.value is None


def test_none_is_valid_at_start(qtbot):
    user_input_widget = UserInputWidget()
    assert user_input_widget.is_valid is None


def test_not_blocked_at_start(qtbot):
    user_input_widget = UserInputWidget()

    assert not user_input_widget.is_blocked
    assert user_input_widget._input.isEnabled()
    assert user_input_widget._ok_button.isEnabled()
    assert user_input_widget._txt_loader.isEnabled()


def test_block(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget.block()

    assert user_input_widget.is_blocked
    assert not user_input_widget._input.isEnabled()
    assert not user_input_widget._ok_button.isEnabled()
    assert not user_input_widget._txt_loader.isEnabled()


def test_unblock(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget.block()
    user_input_widget.unblock()

    assert not user_input_widget.is_blocked
    assert user_input_widget._input.isEnabled()
    assert user_input_widget._ok_button.isEnabled()
    assert user_input_widget._txt_loader.isEnabled()


def test_empty_input_is_invalid(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText("")

    with pytest.raises(
        InputException, match=InputValidator.EMPTY_INPUT_ERROR_MESSAGE
    ) as _:
        user_input_widget._validate_input()

    assert not user_input_widget.is_valid


def test_input_with_no_mandatory_commands_is_invalid(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText("1")

    with pytest.raises(
        InputException, match=InputValidator.NO_MANDATORY_COMMAND_ERROR_MESSAGE
    ) as _:
        user_input_widget._validate_input()

    assert not user_input_widget.is_valid


@pytest.mark.parametrize("command", Commands.mandatory())
def test_input_with_one_mandatory_command_is_valid(qtbot, command):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText(command.value)
    user_input_widget._validate_input()


@pytest.mark.parametrize("command", Commands.mandatory())
def test_input_with_one_uppercase_mandatory_command_is_valid(qtbot, command):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText(command.value.upper())
    user_input_widget._validate_input()


def test_is_valid_is_true_for_valid_input(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText("a")
    user_input_widget._ok_button.click()

    assert user_input_widget.is_valid


def test_value_is_input_when_valid(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText("a")
    user_input_widget._ok_button.click()

    assert user_input_widget.value == "a"


def test_click_ok_emits_signal(qtbot):
    user_input_widget = UserInputWidget()
    user_input_widget._input.setPlainText("a")

    with qtbot.waitSignal(user_input_widget.value_changed):
        user_input_widget._ok_button.click()
