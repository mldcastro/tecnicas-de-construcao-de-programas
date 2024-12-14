from src.control_board import ControlBoard


def test_start_with_play_button(qtbot):
    control_board = ControlBoard()
    assert (
        control_board._play_pause_button._icon
        == control_board._play_pause_button._play_image
    )


def test_starts_with_restart_unblocked(qtbot):
    control_board = ControlBoard()
    assert not control_board._restart_button.is_blocked


def test_starts_not_playing(qtbot):
    control_board = ControlBoard()
    assert not control_board._is_playing


def test_click_play_blocks_restart(qtbot):
    control_board = ControlBoard()
    control_board._play_pause_button.click()

    assert control_board._restart_button.is_blocked


def test_click_pause_unblocks_restart(qtbot):
    control_board = ControlBoard()
    control_board._play_pause_button.click()
    control_board._play_pause_button.click()

    assert not control_board._restart_button.is_blocked


def test_click_play_emits_signal(qtbot):
    control_board = ControlBoard()
    with qtbot.waitSignal(control_board.play):
        control_board._play_pause_button.click()


def test_click_pause_emits_signal(qtbot):
    control_board = ControlBoard()
    with qtbot.waitSignal(control_board.pause):
        control_board._play_pause_button.click()
        control_board._play_pause_button.click()


def test_click_restart_emits_signal(qtbot):
    control_board = ControlBoard()
    with qtbot.waitSignal(control_board.restart):
        control_board._restart_button.click()
