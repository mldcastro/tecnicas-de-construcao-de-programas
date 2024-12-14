from src.control_board import PlayPauseButton


def test_starts_with_play_button(qtbot):
    play_pause_button = PlayPauseButton()
    assert play_pause_button._icon == play_pause_button._play_image


def test_changes_to_pause_after_click(qtbot):
    play_pause_button = PlayPauseButton()
    play_pause_button.click()

    assert play_pause_button._icon == play_pause_button._pause_image


def test_changes_to_play_after_pause_button_clicked(qtbot):
    play_pause_button = PlayPauseButton()
    play_pause_button.click()
    play_pause_button.click()

    assert play_pause_button._icon == play_pause_button._play_image
