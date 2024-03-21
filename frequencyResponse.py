import pyaudio
import os
import struct
import numpy as np
from scipy.fftpack import fft
import time
from halo import Halo


# create a halo spinner
spinner = Halo(text="Loading", spinner="dots")
spinner.start()

# constants
CHUNK = 1024 * 2  # samples per frame
FORMAT = pyaudio.paInt16  # audio format (bytes per sample?)
CHANNELS = 1  # single channel for microphone
RATE = 44100



# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
)



# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
AMPLITUDE_LIMIT = 4096



print("stream started")

# for measuring frame rate
frame_count = 0
start_time = time.time()
os.system("clear")
while True:
    # binary data
    data = stream.read(CHUNK)

    data_np = np.frombuffer(data, dtype="h")

    # compute FFT and update line
    yf = fft(data_np)
    # line_fft.set_ydata(np.abs(yf[0:CHUNK]) / (512 * CHUNK))

    # print("shape of yf",yf[4000])

    # remove the frequency above 20000
    yf[round(20000 * (CHUNK / RATE)) :] = 0

    # print("shape of yf",yf.shape,"first 10",yf[0:10])

    # print the first dominant frequency
    dominant_freq_1 = np.argmax(np.abs(yf[0:CHUNK]) / (512 * CHUNK))
    freqfreq_1_amplitude = np.abs(yf[dominant_freq_1]) / (512 * CHUNK)

    # print the second dominant frequency
    yf[dominant_freq_1 - 3 : dominant_freq_1 + 3] = 0
    dominant_freq_2 = np.argmax(np.abs(yf[0:CHUNK]) / (512 * CHUNK))
    freqfreq_2_amplitude = np.abs(yf[dominant_freq_2]) / (512 * CHUNK)

    # print("second dominant frequency",dominant_freq_1 * (RATE / CHUNK))
    # print the third dominant frequency
    yf[dominant_freq_2 - 3 : dominant_freq_2 + 3] = 0
    dominant_freq_3 = np.argmax(np.abs(yf[0:CHUNK]) / (512 * CHUNK))
    freqfreq_3_amplitude = np.abs(yf[dominant_freq_3]) / (512 * CHUNK)

    # spinner.text = ' frequency 1: ' + str(dominant_freq_1 * RATE / CHUNK) + ' Hz  2: ' + str(dominant_freq_2 * RATE / CHUNK) + ' Hz  3: ' + str(dominant_freq_3 * RATE / CHUNK) + ' Hz'
    spinner.text = (
        " Top 3 frequencies: "
        + str(dominant_freq_1 * RATE / CHUNK)
        + " Hz ("
        + str(freqfreq_1_amplitude)
        + ")  "
        + str(dominant_freq_2 * RATE / CHUNK)
        + " Hz ("
        + str(freqfreq_2_amplitude)
        + ")  "
        + str(dominant_freq_3 * RATE / CHUNK)
        + " Hz ("
        + str(freqfreq_3_amplitude)
        + ")"
    )

    time.sleep(0.01)
