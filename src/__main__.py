import sys

from PyQt6 import QtWidgets
from typing import Never

from .music_player import MusicPlayer


def main() -> Never:
    app = QtWidgets.QApplication(sys.argv)

    music_player = MusicPlayer()
    music_player.resize(640, 480)
    music_player.setWindowTitle("Music Player")
    music_player.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
