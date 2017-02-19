import pyaudio
import wave
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
WAVE_OUTPUT_FILENAME2 = "file2.wav"

# pulseID = 0
# pulse_monitorID = 0

#audio #= pyaudio.PyAudio()


# for i in range(audio.get_device_count()):
#     if((audio.get_device_info_by_index(i))['name'] == 'pulse'):
#         pulseID = i

#     if((audio.get_device_info_by_index(i))['name'] == 'pulse_monitor'):
#         pulse_monitorID = i


class _Microphone_Thread(threading.Thread):

    def __init__(self, mic_event, music_event, frames2):
        threading.Thread.__init__(self)
        self.mic_event = mic_event
        self.music_event = music_event
        self.frames2 = frames2


    def record2(self):
        stream2 = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index = pulseID)

        print("recording...")
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

            data2 = stream2.read(CHUNK)
            self.frames2.append(data2)

            if(len(self.frames2) == 32000 * 5):
            	self.mic_event.set()
            	print("the mic data is ready to send, now waiting for music")
            	self.music_event.wait()



        print("finished recording")
        #print(frames)

        # stop Recording
        stream2.stop_stream()
        stream2.close()
        return self.frames2 

    def write2(self, frames2):
        waveFile2 = wave.open(WAVE_OUTPUT_FILENAME2, 'wb')
        waveFile2.setnchannels(CHANNELS)
        waveFile2.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile2.setframerate(RATE)
        waveFile2.writeframes(b''.join(frames2))
        waveFile2.close()   

    def run(self):
        self.write2(self.record2())

class _Music_Thread(threading.Thread):


    def __init__(self, mic_event, music_event, frames):
        threading.Thread.__init__(self)
        self.mic_event = mic_event
        self.music_event = music_event
        self.frames = frames

    def record1(self):
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index = pulse_monitorID)

        print("recording...")
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            self.frames.append(data)

            if(len(self.frames) == 32000 * 5):
            	self.music_event.set()
            	print("the music data is ready to send, now waiting for mic")
            	self.mic_event.wait()

        print("finished recording")
        #print(frames)

        # stop Recording
        stream.stop_stream()
        stream.close()
        return self.frames

    def write1(self, frames):
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def run(self):
        self.write1(self.record1())




def begin_streaming():

	global audio, pulse_monitorID, pulseID
	audio = pyaudio.PyAudio()
	mic_frames = []
	music_frames = []

	for i in range(audio.get_device_count()):
	    if((audio.get_device_info_by_index(i))['name'] == 'pulse'):
	        pulseID = i

	    if((audio.get_device_info_by_index(i))['name'] == 'pulse_monitor'):
	        pulse_monitorID = i	

	mic_data_recorded = threading.Event()
	music_data_recorded = threading.Event()

	mic_Thread = _Microphone_Thread(mic_data_recorded, music_data_recorded, mic_frames)
	music_ThreadThing = _Music_Thread(mic_data_recorded, music_data_recorded, music_frames)

	mic_Thread.start()
	music_ThreadThing.start()

	mic_Thread.join()
	music_ThreadThing.join()

	return mic_frames, music_frames

	
begin_streaming()

