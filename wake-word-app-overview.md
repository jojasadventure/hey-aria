# Wake Word Detection App: Comprehensive Overview

## 1. Project Structure

The Wake Word Detection app is a modular Python application with the following file structure:

```
wake_word_app/
│
├── main.py
├── wake_word_app.py
├── model.py
├── audio_processing.py
├── gui_utils.py
├── config.py
├── error_handler.py
├── app_utils.py
│
└── models/
    ├── alexa.onnx
    └── eugene.onnx
```

## 2. Component Overview

### 2.1 main.py
- Entry point of the application
- Initializes the GUI and WakeWordApp
- Handles command-line arguments and signal interrupts

### 2.2 wake_word_app.py
- Contains the WakeWordApp class, which is the core of the application
- Manages the GUI, audio processing, and model interaction
- Handles user interactions and real-time updates

### 2.3 model.py
- Defines the Model and AudioFeatures classes for wake word detection
- Manages ONNX model loading and inference
- Handles audio feature extraction and preprocessing

### 2.4 audio_processing.py
- Contains functions for audio normalization, RMS calculation, and device listing
- Manages PyAudio stream creation and callback

### 2.5 gui_utils.py
- Provides utility functions for creating GUI elements
- Includes functions for updating GUI components

### 2.6 config.py
- Stores configuration constants for the application
- Includes audio settings, GUI settings, and model options

### 2.7 error_handler.py
- Defines custom exception classes
- Provides logging and error handling utilities

### 2.8 app_utils.py
- Contains utility functions used across the application
- Includes audio processing and prediction formatting functions

## 3. Key Classes and Their Relationships

### 3.1 WakeWordApp (wake_word_app.py)
- Main application class
- Relationships:
  - Uses Model for wake word detection
  - Uses PyAudio for audio input
  - Uses Config for application settings
  - Uses error_handler for logging and error management

### 3.2 Model (model.py)
- Handles wake word model loading and inference
- Relationships:
  - Contains AudioFeatures for audio preprocessing
  - Uses onnxruntime for model inference
  - Uses error_handler for logging and error management

### 3.3 AudioFeatures (model.py)
- Manages audio feature extraction and preprocessing
- Relationships:
  - Uses onnxruntime for melspectrogram and embedding model inference

### 3.4 Config (config.py)
- Stores application-wide configuration
- Relationships:
  - Used by WakeWordApp and other components for settings

## 4. Key Methods and Their Functions

### 4.1 WakeWordApp Methods

#### 4.1.1 __init__(self, master, initial_model=None)
- Initializes the application
- Sets up the GUI
- Loads the initial wake word model

#### 4.1.2 setup_gui(self)
- Creates and arranges GUI elements

#### 4.1.3 toggle_listening(self)
- Starts or stops the audio listening process

#### 4.1.4 start_listening(self)
- Initializes PyAudio stream
- Starts audio processing thread

#### 4.1.5 audio_callback(self, in_data, frame_count, time_info, status)
- Processes incoming audio data
- Calls model for predictions

#### 4.1.6 process_audio_data(self, audio_data)
- Normalizes audio
- Calculates RMS
- Gets predictions from the model

#### 4.1.7 update_gui(self)
- Updates GUI elements in real-time
- Called in a separate thread

### 4.2 Model Methods

#### 4.2.1 __init__(self, wakeword_models: List[str], ...)
- Initializes the wake word model
- Sets up ONNX runtime session

#### 4.2.2 predict(self, x: np.ndarray, ...)
- Performs wake word detection on input audio
- Returns prediction scores

### 4.3 AudioFeatures Methods

#### 4.3.1 __init__(self, melspec_model_path: str, ...)
- Initializes audio feature extraction models

#### 4.3.2 _get_melspectrogram(self, x: Union[np.ndarray, List], ...)
- Generates mel spectrogram from audio input

#### 4.3.3 _get_embeddings(self, x: np.ndarray, ...)
- Extracts audio embeddings from mel spectrogram

#### 4.3.4 _streaming_features(self, x)
- Processes incoming audio data in a streaming fashion

## 5. Data Flow

1. Audio input is captured via PyAudio in `WakeWordApp.audio_callback`
2. Audio data is processed in `WakeWordApp.process_audio_data`
3. Processed audio is passed to `Model.predict`
4. `Model.predict` uses `AudioFeatures` for preprocessing
5. Prediction results are returned to `WakeWordApp`
6. GUI is updated with results in `WakeWordApp.update_gui`

## 6. Error Handling and Logging

- Custom exceptions (ModelError, AudioError) are defined in `error_handler.py`
- `@log_error` decorator is used on methods to catch and log exceptions
- `handle_error` function is called to process specific error types
- Logging is configured to write to both file and console

## 7. Configuration

The `Config` class in `config.py` contains various settings:

- Audio settings (CHUNK, FORMAT, CHANNELS, RATE)
- Wake word detection settings (WAKE_WORD_THRESHOLD)
- GUI settings (WINDOW_SIZE, WINDOW_TITLE)
- RMS meter settings (RMS_UPDATE_INTERVAL, RMS_SCALE_FACTOR)
- Model settings (DEFAULT_MODEL, MODEL_OPTIONS)

## 8. GUI Components

The app uses the customtkinter library for GUI elements, including:

- Device selection dropdown
- Model selection dropdown
- Toggle button for starting/stopping listening
- Status label
- RMS meter (progress bar)
- Wake word indicator

## 9. Audio Processing

- Uses PyAudio for audio input
- Normalizes audio data to float32 in range [-1, 1]
- Calculates RMS (Root Mean Square) of audio data
- Uses ONNX models for melspectrogram generation and embedding extraction

## 10. Model Handling

- Supports multiple wake word models (e.g., "alexa", "eugene")
- Models are stored as .onnx files in the 'models' directory
- Uses ONNX Runtime for model inference
- Supports both CPU and GPU inference (if available)

## 11. Refactoring Guidelines

When refactoring this application, consider the following:

1. Maintain modular structure: Keep related functionality in appropriate files.
2. Update imports: If moving functions/classes, update imports across all files.
3. Preserve method signatures: Changing method parameters may affect multiple components.
4. Test thoroughly: Each component interacts with others, so test after each change.
5. Update Config: If adding new settings, add them to the Config class.
6. Error handling: Use custom exceptions and logging consistently.
7. GUI updates: Ensure GUI-related code remains in wake_word_app.py or gui_utils.py.
8. Model changes: If modifying the Model or AudioFeatures classes, ensure compatibility with existing audio processing pipeline.
9. Threading: Be cautious when modifying threaded operations (e.g., audio processing, GUI updates).

## 12. Potential Improvements

1. Add support for training new wake word models
2. Implement a more sophisticated audio preprocessing pipeline
3. Add visualization of audio features or model predictions
4. Improve error handling and user feedback for model loading and audio device issues
5. Implement a plugin system for easy addition of new wake word models or audio processing techniques
6. Add unit tests and integration tests for core components
7. Optimize performance for low-power devices

This overview provides a comprehensive guide to the Wake Word Detection app's structure, components, and functionality. It should serve as a valuable resource for future development and maintenance of the application.
