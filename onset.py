import pyaudio
import wave
from matplotlib import pyplot as plt
import numpy as np
import time
import librosa

#create a chart
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

FRAMES_PER_BUFFER = 1024 * 2 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

#record the audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=FRAMES_PER_BUFFER)

AMPLITUDE_LIMIT = 4096
#variable for plotting
x = np.arange(0, 2 * FRAMES_PER_BUFFER, 2)       # samples (waveform)
# xf = np.linspace(0, RATE, FRAMES_PER_BUFFER)     # frequencies (spectrum)
# create a line object with random data

#plot a graph with matplotlib
plt.show(block=False)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Signal')
ax1.set_xlim(0, 2 * FRAMES_PER_BUFFER)
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax2.set_xlim(0, 2 * FRAMES_PER_BUFFER)
ax2.set_ylim(-10, 10)
plt.setp(ax1, xticks=[0, FRAMES_PER_BUFFER, 2 * FRAMES_PER_BUFFER], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])
times = np.linspace(0, FRAMES_PER_BUFFER, num=FRAMES_PER_BUFFER)
line, = ax1.plot(x, np.random.rand(FRAMES_PER_BUFFER), '-', c="r")
line2, = ax2.plot(x, np.random.rand(FRAMES_PER_BUFFER), '-', c="b")

# Parameters for onset detection
FRAME_SIZE = 2048
HOP_SIZE = 512
THRESHOLD = 0.2

while True:
    data = stream.read(FRAMES_PER_BUFFER)
    signal_array = np.frombuffer(data, dtype='h')

    # Compute onset detection function using librosa
    onset_env = librosa.onset.onset_strength(y=signal_array.astype(float), sr=RATE,
                                              hop_length=HOP_SIZE, n_fft=FRAME_SIZE)

    # Find onsets
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=RATE, hop_length=HOP_SIZE,
                                         backtrack=False, pre_max=20, post_max=20,
                                         pre_avg=100, post_avg=100, delta=0.2, wait=0)

    # Create marker for onsets
    for onset in onsets:
        ax1.axvline(x=onset * HOP_SIZE / RATE, color='g', linestyle='--')

    line.set_ydata(np.abs(signal_array))

    fig.canvas.draw()
    fig.canvas.flush_events()
