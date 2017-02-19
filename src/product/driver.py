import os
import wave
import pyaudio
import sys
from multi_threaded_mic_recording import begin_streaming
from change_volume import setup_vol
from analyze import analyze_data
import numpy as np
import threading

setup_vol()

mic_arr = []
music_arr = []
data_ready = threading.Event()
data_sent = threading.Event()

data_streaming = threading.Thread(
        target=begin_streaming, args=(mic_arr, music_arr, data_ready, data_sent,))
data_streaming.start()

audio = pyaudio.PyAudio()

for x in range (0,3):
	data_sent.clear()
	
	data_ready.wait()

	new_mic_arr = mic_arr
	new_music_arr = music_arr

	print("current iteration is ", x)

	print("this is mic")
	print(mic_arr)
	print("this is music")
	print(music_arr)

	waveFile = wave.open("mic" + str(x) + ".wav", 'wb')
	waveFile.setnchannels(1)
	waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
	waveFile.setframerate(32000)
	waveFile.writeframes(b''.join(new_mic_arr))
	waveFile.close()

	waveFile2 = wave.open("music" + str(x) +".wav", 'wb')
	waveFile2.setnchannels(1)
	waveFile2.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
	waveFile2.setframerate(32000)
	waveFile2.writeframes(b''.join(new_music_arr))
	waveFile2.close()

	#analyze_data(new_music_arr, new_mic_arr)

	del mic_arr[:]
	del music_arr[:]


	data_sent.set()

	if(x == 2):
		print("**********THIS IS THE LAST ONE******")
		
