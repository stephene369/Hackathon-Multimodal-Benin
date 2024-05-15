from .lib import * 
from transformers import pipeline


class VoiceWidget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.transcription_box = QTextEdit(self)
        self.transcription_box.setReadOnly(True)
        self.transcription_box.setPlaceholderText("Transcription will appear here")

        self.button = PushButton("Select Audio File", self)
        self.button.clicked.connect(self.transcribe_audio)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.transcription_box)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.worker_thread = None
        self.transcription_worker = None

        self.setObjectName(text.replace(' ', '-'))

    def transcribe_audio(self):
        self.button.setEnabled(False)  # Désactiver le bouton pendant le traitement

        audio_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.ogg *.wav *.mp3)")
        if audio_path:
            self.transcription_worker = TranscriptionWorker(audio_path)
            self.worker_thread = QThread()
            self.transcription_worker.moveToThread(self.worker_thread)
            self.transcription_worker.finished.connect(self.handle_transcription_finished)
            self.worker_thread.started.connect(self.transcription_worker.run)
            self.worker_thread.start()

            self.stateTooltip = StateToolTip('En cours', 'Veuillez patienter, ceci peut prendre un moment.', self)
            self.stateTooltip.move(510, 30)
            self.stateTooltip.show()

    def handle_transcription_finished(self, transcription):
        self.transcription_box.setPlainText(transcription)
        self.button.setEnabled(True)  # Réactiver le bouton après le traitement


        self.stateTooltip.setContent('Operation terminee')
        self.stateTooltip.setState(True)
        self.stateTooltip = None




class TranscriptionWorker(QObject):
    finished = pyqtSignal(str)

    def __init__(self, audio_path):
        super().__init__()
        self.audio_path = audio_path

    def run(self):
        pipe = pipeline("automatic-speech-recognition", model="chrisjay/fonxlsr")
        transcription = pipe(self.audio_path)
        self.finished.emit(transcription['text'])


