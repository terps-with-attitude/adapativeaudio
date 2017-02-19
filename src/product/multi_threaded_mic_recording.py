import pyaudio
import wave
import threading
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
WAVE_OUTPUT_FILENAME2 = "file2.wav"


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

    def run(self):
        self.record2()

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


    def run(self):
        self.record1()




def begin_streaming(mic_arr, music_arr, data_ready, data_sent):

	global audio, pulse_monitorID, pulseID
	audio = pyaudio.PyAudio()

	for i in range(audio.get_device_count()):
	    if((audio.get_device_info_by_index(i))['name'] == 'pulse'):
	        pulseID = i

	    if((audio.get_device_info_by_index(i))['name'] == 'pulse_monitor'):
	        pulse_monitorID = i	

		mic_data_recorded = threading.Event()
		music_data_recorded = threading.Event()

	while True:

		data_ready.clear()

		mic_Thread = _Microphone_Thread(mic_data_recorded, music_data_recorded, mic_arr)
		music_ThreadThing = _Music_Thread(mic_data_recorded, music_data_recorded, music_arr)

		mic_Thread.start()
		music_ThreadThing.start()

		mic_Thread.join()
		music_ThreadThing.join()

		data_ready.set()
		data_sent.wait()

	

	
begin_streaming()

