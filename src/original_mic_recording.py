import pyaudio
import wave
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "file.wav"
WAVE_OUTPUT_FILENAME2 = "file2.wav"

pulseID = 0
pulse_monitorID = 0

audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
    if((audio.get_device_info_by_index(i))['name'] == 'pulse'):
        pulseID = i

    if((audio.get_device_info_by_index(i))['name'] == 'pulse_monitor'):
        pulse_monitorID = i

class microphoneThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def record2(self):
        stream2 = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index = pulseID)

        print("recording...")
        frames2 = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data2 = stream2.read(CHUNK)
            frames2.append(data2)
        print("finished recording")
        #print(frames)

        # stop Recording
        stream2.stop_stream()
        stream2.close()
        return frames2 

    def write2(self, frames2):
        waveFile2 = wave.open(WAVE_OUTPUT_FILENAME2, 'wb')
        waveFile2.setnchannels(CHANNELS)
        waveFile2.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile2.setframerate(RATE)
        waveFile2.writeframes(b''.join(frames2))
        waveFile2.close()   

    def run(self):
        self.write2(self.record2())


class musicThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def record1(self):
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index = pulse_monitorID)

        print("recording...")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")
        #print(frames)

        # stop Recording
        stream.stop_stream()
        stream.close()
        return frames

    def write1(self, frames):
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def run(self):
        self.write1(self.record1())



micThread = microphoneThread()
musicThreadThing = musicThread()

micThread.start()
musicThreadThing.start()