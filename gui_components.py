import customtkinter as ctk
from config import Config

class DeviceFrame(ctk.CTkFrame):
    def __init__(self, master, device_var, device_options):
        super().__init__(master)
        self.pack(pady=10)

        device_label = ctk.CTkLabel(self, text="Select Audio Device:")
        device_label.grid(row=0, column=0, padx=10)

        self.device_dropdown = ctk.CTkComboBox(self, variable=device_var, values=device_options, state="readonly")
        self.device_dropdown.set(device_options[0] if device_options else "No devices found")
        self.device_dropdown.grid(row=0, column=1)

class ModelFrame(ctk.CTkFrame):
    def __init__(self, master, model_var, model_options, on_model_select):
        super().__init__(master)
        self.pack(pady=10)

        model_label = ctk.CTkLabel(self, text="Select Model:")
        model_label.grid(row=0, column=0, padx=10)

        self.model_dropdown = ctk.CTkComboBox(self, variable=model_var, values=model_options, state="readonly", command=on_model_select)
        self.model_dropdown.set(model_options[0] if model_options else "No models found")
        self.model_dropdown.grid(row=0, column=1)

class ToggleButton(ctk.CTkButton):
    def __init__(self, master, command):
        super().__init__(master, text="Start Listening", command=command)
        self.pack(pady=10)

    def set_listening_state(self, is_listening):
        self.configure(text="Stop Listening" if is_listening else "Start Listening")

class StatusLabel(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master, text="Status: Not Listening")
        self.pack(pady=5)

    def set_listening_state(self, is_listening):
        self.configure(text="Status: Listening" if is_listening else "Status: Not Listening")

class RMSMeter(ctk.CTkProgressBar):
    def __init__(self, master):
        super().__init__(master, orientation="horizontal", mode="determinate")
        self.pack(pady=10, padx=20, fill="x")

    def update_meter(self, rms):
        scaled_rms = min(rms * Config.RMS_SCALE_FACTOR, 1.0)
        self.set(scaled_rms)

class WakeWordIndicator(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master, text="●", font=("Arial", 24), text_color="gray")
        self.pack(pady=10)

    def set_wake_word(self, wake_word):
        self.configure(text=f"Wake Word: {wake_word}")

    def reset(self):
        self.configure(text="Wake Word: None", text_color="gray")

    def blink(self):
        self.configure(text_color="green")

    def reset_color(self):
        self.configure(text_color="gray")