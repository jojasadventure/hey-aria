import customtkinter as ctk

def create_device_frame(master, device_var, device_options):
    device_frame = ctk.CTkFrame(master)
    device_frame.pack(pady=10)

    device_label = ctk.CTkLabel(device_frame, text="Select Audio Device:")
    device_label.grid(row=0, column=0, padx=10)

    device_dropdown = ctk.CTkComboBox(device_frame, variable=device_var, values=device_options, state="readonly")
    device_dropdown.set(device_options[0] if device_options else "No devices found")
    device_dropdown.grid(row=0, column=1)

    return device_frame

def create_model_frame(master, model_var, model_options, on_model_select):
    model_frame = ctk.CTkFrame(master)
    model_frame.pack(pady=10)

    model_label = ctk.CTkLabel(model_frame, text="Select Model:")
    model_label.grid(row=0, column=0, padx=10)

    model_dropdown = ctk.CTkComboBox(model_frame, variable=model_var, values=model_options, state="readonly", command=on_model_select)
    model_dropdown.set(model_options[0] if model_options else "No models found")
    model_dropdown.grid(row=0, column=1)

    return model_frame

def create_toggle_button(master, text, command):
    return ctk.CTkButton(master, text=text, command=command)

def create_status_label(master, text):
    return ctk.CTkLabel(master, text=text)

def create_detection_light(master):
    return ctk.CTkLabel(master, text="●", font=("Arial", 24), text_color="gray")

def update_toggle_button(button, is_listening):
    button.configure(text="Stop Listening" if is_listening else "Start Listening")

def update_status_label(label, is_listening):
    label.configure(text="Status: Listening" if is_listening else "Status: Not Listening")

def blink_detection_light(light, master):
    light.configure(text_color="green")
    master.after(500, lambda: light.configure(text_color="gray"))