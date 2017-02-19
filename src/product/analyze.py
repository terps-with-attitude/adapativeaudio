import pyaudio
import webrtcvad
import wave
import numpy as np
import time
import adaptfilt as adf
from scipy.io.wavfile import write
import speech_recognition as sr
from os import path
from change_volume import lower_vol, reset
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft, fftfreq
from scipy import signal
import scipy 
import math
import time

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

#CONSTANTS
FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024
RECORD_SECONDS = 5
FRAME_DURATION = 30  # ms

FRAME_RATE = 44100

LENGHTH = 30

TOTAL_FRAMES = FRAME_RATE * LENGHTH

FRAME_OFFSET = 1700

FRAME_RESOLUTION = 1000

FRAME_START = 0

FRAME_END =  5*FRAME_RATE/FRAME_RESOLUTION#((TOTAL_FRAMES-FRAME_OFFSET)/FRAME_RESOLUTION)

AMP_CUTOFF = .02


def analyze_data(music_frames, mic_input_frames):    
    
    full_e = np.array([])

    full_u = np.fromstring(music_frames, np.int16)
    full_u = np.float64(full_u)

    full_v = np.fromstring(mic_input_frames, np.int16)
    full_v = np.float64(full_v)

    full_v /= np.max(np.abs(full_v), axis=0)
    full_u /= np.max(np.abs(full_u), axis=0)

    W_v = fftfreq(full_v.size, d=1.0/FRAME_RATE)
    rft_v = rfft(full_v)
    rft_v[(W_v > 700)] = 0
    rft_v[(W_v < 400)] = 0
    full_v_cut = irfft(rft_v)

    W_u = fftfreq(full_u.size, d=1.0/FRAME_RATE)
    rft_u = rfft(full_u)
    rft_u[(W_u > 700)] = 0
    rft_u[(W_u < 400)] = 0
    full_u_cut = irfft(rft_u)

    full_y = np.array([])

    i = FRAME_START

    while i < FRAME_END: 
        
        u = full_u_cut[FRAME_RESOLUTION*i:FRAME_RESOLUTION*i+FRAME_RESOLUTION]
        

        v = full_v_cut[FRAME_RESOLUTION*i:FRAME_RESOLUTION*i+FRAME_RESOLUTION]

        #print(len(u))

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
    rft_e[(W_e < 400)] = 0
    full_e_cut = irfft(rft_e)

    peak_finder = map(lambda x: abs(x), full_e_cut)
    peak_finder = movingaverage(peak_finder, 5000)

    peak_finder = scipy.ndimage.interpolation.zoom(peak_finder, .1, order = 1)

    peaks =  signal.find_peaks_cwt(peak_finder, np.array([1000,2000,3000,4000,5000]), noise_perc = 75)

    peaks_filtered = np.array(filter(lambda x: peak_finder[x] >= AMP_CUTOFF, peaks))
    
    process_split_audio(peaks_filtered)


def process_split_audio(peaks):
    print("Processing voice detection for split audio...")

    print("# of peaks: ")
    print(len(peaks))

    if(len(peaks) > 2):
        lower_vol()
        

    else:
        reset()