import pyaudio
import wave

FRAMES_PER_BUFFER = 1600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

#record the audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=FRAMES_PER_BUFFER)

print("* recording")
frames = []

for i in range(0, int(RATE / FRAMES_PER_BUFFER * RECORD_SECONDS)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

print("* done recording")

#save the audio
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)

wf.writeframes(b''.join(frames))

wf.close()

