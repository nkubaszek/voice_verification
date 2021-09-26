import sys
sys.path.append("./")
import pyaudio
import wave

def unikatoweid():
    from time import time
    return hex(int(time()*10000000))[2:]

Id_uzytkownika = unikatoweid()

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "audioRefrence/" + Id_uzytkownika + ".wav"

audio = pyaudio.PyAudio()

print("Powiedz biometria")
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print( "Nagrywanie...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print( "Nagrywanie zakończone")

print("Twoje id to", Id_uzytkownika)
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

