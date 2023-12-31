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
        self.setWindowTitle('Text-to-Speech App')
        self.setGeometry(100, 100, 400, 500)

        icon_data = b'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'
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(icon_data))

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
