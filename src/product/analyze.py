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
    rft_v[(W_v > 255)] = 0
    rft_v[(W_v < 85)] = 0
    full_v_cut = irfft(rft_v)

    W_u = fftfreq(full_u.size, d=1.0/FRAME_RATE)
    rft_u = rfft(full_u)
    rft_u[(W_u > 255)] = 0
    rft_u[(W_u < 85)] = 0
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
    rft_e[(W_e > 255)] = 0
    rft_e[(W_e < 85)] = 0
    full_e_cut = irfft(rft_e)

    peak_finder = map(lambda x: abs(x), full_e_cut)
    peak_finder = movingaverage(peak_finder, 5000)



    peak_finder = scipy.ndimage.interpolation.zoom(peak_finder, .1, order = 1)
    plt.figure()
    plt.plot(full_v_cut)
    plt.grid()


    plt.figure()
    plt.plot(full_e_cut)
    plt.grid()

    plt.figure()
    plt.plot(peak_finder)
    plt.title('Voice detection peaks')
    plt.grid()

    plt.show()
    peaks =  signal.find_peaks_cwt(peak_finder, np.array([1000,2000,3000,4000,5000]), noise_perc = 75)

    
    process_split_audio(peaks)

def process_split_audio(peaks):
    print("Processing voice detection for split audio...")
    # GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
    # "type": "service_account",
    # "project_id": "my-project-1478361491618",
    # "private_key_id": "93edfcefc3766a686a5359a04e5e6800471cbc6f",
    # "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDMce1Ua4ZQKRMf\nlXCzlBzt8gvr/CsvzmooQwm6oYII9nYDKEx0LHQ5aE/HKQonTrjtTwkRxTT+f3CP\nYkLuCCmPhmBD+BiaHj2Tias5PT2D1SfxY9ZL/UlRfQA6QCp/CX2JCTuUMGraTlR4\nBvoMfDY3y8P4TK0LxxCKq8g7DcpIcLJhICZPavORSXu72vOVBsN4DdG2+VjuLkDR\nQ6tFntC3eyxuZNerEPlXGTWg/gMnTyOIAgqNnarh19QXTcfG2ovEFN0KQ2Eg9ZUC\neVXVQoPHDkrBnlim4MlWhnWr04URZ+uM8fXRPVRKa+Flb+clorT4ROM8CXQWpGcb\nlelPToCjAgMBAAECggEAVwz3ceeqs/0ZUGxwJXaebs6ONvgTZ3KrjuMkhFv6o1hV\n3XhOPXUkM8FvnqyhzyTc5uatROzEaMzYn6TGPNYq5BriaG5+Azl3HJgU2PVzeOvM\n6yKIf6ikjFb+Ps9NiPQAiNXukWWgSb3qh4To+WH2MAHKOrJjSE2FhJYqVsLDa94V\nsEFZpKVJ0n1AQIckqFMk8h/AIF8t9EW/2Feutpg0HHpPk6fckjZ+KfL38hAhaoNZ\npAFU973ZU+xKvAkj0hndy7sJWfPUDEIoyfX1iY+59bkybN4qmEdgsmBVup+vqiMe\nGXwbmRuehC71764U2Fu5nsiz7CHn7wDTNT6Q6TDGuQKBgQDnTTXT6qOw2i4f00ns\nmvVRZqNFRb5CG+GkYtCVulcct/5rG0cL324sguYqUygAoc6wpRZRO/8h5nbsrEpZ\nn5KKYfKM9pOTCTADHb1pmuA4M7oU98ES6pYFwK4cgZIMR4Ug9xwYDa7O5zgbU6K9\nKVhkIkLUM81P5EDoeFl2fOwlFQKBgQDiRpLeAN15x5B3oAYyFxsKAUzgrTwrLv7z\nxFTfrAEjuMCF2/Xu25RpbxUg9qoBzM3ZJ5tOFV3Bx7krhc12CBxnBDQCN6gB1VT1\ndSc57UrlkzVPjsKXGHHo3Ioe63lwjU/lNjs/SAbsgUB4KtiixnrKke8irzGeREVd\niYq4Mpzs1wKBgQCKM5Hz+wCvTM2+akqDOttVNdRcMZ3KdkpOJFSpAdvG5xD3Aidj\nKq7znYrUwzblmcibtygshYKdyMxKAW+zOSsf0AJSw4nNkvHDCuP/03AhZJbMrHQK\nT2wwJ75gffK7r4gV+FAq9xH5wiG+Aiz8hVWxDt+LVyBXmfRGcpJRv7aBOQKBgQCp\nz6rinqWXgdQCYn6j0sFBBe7K4lc4VUGScTH81hnY1Arvqj5rrjA329xwa4z0Yt3M\n7TNZKyG8joWBix3BSZ7/FKFvVJNqJM5oky4IA/PkTFCCzzFrsTWzOucRA0iU1ggy\njTtzZzuC/BEE3arMpcV7Bn//eJj1HGkuJE2NpLYt6wKBgQDFFMC3zlFw3HShuaho\nwSKL90W32RjGGn2naKZEs5s0cBk8fvn3WquNKgCsKCD6DKxaIz38D5m0vnTaWbun\nzCnkOUeDtuoCwJFUapfqlRFBSZp5p+xZuk0jv93JUuqZxrv7k701seCtSkd+pB48\nZW6lOkYa13b6I2X4/KvRxrcRrA==\n-----END PRIVATE KEY-----\n",
    # "client_email": "adaptiveaudio@my-project-1478361491618.iam.gserviceaccount.com",
    # "client_id": "109715588347315681415",
    # "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    # "token_uri": "https://accounts.google.com/o/oauth2/token",
    # "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    # "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/adaptiveaudio%40my-project-1478361491618.iam.gserviceaccount.com"
    # }"""

    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "splitaudio.wav")
    # r = sr.Recognizer()
    
    # with sr.AudioFile(AUDIO_FILE) as source:
    #     audio = r.record(source)
    
    # try:
    #     results =  r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    #     lower_vol()
    #     print(results)
        
    # except sr.UnknownValueError:
    #     print("Unrecognizable audio.")
    #     reset()
        
    # except sr.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
    


    print("# of peaks: ")
    print(len(peaks))
    if(len(peaks) > 1):
        #lower_vol()
        pass

    else:
        #reset()
        pass

