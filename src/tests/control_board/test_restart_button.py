from src.control_board import RestartButton


def test_starts_unblocked(qtbot):
    restart_button = RestartButton()

    assert not restart_button.is_blocked
    assert restart_button.isEnabled()
    assert restart_button._icon == restart_button._image


def test_remains_unblocked_after_click(qtbot):
    restart_button = RestartButton()
    restart_button.click()

    assert not restart_button.is_blocked
    assert restart_button.isEnabled()
    assert restart_button._icon == restart_button._image


def test_block(qtbot):
    restart_button = RestartButton()
    restart_button.block()

    assert restart_button.is_blocked
    assert not restart_button.isEnabled()
    assert restart_button._icon == restart_button._image_blocked


def test_unblocks(qtbot):
    restart_button = RestartButton()
    restart_button.block()
    restart_button.unblock()

    assert not restart_button.is_blocked
    assert restart_button.isEnabled()
    assert restart_button._icon == restart_button._image
