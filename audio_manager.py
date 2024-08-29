import pyaudio
import numpy as np
from config import Config
from error_handler import log_error, handle_error, AudioError
from playsound import playsound

class AudioManager:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.audio_stream = None
        self.is_listening = False

    @staticmethod
    def get_audio_devices():
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        devices = []
        for i in range(0, num_devices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices.append(f"{i}: {p.get_device_info_by_host_api_device_index(0, i).get('name')}")
        p.terminate()
        return devices

    @log_error
    def start_listening(self, device_index, callback):
        try:
            self.is_listening = True
            device_info = self.pa.get_device_info_by_index(device_index)
            self.audio_stream = self.pa.open(
                format=Config.FORMAT,
                channels=Config.CHANNELS,
                rate=Config.RATE,
                input=True,
                input_device_index=device_info['index'],
                frames_per_buffer=Config.CHUNK,
                stream_callback=callback
            )
            self.audio_stream.start_stream()
        except Exception as e:
            handle_error(AudioError, f"Failed to start listening: {str(e)}")
            self.is_listening = False
            raise

    @log_error
    def stop_listening(self):
        self.is_listening = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

    @staticmethod
    def normalize_audio(audio_data):
        return audio_data.astype(np.float32) / 32768.0

    @staticmethod
    def calculate_rms(audio_data):
        return np.sqrt(np.mean(np.square(audio_data)))

    @staticmethod
    def play_sound(sound_file):
        try:
            playsound(sound_file)
        except Exception as e:
            handle_error(AudioError, f"Failed to play sound: {str(e)}")

    def cleanup(self):
        self.stop_listening()
        self.pa.terminate()