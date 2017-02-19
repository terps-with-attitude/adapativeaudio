import os
import wave
import pyaudio
import sys
import time
from multi_threaded_mic_recording import begin_streaming
from change_volume import setup_vol, setup_vol_floor
from analyze import analyze_data
import numpy as np
import threading

setup_vol()
setup_vol_floor(30)

mic_arr = []
music_arr = []
data_ready = threading.Event()
data_sent = threading.Event()

data_streaming = threading.Thread(
        target=begin_streaming, args=(mic_arr, music_arr, data_ready, data_sent,))
data_streaming.start()

audio = pyaudio.PyAudio()

while True:
	firstTime = time.mktime(time.gmtime())

	data_sent.clear()
	
	data_ready.wait()

	new_mic_arr = mic_arr
	new_music_arr = music_arr


	waveFile = wave.open("mic.wav", 'wb')
	waveFile.setnchannels(1)
	waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
	waveFile.setframerate(44100)
	waveFile.writeframes(b''.join(new_mic_arr))
	waveFile.close()

	waveFile2 = wave.open("music.wav", 'wb')
	waveFile2.setnchannels(1)
	waveFile2.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
	waveFile2.setframerate(44100)
	waveFile2.writeframes(b''.join(new_music_arr))
	waveFile2.close()

	mic_frames = wave.open("mic.wav", 'r')
	music_frames = wave.open("music.wav", 'r')

	


	analysis_stream = threading.Thread(
		target = analyze_data, args = (music_frames.readframes(220500), mic_frames.readframes(220500)))

	analysis_stream.start()
	#analyze_data(mic_frames.readframes(220500), music_frames.readframes(220500))
	
	mic_frames.close()
	music_frames.close()

	del mic_arr[:]
	del music_arr[:]


	data_sent.set()
	time.sleep(.03)

	secondTime = time.mktime(time.gmtime())
	print("it took seconds")
	print(secondTime - firstTime)
		
