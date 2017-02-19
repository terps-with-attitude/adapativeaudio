import pyaudio
import wave
import threading
import traceback
import sys
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1000
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "file3.wav"
WAVE_OUTPUT_FILENAME2 = "file2.wav"

pulseID = 0
pulse_monitorID = 0

audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
	if((audio.get_device_info_by_index(i))['name'] == 'pulse'):
	 	pulseID = i

	if((audio.get_device_info_by_index(i))['name'] == 'pulse_monitor'):
	 	pulse_monitorID = i



class micThread (threading.Thread):

	def __init__(self, threadID, threadName):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.threadName = threadName
		#audio1 = audio

	def run(self):
		pass

		#audio1 = pyaudio.PyAudio()

		# print("mic thread started")
		

		# stream = audio.open(format=FORMAT, channels=CHANNELS,
  #               rate=RATE, input=True,
  #               frames_per_buffer=CHUNK,
  #               input_device_index = pulseID)

		# print("recording mic...")

		# frames = []
		# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		# 	data = stream.read(CHUNK)
	 #    	frames.append(data)

		# print("finished recording mic")

	 #   	stream.stop_stream()
		# stream.close()


		

		# waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		# waveFile.setnchannels(CHANNELS)
		# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
		# waveFile.setframerate(RATE)
		# waveFile.writeframes(b''.join(frames))
		# waveFile.close()

		# print("Everything ran just fine in mic")

		


class musicThread (threading.Thread):

	def __init__(self, threadID, threadName):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.threadName = threadName
		#audio2 = audio
	
	def run(self):

		#audio2 = pyaudio.PyAudio()

		print("music thread started")
		

		stream2 = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, 
							frames_per_buffer=CHUNK, 
							input_device_index = pulse_monitorID)

		print("recording music...")

		frames2 = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data2 = stream2.read(CHUNK)
			frames2.append(data2)

		print("finished recording  music")

		stream2.stop_stream()
		stream2.close()

		waveFile2 = wave.open(WAVE_OUTPUT_FILENAME2, 'wb')
		waveFile2.setnchannels(CHANNELS)
		waveFile2.setsampwidth(audio.get_sample_size(FORMAT))
		waveFile2.setframerate(RATE)
		waveFile2.writeframes(b''.join(frames2))
		waveFile2.close()

		


def recordMic():
	print("mic thread started")
	

	stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            frames_per_buffer=CHUNK,
            input_device_index = 4)

	print("recording mic...")

	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
    	frames.append(data)

	print("finished recording mic")

   	stream.stop_stream()
	stream.close()


	

	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

	print("Everything ran just fine in mic")


recordMic()

music_thread = musicThread(1, "musicThread")
#mic_thread = micThread(2, "micThread")


#mic_thread.start()
music_thread.start()

#mic_thread.join()
music_thread.join()



audio.terminate()