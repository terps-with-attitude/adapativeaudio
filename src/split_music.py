import wave
import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
from scipy.io.wavfile import write

voice = wave.open("mic3.wav", "r")
music = wave.open("music3.wav", "r")

music_frames = music.readframes(160000)
voice_frames = voice.readframes(160000)

# full_e = np.array([])
# full_u = np.array([])
# full_d = np.array([])

# i = 0

# while i < 16: 
# 	music_frames = music.readframes(10000)
# 	voice_frames = voice.readframes(10000)


# 	u = np.fromstring(music_frames, np.int16)
# 	u = np.float64(u)

# 	print(i)

# 	d = np.fromstring(voice_frames, np.int16)
# 	d = np.float64(d)


# 	# Apply adaptive filter
# 	M = 20  # Number of filter taps in adaptive filter
# 	step = 0.1  # Step size
# 	y, e, w = adf.nlms(u, d, M, step, returnCoeffs=True)

# 	full_e = np.concatenate([full_e, e])
# 	full_d = np.concatenate([full_d, d])
# 	full_u = np.concatenate([full_u, u])
# 	i += 1

u = np.fromstring(music_frames, np.int16)
u = np.float64(u)

d = np.fromstring(voice_frames, np.int16)
d = np.float64(d)
# Apply adaptive filter
M = 20  # Number of filter taps in adaptive filter
step = 0.1  # Step size
y, e, w = adf.nlms(u, d, M, step, returnCoeffs=True)

scaled = np.int16(e/np.max(np.abs(e)) * 32767) 
write('splitaudio.wav', 32000, scaled)





# plt.figure()
# plt.title('Music (unaltered)')
# plt.plot(full_u)
# plt.grid()
# plt.xlabel('Samples')

# plt.figure()
# plt.title('Mixed voice and music')
# plt.plot(full_d)
# plt.ylim([-30000, 30000])
# plt.grid()
# plt.xlabel('Samples')

# plt.figure() 
# plt.title('Predicted Voice obtained by LMS Algo.')
# plt.plot(full_e)
# plt.grid()
# plt.ylim([-30000, 30000])
# plt.xlabel('Samples')



#plt.show()


# scaled = np.int16(full_e/np.max(np.abs(full_e)) * 32767)

# write('e.wav', 32000, scaled)

# scaled_d = np.int16(full_d/np.max(np.abs(full_d)) * 32767)

#write('mixedtest.wav', 32000, scaled_d)
