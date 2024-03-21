import pyaudio
import wave
from matplotlib import pyplot as plt
import numpy as np
import time
import librosa
from tkinter import TclError

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
# plt.show()
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Signal')
ax1.set_xlim(0, 2 * FRAMES_PER_BUFFER)
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax2.set_xlim(0, 2 * FRAMES_PER_BUFFER)
ax2.set_ylim(-10, 10)
plt.setp(ax1, xticks=[0, FRAMES_PER_BUFFER, 2 * FRAMES_PER_BUFFER], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])
times = np.linspace(0, FRAMES_PER_BUFFER, num=FRAMES_PER_BUFFER)
line, = ax1.plot(x, np.random.rand(FRAMES_PER_BUFFER), '-', c= "r")
line2, = ax2.plot(x, np.random.rand(FRAMES_PER_BUFFER), '-', c = "b")
while True:
    data = stream.read(FRAMES_PER_BUFFER,False)
    signal_array = np.frombuffer(data, dtype='h')
    #find onset in the data




    #create a marker for the onset


    

    line.set_ydata(np.abs(signal_array))

    #plot the meanline
    # line2.set_ydata(meanLine)
    

    # fig.canvas.draw()
    # fig.canvas.flush_events()
    time.sleep(0.001)
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        
    except TclError:
        
        # calculate average frame rate
        # frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
    




    