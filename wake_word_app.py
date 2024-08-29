import customtkinter as ctk
import numpy as np
import os
import time
import threading
import pyaudio
from model import Model
from error_handler import log_error, handle_error, ModelError
from config import Config
from gui_components import DeviceFrame, ModelFrame, ToggleButton, StatusLabel, RMSMeter, WakeWordIndicator
from audio_manager import AudioManager

class WakeWordApp:
    def __init__(self, master, initial_model=None):
        self.master = master
        self.master.title(Config.WINDOW_TITLE)
        self.master.geometry(Config.WINDOW_SIZE)

        self.audio_manager = AudioManager()
        self.model = None

        self.device_var = ctk.StringVar()
        self.model_var = ctk.StringVar()

        # Load the default model immediately
        default_model = initial_model or Config.DEFAULT_MODEL
        self.load_model(os.path.join(os.path.dirname(__file__), 'models', f"{default_model}.onnx"))

        self.setup_gui()

        self.master.protocol("WM_DELETE_WINDOW", self.cleanup)

        # Add variables for wake word smoothing
        self.last_wake_word_time = 0
        self.wake_word_cooldown = 2  # 2 seconds cooldown
        self.wake_word_active = False

    @log_error
    def setup_gui(self):
        device_options = AudioManager.get_audio_devices()
        self.device_frame = DeviceFrame(self.master, self.device_var, device_options)

        model_options = self.get_model_files()
        self.model_frame = ModelFrame(self.master, self.model_var, model_options, self.on_model_select)

        self.toggle_button = ToggleButton(self.master, self.toggle_listening)
        self.status_label = StatusLabel(self.master)
        self.rms_meter = RMSMeter(self.master)
        self.wake_word_indicator = WakeWordIndicator(self.master)

    @log_error
    def get_model_files(self):
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        if not os.path.exists(model_dir):
            return []
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.onnx')]
        return model_files

    @log_error
    def on_model_select(self, choice):
        model_path = os.path.join(os.path.dirname(__file__), 'models', choice)
        self.load_model(model_path)

    @log_error
    def load_model(self, model_path):
        try:
            self.model = Model([model_path])
        except Exception as e:
            handle_error(ModelError, f"Failed to initialize model: {str(e)}")
            self.model = None

    @log_error
    def toggle_listening(self):
        if self.audio_manager.is_listening:
            self.stop_listening()
        else:
            self.start_listening()

    @log_error
    def start_listening(self):
        try:
            device_index = int(self.device_var.get().split(':')[0])
            self.audio_manager.start_listening(device_index, self.audio_callback)
            self.toggle_button.set_listening_state(True)
            self.status_label.set_listening_state(True)
            threading.Thread(target=self.update_gui, daemon=True).start()
        except Exception as e:
            handle_error(AudioError, f"Failed to start listening: {str(e)}")
            self.toggle_button.set_listening_state(False)
            self.status_label.set_listening_state(False)

    @log_error
    def stop_listening(self):
        self.audio_manager.stop_listening()
        self.toggle_button.set_listening_state(False)
        self.status_label.set_listening_state(False)

    def audio_callback(self, in_data, frame_count, time_info, status):
        try:
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.current_rms, self.current_predictions = self.process_audio_data(audio_data)
            return (in_data, pyaudio.paContinue)
        except Exception as e:
            handle_error(AudioError, f"Error in audio callback: {str(e)}")
            return (None, pyaudio.paAbort)

    def process_audio_data(self, audio_data):
        normalized_audio = AudioManager.normalize_audio(audio_data)
        rms = AudioManager.calculate_rms(normalized_audio)
        predictions = self.model.predict(audio_data) if self.model else {}
        return rms, predictions

    @log_error
    def update_gui(self):
        while self.audio_manager.is_listening:
            self.master.after(0, self.update_rms_meter)
            self.master.after(0, self.update_wake_word_indicator)
            time.sleep(Config.RMS_UPDATE_INTERVAL / 1000)

    def update_rms_meter(self):
        if hasattr(self, 'current_rms'):
            self.rms_meter.update_meter(self.current_rms)

    def update_wake_word_indicator(self):
        if hasattr(self, 'current_predictions') and self.current_predictions:
            wake_word = max(self.current_predictions, key=self.current_predictions.get)
            if self.current_predictions[wake_word] > Config.WAKE_WORD_THRESHOLD:
                current_time = time.time()
                if current_time - self.last_wake_word_time > self.wake_word_cooldown and not self.wake_word_active:
                    self.last_wake_word_time = current_time
                    self.wake_word_indicator.set_wake_word(wake_word)
                    self.wake_word_active = True
                    self.wake_word_indicator.blink()
                    self.master.after(2000, self.reset_detection_light)
                    self.trigger_wake_word_action()
            elif self.wake_word_active:
                self.wake_word_active = False
                self.wake_word_indicator.reset()
        else:
            self.wake_word_indicator.reset()

    def reset_detection_light(self):
        if not self.wake_word_active:
            self.wake_word_indicator.reset_color()

    def trigger_wake_word_action(self):
        AudioManager.play_sound("hello.wav")
        print("Wake word detected! Add your custom actions here.")

    @log_error
    def cleanup(self):
        self.audio_manager.cleanup()
        self.master.quit()
        #self.master.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = WakeWordApp(root)
    root.mainloop()