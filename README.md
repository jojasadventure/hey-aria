# Wake Word Detection App

A Python application for real-time wake word detection using customizable ONNX models.

Made possible by the library for https://github.com/sujitvasanth/openwakeword-simplified

Note: Experimental, just for myself, no requirements.txt file at this time, only ran on intel mac from 2015 ( - ; 

## Features

- Real-time audio processing
- Customizable wake word models (ONNX format)
- User-friendly GUI built with customtkinter
- Support for multiple audio devices
- Visual feedback with RMS meter and wake word indicator

## Requirements

- Python 3.7+
- PyAudio
- NumPy
- ONNX Runtime
- customtkinter

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/wake-word-detection-app.git
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```
python main.py
```

Select an audio device and model from the dropdowns, then click "Start Listening" to begin wake word detection.

## Adding Custom Models

Place your custom ONNX models in the `models/` directory. They will automatically appear in the model selection dropdown.

## License

[MIT License](LICENSE)
