import wave
import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
from scipy.io.wavfile import write

voice = wave.open("voice.wav", "r")
music = wave.open("music.wav", "r")



music.readframes(900000)

music_frames = music.readframes(80000)
voice_frames = voice.readframes(160000)


u = np.fromstring(music_frames, np.int16)
u = np.float64(u)


v= np.fromstring(voice_frames, np.int16)
v = np.float64(v)

d = u+v


# Apply adaptive filter
M = 10  # Number of filter taps in adaptive filter
step = 0.0001  # Step size
y, e, w = adf.nlms(u, d, M, step, returnCoeffs=True)
#
#plt.figure()
#plt.title('u(n)')
#plt.plot(u)
#plt.grid()
#plt.xlabel('Samples')
#
#plt.figure()
#plt.title('v(n)')
#plt.plot(v)
#plt.ylim([-5500, 5000])
#plt.grid()
#plt.xlabel('Samples')
#
#plt.figure()
#plt.title('e (n)')
#plt.plot(e)
#plt.grid()
#plt.ylim([-5500, 5000])
#plt.xlabel('Samples')
#
#
#
#plt.show()


scaled = np.int16(e/np.max(np.abs(e)) * 32767)

write('test.wav', 32000, scaled)

scaled_u = np.int16(u/np.max(np.abs(u)) * 32767)

write('new_musc.wav', 64000, scaled_u)
