import pyaudio

class Config:
    # Audio settings
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    # Wake word detection settings
    WAKE_WORD_THRESHOLD = 0.5

    # GUI settings
    WINDOW_SIZE = "400x500"
    WINDOW_TITLE = "Wake Word Detection App"

    # RMS meter settings
    RMS_UPDATE_INTERVAL = 100  # milliseconds
    RMS_SCALE_FACTOR = 20.0  # Increased scale factor for better visibility

    # Model settings
    DEFAULT_MODEL = "alexa"
    MODEL_OPTIONS = ["alexa", "eugene"]

    @classmethod
    def get_model_path(cls, model_name):
        return f"models/{model_name}.onnx"