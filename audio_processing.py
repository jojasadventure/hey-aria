import numpy as np
import pyaudio

def normalize_audio(audio_data):
    return audio_data.astype(np.float32) / 32768.0

def calculate_rms(audio_data):
    return np.sqrt(np.mean(np.square(audio_data)))

def create_audio_stream(pa, format, channels, rate, input_device_index, frames_per_buffer, callback):
    return pa.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        input_device_index=input_device_index,
        frames_per_buffer=frames_per_buffer,
        stream_callback=callback
    )

def process_audio_data(audio_data, model):
    normalized_audio = normalize_audio(audio_data)
    rms = calculate_rms(normalized_audio)
    predictions = model.predict(normalized_audio)
    return rms, predictions

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