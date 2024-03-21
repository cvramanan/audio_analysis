import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
import time
import threading
import librosa

# Constants
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100  # Sampling rate in Hz

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Function to compute spectral flux
def compute_spectral_flux(audio_data, prev_spectrum):
    # Compute magnitude spectrum
    spectrum = np.abs(np.fft.fft(audio_data))
    
    # Compute spectral flux
    spectral_flux = np.sum((spectrum - prev_spectrum) ** 2)
    
    return spectrum, spectral_flux

# Initialize previous spectrum
prev_spectrum = None

# Plotting variables
x_values = []
y_values = []

# Create a new plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlabel('Time')
ax.set_ylabel('Spectral Flux')


audioQueue = Queue(maxsize=1)
def liveStream(stream):
    while True:
        data = stream.read(CHUNK,False)
        
        if audioQueue.empty() == True:
            audioQueue.put(data)
        time.sleep(0.01)


threading.Thread(target=liveStream, args=(stream,)).start()

# Main loop
xiter = 0
timer = time.time()
try:
    while True:
        # Read audio data from the stream
        # data = stream.read(CHUNK,False)
        if audioQueue.empty() == False:
            data = audioQueue.get()
        
            # Convert binary data to numpy array
            audio_data = np.frombuffer(data, dtype=np.float16)
            
            # Initialize spectral flux to 0 if it's the first frame
            if prev_spectrum is None:
                prev_spectrum = np.abs(np.fft.fft(audio_data))
                continue
            
            # Compute spectral flux
            # spectrum, spectral_flux = compute_spectral_flux(audio_data, prev_spectrum)
            
            prev_spectrum[np.isnan(prev_spectrum)] = 0

            onset_env = librosa.onset.onset_strength(y=prev_spectrum, sr=RATE)
            print(onset_env)
            #find the nan values
            
            # exit()

            # Update previous spectrum
            # prev_spectrum = spectrum
            
            # Append time and spectral flux values for plotting
            x_values.append(xiter)
            xiter += 1
            # y_values.append(spectral_flux)
            y_values.append(onset_env)
            
            # Update plot
            line.set_xdata(x_values)
            line.set_ydata(y_values)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()

            if len(x_values) > 250:
                x_values.pop(0)
                y_values.pop(0)
                print("Time taken: ", time.time() - timer)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

# Close audio stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
