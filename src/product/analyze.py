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

#CONSTANTS
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1024
RECORD_SECONDS = 5
FRAME_DURATION = 30  # ms


def analyze_data(music_frames, mic_input_frames):    
    u = np.fromstring(music_frames, np.int16)
    u = np.float64(u)

    d = np.fromstring(mic_input_frames, np.int16)
    d = np.float64(d)
    # Apply adaptive filter
    M = 20  # Number of filter taps in adaptive filter
    step = 0.1  # Step size
    y, e, w = adf.nlms(u, d, M, step, returnCoeffs=True)
    
    scaled = np.int16(e/np.max(np.abs(e)) * 32767) 
    write('splitaudio.wav', 32000, scaled)

    print("THE SPLIT HAS BEEN WRITTEN STOP NOW")
    time.sleep(5)
    process_split_audio()

def process_split_audio():
    print("Processing voice detection for split audio...")
    
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
    "type": "service_account",
    "project_id": "my-project-1478361491618",
    "private_key_id": "93edfcefc3766a686a5359a04e5e6800471cbc6f",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDMce1Ua4ZQKRMf\nlXCzlBzt8gvr/CsvzmooQwm6oYII9nYDKEx0LHQ5aE/HKQonTrjtTwkRxTT+f3CP\nYkLuCCmPhmBD+BiaHj2Tias5PT2D1SfxY9ZL/UlRfQA6QCp/CX2JCTuUMGraTlR4\nBvoMfDY3y8P4TK0LxxCKq8g7DcpIcLJhICZPavORSXu72vOVBsN4DdG2+VjuLkDR\nQ6tFntC3eyxuZNerEPlXGTWg/gMnTyOIAgqNnarh19QXTcfG2ovEFN0KQ2Eg9ZUC\neVXVQoPHDkrBnlim4MlWhnWr04URZ+uM8fXRPVRKa+Flb+clorT4ROM8CXQWpGcb\nlelPToCjAgMBAAECggEAVwz3ceeqs/0ZUGxwJXaebs6ONvgTZ3KrjuMkhFv6o1hV\n3XhOPXUkM8FvnqyhzyTc5uatROzEaMzYn6TGPNYq5BriaG5+Azl3HJgU2PVzeOvM\n6yKIf6ikjFb+Ps9NiPQAiNXukWWgSb3qh4To+WH2MAHKOrJjSE2FhJYqVsLDa94V\nsEFZpKVJ0n1AQIckqFMk8h/AIF8t9EW/2Feutpg0HHpPk6fckjZ+KfL38hAhaoNZ\npAFU973ZU+xKvAkj0hndy7sJWfPUDEIoyfX1iY+59bkybN4qmEdgsmBVup+vqiMe\nGXwbmRuehC71764U2Fu5nsiz7CHn7wDTNT6Q6TDGuQKBgQDnTTXT6qOw2i4f00ns\nmvVRZqNFRb5CG+GkYtCVulcct/5rG0cL324sguYqUygAoc6wpRZRO/8h5nbsrEpZ\nn5KKYfKM9pOTCTADHb1pmuA4M7oU98ES6pYFwK4cgZIMR4Ug9xwYDa7O5zgbU6K9\nKVhkIkLUM81P5EDoeFl2fOwlFQKBgQDiRpLeAN15x5B3oAYyFxsKAUzgrTwrLv7z\nxFTfrAEjuMCF2/Xu25RpbxUg9qoBzM3ZJ5tOFV3Bx7krhc12CBxnBDQCN6gB1VT1\ndSc57UrlkzVPjsKXGHHo3Ioe63lwjU/lNjs/SAbsgUB4KtiixnrKke8irzGeREVd\niYq4Mpzs1wKBgQCKM5Hz+wCvTM2+akqDOttVNdRcMZ3KdkpOJFSpAdvG5xD3Aidj\nKq7znYrUwzblmcibtygshYKdyMxKAW+zOSsf0AJSw4nNkvHDCuP/03AhZJbMrHQK\nT2wwJ75gffK7r4gV+FAq9xH5wiG+Aiz8hVWxDt+LVyBXmfRGcpJRv7aBOQKBgQCp\nz6rinqWXgdQCYn6j0sFBBe7K4lc4VUGScTH81hnY1Arvqj5rrjA329xwa4z0Yt3M\n7TNZKyG8joWBix3BSZ7/FKFvVJNqJM5oky4IA/PkTFCCzzFrsTWzOucRA0iU1ggy\njTtzZzuC/BEE3arMpcV7Bn//eJj1HGkuJE2NpLYt6wKBgQDFFMC3zlFw3HShuaho\nwSKL90W32RjGGn2naKZEs5s0cBk8fvn3WquNKgCsKCD6DKxaIz38D5m0vnTaWbun\nzCnkOUeDtuoCwJFUapfqlRFBSZp5p+xZuk0jv93JUuqZxrv7k701seCtSkd+pB48\nZW6lOkYa13b6I2X4/KvRxrcRrA==\n-----END PRIVATE KEY-----\n",
    "client_email": "adaptiveaudio@my-project-1478361491618.iam.gserviceaccount.com",
    "client_id": "109715588347315681415",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/adaptiveaudio%40my-project-1478361491618.iam.gserviceaccount.com"
    }"""

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "splitaudio.wav")
    r = sr.Recognizer()
    
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
    
    try:
        results =  r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        lower_vol()
        print(results)
        
    except sr.UnknownValueError:
        print("Unrecognizable audio.")
        reset()
        
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
