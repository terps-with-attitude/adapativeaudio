import os
import multi_threaded_mic_recording
from change_volume import setup_vol
from analyze import analyze_data
import numpy as np
import threading

setup_vol()

mic_arr = np.array([])
music_arr = np.array([])
data_received = threading.Event()
data_sent = threading.Event()

while True:
	data_sent.clear()
	
	begin_streaming(mic_arr, music_arr, data_received, data_sent)

	data_received.wait()

	new_mic_arr = list(mic_arr)
	new_music_arr = list(music_arr)

	analyze_data(new_music_arr, new_mic_arr)

	data_sent.set()