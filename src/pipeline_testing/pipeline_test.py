import pyaudio
import webrtcvad
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()
vad = webrtcvad.Vad(3)

# startcd  Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")


stream.stop_stream()
stream.close()

audio.terminate()


frame_duration = 30  # ms
frame = b'\x00\x00' * (RATE * frame_duration / 1000)


speech_ratio = 0
speech_total = 0

samples =  int(RATE*RECORD_SECONDS/(RATE * frame_duration / 1000))

#print(frames)


for i in range(0, samples):
	sample = ''.join(frames[((RATE * frame_duration / 1000))*i : ((RATE * frame_duration / 1000))*(i+1)])
	print(len(sample))
	speech_exists = vad.is_speech(sample, RATE)
	speech_total = speech_total + speech_exists
	print('Contains speech: %s' % (vad.is_speech(sample, RATE)))

speech_ratio = speech_total/float(samples)


print(speech_ratio)

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()