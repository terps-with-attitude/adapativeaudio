import pyaudio
import webrtcvad
import wave
import numpy as np
import adaptfilt as adf
from scipy.io.wavfile import write
import speech_recognition as sr
from os import path
from change_volume import lower_vol, reset

#CONSTANTS
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1024
RECORD_SECONDS = 5
FRAME_DURATION = 30  # ms


def analyze_data(music_frames, mic_input_frames):    
    full_e = np.array([])
    full_u = np.array([])
    full_d = np.array([])

    for i in range(0, (RATE * FRAME_DURATION) / 10000):
        #print("Stage: " + str(i))

        u = np.fromstring(music_frames[0], dtype = np.int16)
        u = np.float64(np.fromstring(music_frames[0], dtype = np.int16))
       
        d = np.fromstring(mic_input_frames[0], dtype = np.int16)
        d = np.float64(np.fromstring(mic_input_frames[0], dtype = np.int16))
        
      
        
        # Apply adaptive filter
        M = 20  # Number of filter taps in adaptive filter
        step = 0.1  # Step size
        y, e, w = adf.nlms(u, d, M, step, returnCoeffs=True)
        
        full_e = np.concatenate([full_e, e])
        full_d = np.concatenate([full_d, d])
        full_u = np.concatenate([full_u, u])
    
    scaled = np.int16(full_e/np.max(np.abs(full_e)) * 32767) 
    write('splitaudio.wav', 32000, scaled)
    process_split_audio()

def process_split_audio():
    print("Processing voice detection for split audio...")
    
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "splitaudio.wav")
    r = sr.Recognizer()
    
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
    
    try:
        results = r.recognize_google(audio)
        lower_vol()
        print(results)
        
    except sr.UnknownValueError:
        print("Unrecognizable audio.")
        reset()
        
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))