import numpy as np
import os

def calculate_rms(audio_data):
    """Calculate the Root Mean Square (RMS) of audio data."""
    return np.sqrt(np.mean(np.square(audio_data)))

def normalize_audio(audio_data):
    """Normalize audio data to the range [-1, 1]."""
    return audio_data / np.max(np.abs(audio_data))

def get_model_path(model_name):
    """Get the full path for a given model name."""
    models_dir = "models"  # Assume a models directory in the project root
    return os.path.join(models_dir, f"{model_name}.onnx")

def format_prediction(predictions):
    """Format the prediction results for display."""
    return ", ".join([f"{word}: {score:.2f}" for word, score in predictions.items()])

def is_wake_word_detected(predictions, threshold=0.5):
    """Check if any wake word is detected based on the prediction scores."""
    return any(score > threshold for score in predictions.values())