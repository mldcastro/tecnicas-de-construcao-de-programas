from typing import Optional
from PyQt6 import QtWidgets, QtGui, QtCore


class PlayPauseButton(QtWidgets.QAbstractButton):
    def __init__(self) -> None:
        super().__init__()

        self._play_image = QtGui.QPixmap("src/images/play.png").scaled(
            QtCore.QSize(100, 100)
        )
        self._pause_image = QtGui.QPixmap("src/images/pause.png").scaled(
            QtCore.QSize(100, 100)
        )

        self._icon = self._play_image
        self.setIcon(QtGui.QIcon(self._icon))
        self.setFixedSize(self._icon.size())
        self.clicked.connect(self.toggle_icon)

    def toggle_icon(self) -> None:
        if self._icon == self._play_image:
            self._icon = self._pause_image
        else:
            self._icon = self._play_image

        self.setIcon(QtGui.QIcon(self._icon))
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        return self._icon.size()

    def paintEvent(self, e: Optional[QtGui.QPaintEvent]) -> None:
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self._icon)


class RestartButton(QtWidgets.QAbstractButton):
    def __init__(self) -> None:
        super().__init__()

        self._image = QtGui.QPixmap("src/images/restart.png").scaled(
            QtCore.QSize(100, 100)
        )
        self._image_blocked = QtGui.QPixmap("src/images/restart_blocked.png").scaled(
            QtCore.QSize(100, 100)
        )

        self._icon = self._image
        self.setIcon(QtGui.QIcon(self._icon))
        self.setFixedSize(self._icon.size())

        self._is_blocked = False

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    def block(self) -> None:
        self.setDisabled(True)
        self._icon = self._image_blocked
        self.setIcon(QtGui.QIcon(self._icon))
        self.update()

        self._is_blocked = True

    def unblock(self) -> None:
        self.setDisabled(False)
        self._icon = self._image
        self.setIcon(QtGui.QIcon(self._icon))
        self.update()

        self._is_blocked = False

    def sizeHint(self) -> QtCore.QSize:
        return self._icon.size()

    def paintEvent(self, e: Optional[QtGui.QPaintEvent]) -> None:
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self._icon)


class ControlBoard(QtWidgets.QWidget):
    play = QtCore.pyqtSignal()
    pause = QtCore.pyqtSignal()
    restart = QtCore.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)

        self._play_pause_button = PlayPauseButton()
        self._play_pause_button.clicked.connect(self._on_play_pause_button_clicked)

        self._restart_button = RestartButton()
        self._restart_button.clicked.connect(self._on_restart_button_clicked)

        self._layout.addWidget(self._play_pause_button)
        self._layout.addWidget(self._restart_button)

        self._is_playing = False

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    def _on_play_pause_button_clicked(self) -> None:
        self._is_playing = not self._is_playing

        if self._is_playing:
            self._restart_button.block()
            self.play.emit()
        else:
            self._restart_button.unblock()
            self.pause.emit()

    def _on_restart_button_clicked(self) -> None:
        self.restart.emit()
