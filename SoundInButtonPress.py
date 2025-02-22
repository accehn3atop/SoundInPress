import pyaudio
import numpy as np
import pynput.keyboard as keyboard

# Parameters for sound capture
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 250  # Threshold for sound detection
KEY_TO_PRESS = 'w'  # Key to press

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the stream for sound capture
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Initialize the keyboard controller
keyboard_controller = keyboard.Controller()

def listen_and_press_key():
    print("Listening to sound...")
    try:
        while True:
            # Read data from the stream
            data = stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Check the sound level
            if np.abs(audio_data).mean() > THRESHOLD:
                print("Sound detected! Pressing the key...")
                keyboard_controller.press(KEY_TO_PRESS)
                keyboard_controller.release(KEY_TO_PRESS)

    except KeyboardInterrupt:
        print("Stopping the program...")

    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    listen_and_press_key()