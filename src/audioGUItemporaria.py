import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from audio import Audio

class AudioPlayerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_player = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Player")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.input_field = QTextEdit(self)  # Substituído QLineEdit por QTextEdit
        self.input_field.setPlaceholderText("Digite uma sequência de A-Z")
        layout.addWidget(self.input_field)

        self.status_label = QLabel("Status: Parado", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Ajuste para PyQt6
        layout.addWidget(self.status_label)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause_audio)
        layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume", self)
        self.resume_button.setEnabled(False)
        self.resume_button.clicked.connect(self.resume_audio)
        layout.addWidget(self.resume_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_audio)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def play_audio(self):
        sequence = self.input_field.toPlainText().strip().upper()  # Para QTextEdit, usa-se toPlainText()
        if not sequence:
            self.status_label.setText("Erro: Insira uma sequência válida!")
            return

        self.status_label.setText("Status: Tocando")
        self.audio_player = Audio(sequence)
        self.audio_player.current_note.connect(self.update_status)
        self.audio_player.finished.connect(self.on_finished)
        self.audio_player.start()

        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)

    def pause_audio(self):
        self.status_label.setText("Status: Pausado")
        self.audio_player.pause()
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(True)

    def resume_audio(self):
        self.status_label.setText("Status: Tocando")
        self.audio_player.resume()
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)

    def stop_audio(self):
        self.status_label.setText("Status: Parado")
        if self.audio_player:
            self.audio_player.stop()

        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def update_status(self, instrument, note):
        self.status_label.setText(f"Tocando: Nota {note}, Instrumento {instrument}")

    def on_finished(self):
        self.status_label.setText("Status: Concluído")
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AudioPlayerGUI()
    gui.show()
    sys.exit(app.exec())
