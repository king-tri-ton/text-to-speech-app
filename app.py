import sys
import threading
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sounddevice as sd
import soundfile as sf
import torch
import numpy as np
from icon import ICON_BASE64

class TTSApp(QWidget):
    def __init__(self):
        super().__init__()

        self.language = 'ru'
        self.model_id = 'ru_v3'
        self.sample_rate = 48000
        self.speakers = ['aidar', 'baya', 'kseniya', 'xenia', 'random']
        self.selected_speaker = 'baya'
        self.put_accent = True
        self.put_yo = True
        self.device = torch.device('cpu')

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text to Speech App')
        self.setGeometry(100, 100, 400, 500)

        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ICON_BASE64))

        self.setWindowIcon(QIcon(pixmap))

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.speaker_combo = QComboBox(self)
        self.speaker_combo.addItems(self.speakers)
        self.speaker_combo.setCurrentText(self.selected_speaker)
        layout.addWidget(self.speaker_combo)

        self.create_button = QPushButton('Create Audio', self)
        self.create_button.clicked.connect(self.create_audio)
        layout.addWidget(self.create_button)

        self.play_button = QPushButton('Play Audio', self)
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)

        self.save_button = QPushButton('Save Audio', self)
        self.save_button.clicked.connect(self.save_audio)
        layout.addWidget(self.save_button)

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def create_audio(self):
        text = self.text_edit.toPlainText()
        if text:
            self.selected_speaker = self.speaker_combo.currentText()
            thread = threading.Thread(target=self._create_audio, args=(text,))
            thread.start()
        else:
            self.result_label.setText('Please enter some text.')

    def _create_audio(self, text):
        model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                  model='silero_tts',
                                  language=self.language,
                                  speaker=self.model_id)
        model.to(self.device)

        audio = model.apply_tts(text=text + "..",
                                speaker=self.selected_speaker,
                                sample_rate=self.sample_rate,
                                put_accent=self.put_accent,
                                put_yo=self.put_yo)

        self.audio_data = audio
        self.result_label.setText('Audio created successfully.')

    def play_audio(self):
        if hasattr(self, 'audio_data'):
            thread = threading.Thread(target=self._play_audio)
            thread.start()
        else:
            self.result_label.setText('No audio to play. Create audio first.')

    def _play_audio(self):
        sd.play(self.audio_data, self.sample_rate)
        sd.wait()
        self.result_label.setText('Audio played successfully.')

    def save_audio(self):
        if hasattr(self, 'audio_data'):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "WAV Files (*.wav);;All Files (*)", options=options)

            if file_name:
                audio_np = self.audio_data.numpy()
                audio_int16 = (audio_np * 32767).astype(np.int16)

                if not file_name.lower().endswith('.wav'):
                    file_name += '.wav'

                sf.write(file_name, audio_int16, self.sample_rate, format='wav')
                self.result_label.setText(f'Audio saved to: {file_name}')
            else:
                self.result_label.setText('Save operation canceled.')
        else:
            self.result_label.setText('No audio to save. Create audio first.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tts_app = TTSApp()
    tts_app.show()
    sys.exit(app.exec_())
