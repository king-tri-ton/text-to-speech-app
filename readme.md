# Text-to-Speech App

This Python script implements a simple Text-to-Speech (TTS) application using the PyQt5 library and the Silero TTS model. The application allows users to enter text, select a speaker, and generate and play audio from the entered text.

![Screenshot_12](https://github.com/king-tri-ton/text-to-speech-app/assets/53092931/558a535b-0194-41e7-8143-76cd10cd4e40)

## Usage

1. **Requirements:**
    - Python
    - PyQt5
    - sounddevice
    - soundfile
    - torch
    - numpy
    - silero-models (can be installed using `torch.hub.load`)

2. **How to Run:**
    ```bash
    python app.py
    ```

3. **Application Features:**
    - Enter text in the provided text box.
    - Choose a speaker from the available options.
    - Click the "Create Audio" button to generate audio from the entered text.
    - Click the "Play Audio" button to listen to the generated audio.
    - Click the "Save Audio" button to save the generated audio as a WAV file.

4. **Note:**
    - The script uses the Silero TTS model, which needs to be downloaded during runtime.
    - The application uses a separate thread to create audio, ensuring the GUI remains responsive during the process.
    - The generated audio can be played using the "Play Audio" button or saved using the "Save Audio" button.

## Dependencies

- PyQt5
- sounddevice
- soundfile
- torch
- numpy
- silero-models

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
