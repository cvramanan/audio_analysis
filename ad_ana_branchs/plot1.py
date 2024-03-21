import pyaudio
import wave
from matplotlib import pyplot as plt
import numpy as np
import time

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


t_audio = 1


AMPLITUDE_LIMIT = 4096
#variable for plotting
x = np.arange(0, 2 * FRAMES_PER_BUFFER, 2)       # samples (waveform)
# xf = np.linspace(0, RATE, FRAMES_PER_BUFFER)     # frequencies (spectrum)
# create a line object with random data
line, = ax1.plot(x, np.random.rand(FRAMES_PER_BUFFER), '-', lw=2)





#plot a graph with matplotlib
plt.show(block=False)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Signal')
ax1.set_xlim(0, 2 * FRAMES_PER_BUFFER)
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
plt.setp(ax1, xticks=[0, FRAMES_PER_BUFFER, 2 * FRAMES_PER_BUFFER], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])
times = np.linspace(0, FRAMES_PER_BUFFER, num=FRAMES_PER_BUFFER)
line, = ax1.plot(x, np.random.rand(FRAMES_PER_BUFFER), '-', lw=2)
while True:
    data = stream.read(FRAMES_PER_BUFFER)
    signal_array = np.frombuffer(data, dtype='h')
    # print("size of signal_array: ", len(signal_array))
    #mean of signal_array
    # print("mean of signal_array: ", np.mean(signal_array))
    # exit()
    # print("signal_array: ", signal_array[:1000])
    # exit()
    
    # ax1.plot(times, signal_array, color='b')
    line.set_ydata(np.abs(signal_array))
    

    fig.canvas.draw()
    fig.canvas.flush_events()
    # time.sleep(0.1)
    
    




    