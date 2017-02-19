import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
WAVE_OUTPUT_FILENAME2 = "file2.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
#stream2 = audio.open(format=FORMAT, channels=CHANNELS,
                #rate=RATE, input=True,
                #frames_per_buffer=CHUNK)

print("recording...")
frames = []
#frames2 = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #data2 = stream2.read(CHUNK)
    frames.append(data)
    #frames2.append(data2)
print("finished recording")
#print(frames)

# stop Recording
stream.stop_stream()
stream.close()
#stream2.stop_stream()
#stream2.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

#waveFile2 = wave.open(WAVE_OUTPUT_FILENAME2, 'wb')
#waveFile2.setnchannels(CHANNELS)
#waveFile2.setsampwidth(audio.get_sample_size(FORMAT))
#waveFile2.setframerate(RATE)
#waveFile2.writeframes(b''.join(frames2))
#waveFile2.close()