"""
Wake Word Detection App
This script serves as the entry point for the Wake Word Detection application.
It sets up the GUI, initializes the WakeWordApp, and handles command-line arguments.
Usage:
python main.py [--model MODEL_PATH]
Copy--model MODEL_PATH: Optional path to a specific ONNX model file
The application uses customtkinter for the GUI and supports multiple wake word models.
It provides real-time audio processing and wake word detection with visual feedback.
For more information, see the README.md file.
"""

import customtkinter as ctk
import sys
import os
import signal
import argparse
from wake_word_app import WakeWordApp

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

def signal_handler(sig, frame):
    print("\nReceived interrupt signal. Exiting...")
    if 'app' in globals():
        app.cleanup()
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Wake Word Detection App")
    parser.add_argument("--model", type=str, help="Path to the wake word model file (.onnx)")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    root = ctk.CTk()
    global app
    app = WakeWordApp(root, initial_model=args.model)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)

    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()