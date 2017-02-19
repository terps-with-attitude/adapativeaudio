import wave
import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
from scipy.io.wavfile import write
from scipy.fftpack import rfft, irfft, fftfreq
from scipy import signal
import scipy 
import math

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

FRAME_RATE = 44100

LENGHTH = 30

TOTAL_FRAMES = FRAME_RATE * LENGHTH

FRAME_OFFSET = 1700

FRAME_RESOLUTION = 1000

FRAME_START = 0

FRAME_END =  5*FRAME_RATE/FRAME_RESOLUTION#((TOTAL_FRAMES-FRAME_OFFSET)/FRAME_RESOLUTION)

AMP_CUTOFF = .02


voice = wave.open("musicvoice.wav", "r")
music = wave.open("music.wav", "r")

music.readframes(FRAME_OFFSET)

music_frames = music.readframes(TOTAL_FRAMES-FRAME_OFFSET)
voice_frames = voice.readframes(TOTAL_FRAMES-FRAME_OFFSET)

full_e = np.array([])

full_u = np.fromstring(music_frames, np.int16)
full_u = np.float64(full_u)

full_v = np.fromstring(voice_frames, np.int16)
full_v = np.float64(full_v)

full_v /= np.max(np.abs(full_v), axis=0)
full_u /= np.max(np.abs(full_u), axis=0)


W_v = fftfreq(full_v.size, d=1.0/FRAME_RATE)
rft_v = rfft(full_v)
rft_v[(W_v > 700)] = 0
rft_v[(W_v < 300)] = 0
full_v_cut = irfft(rft_v)

W_u = fftfreq(full_u.size, d=1.0/FRAME_RATE)
rft_u = rfft(full_u)
rft_u[(W_u > 700)] = 0
rft_u[(W_u < 300)] = 0
full_u_cut = irfft(rft_u)

full_y = np.array([])



i = FRAME_START

while i < FRAME_END: 
	
	
	

	u = full_u_cut[FRAME_RESOLUTION*i:FRAME_RESOLUTION*i+FRAME_RESOLUTION]

	

	v = full_v_cut[FRAME_RESOLUTION*i:FRAME_RESOLUTION*i+FRAME_RESOLUTION]

	print(len(u))

	# Apply adaptive filter
	M = 20  # Number of filter taps in adaptive filter
	step = 0.0000001  # Step size
	y, e, w = adf.nlms(u, v, M, step, returnCoeffs=True)



	full_e = np.concatenate([full_e, e])
	full_e = np.lib.pad(full_e, (0,M), 'constant', constant_values=0)
	full_y = np.concatenate([full_y, y])
	i += 1



W_e = fftfreq(full_e.size, d=1.0/FRAME_RATE)
rft_e = rfft(full_e)
rft_e[(W_e > 700)] = 0
rft_e[(W_e < 300)] = 0
full_e_cut = irfft(rft_e)
#full_e_cut = map(lambda x: x if np.abs(x)>AMP_CUTOFF else 0, full_e_cut)
#full_e_cut = np.lib.pad(full_e_cut,(0,TOTAL_FRAMES-len(full_e_cut)), 'constant', constant_values=0)
#print(len(full_e)-TOTAL_FRAMES)


peak_finder = map(lambda x: abs(x), full_e_cut)
peak_finder = movingaverage(peak_finder, 5000)



peak_finder = scipy.ndimage.interpolation.zoom(peak_finder, .1, order = 1)

peaks =  signal.find_peaks_cwt(peak_finder, np.array([10000,20000]), noise_perc = 75)

print(len(peaks))

plt.figure()
plt.title('Music (unaltered)')
plt.plot(full_u_cut[FRAME_START*FRAME_RESOLUTION : FRAME_END*FRAME_RESOLUTION])
plt.grid()
plt.xlabel('Samples')

plt.figure()
plt.title('Mixed voice and music')
plt.plot(full_u_cut[FRAME_START*FRAME_RESOLUTION : FRAME_END*FRAME_RESOLUTION])
plt.plot(full_v_cut[FRAME_START*FRAME_RESOLUTION : FRAME_END*FRAME_RESOLUTION])
#plt.plot(full_u_cut[FRAME_START*FRAME_RESOLUTION : FRAME_END*FRAME_RESOLUTION])
#plt.ylim([-30000, 30000])
plt.grid()
plt.xlabel('Samples')

plt.figure() 
plt.title('Predicted Voice obtained by LMS Algo.')
plt.plot(full_e_cut)
plt.grid()
#plt.ylim([-30000, 30000])
plt.xlabel('Samples')


plt.figure()
plt.plot(peak_finder)
plt.grid()


plt.show()

out = full_e_cut

scaled = np.int16(out/np.abs(np.max(out)) * 32767)

write('e.wav', 44100, scaled)

scaled_v = np.int16(full_v_cut/np.abs(np.max(full_v_cut)) * 32767)

write('mixedtest.wav', 44100, scaled_v)
