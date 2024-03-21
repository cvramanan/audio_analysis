import wave
from matplotlib import pyplot as plt
import numpy as np
import librosa

#create a chart
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

# Load the MP3 file
file_path = "your_input_file.mp3"
y, sr = librosa.load(file_path, sr=None)

# Constants for processing
FRAME_SIZE = 2048
HOP_SIZE = 512

AMPLITUDE_LIMIT = max(abs(y))
x = np.arange(0, len(y))  # samples

# Plot the waveform
plt.show(block=False)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Signal')
ax1.set_xlim(0, len(y))
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax2.set_xlim(0, len(y))
ax2.set_ylim(-10, 10)
plt.setp(ax1, xticks=[0, len(y)], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])
line, = ax1.plot(x, y, '-', c="r")
line2, = ax2.plot(x, np.random.rand(len(y)), '-', c="b")

# Compute onset detection function using librosa
onset_env = librosa.onset.onset_strength(y=y.astype(float), sr=sr,
                                          hop_length=HOP_SIZE, n_fft=FRAME_SIZE)

# Find onsets
onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, hop_length=HOP_SIZE,
                                     backtrack=False, pre_max=20, post_max=20,
                                     pre_avg=100, post_avg=100, delta=0.2, wait=0)

# Plot detected onsets
for onset in onsets:
    ax1.axvline(x=onset * HOP_SIZE / sr, color='g', linestyle='--')

# Update the plot
fig.canvas.draw()
fig.canvas.flush_events()

plt.show()