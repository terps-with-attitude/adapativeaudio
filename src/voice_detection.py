import webrtcvad
import wave


vad = webrtcvad.Vad()
vad.set_mode(1)

w = wave.open("no_voice.wav", "r")
frame_rate = w.getframerate()

# running VAD on 30 ms of silent audio
frame_duration = 10;
num_frames = frame_rate * frame_duration / 1000;

print(num_frames)

frame = w.readframes(num_frames)


print('Contains speech: %s' % (vad.is_speech(frame, frame_rate)))
                        
                           
#sample_rate = 16000
#frame_duration = 10  # ms
#frame = b'\x00\x00' * (sample_rate * frame_duration / 1000)
#print('Contains speech: %s' % (vad.is_speech(frame, sample_rate)))                  
#
#
