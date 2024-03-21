import pyaudio
import numpy as np
import librosa
import time
import threading
import queue


# Constants
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paFloat32  # Audio format (floating point)
CHANNELS = 1  # Number of audio channels (1 for mono)
RATE = 44100  # Sampling rate in Hz

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Function to detect onsets and calculate tempo
def detect_tempo(signal):
    # onset_env = librosa.onset.onset_strength(y=signal, sr=RATE)
    
    tempo, bt = librosa.beat.beat_track(onset_envelope=signal, sr=RATE)

    # tempo = str(onset_env)
    return tempo,bt

audioQueue = queue.Queue(maxsize=1)

# Audio streaming function
def audio_stream():
    while True:
        data = stream.read(CHUNK)
        if audioQueue.empty():
            audioQueue.put(data)
        time.sleep(0.01)

# Main tempo detection loop
try:
    threading.Thread(target=audio_stream).start()
    while True:
        if not audioQueue.empty():
            data = audioQueue.get()
            signal = np.frombuffer(data, dtype=np.float32)
            # print(signal)
            tempo,bt = detect_tempo(signal)
            # print tempo and beat time
            print(tempo,bt)
except KeyboardInterrupt:
    pass

# Close audio stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
