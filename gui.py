import os
import tkinter as tk
from tkinter import filedialog, RAISED
import PIL
from PIL import ImageTk, Image
import sys

directory = "audioRefrence/"
sys.path.append("./")
from tkinter import messagebox
import pyaudio
import wave
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import librosa.display
from dtw import dtw
from numpy.linalg import norm
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "1.wav"

audio = pyaudio.PyAudio()
def startRecording():
    # start Recording
    messagebox.showinfo(title="Biometria", message="Gdy zacznie się nagrywanie powiedz biometria")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    messagebox.showinfo(title="Nagrywanie...", message="Nagrywanie...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    messagebox.showinfo(title="Nagrywanie zakończone", message="Nagrywanie zakończone")



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

def wyświetl_wykresy():
    for filename in os.listdir(directory):
        i = 0
        if filename.endswith(".wav"):
            file = os.path.join(filename)
            stringFile = str(file);
            y1, sr1 = librosa.load('1.wav')
            y2, sr2 = librosa.load("audioRefrence/"+stringFile)



            mfcc1 = librosa.feature.mfcc(y1,sr1)   #Liczenie wartości współćzynników mfcc


            mfcc2 = librosa.feature.mfcc(y2, sr2)

            #plt.show()

            dist,cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
            messagebox.showinfo(title="Dystans ",message="Dystans pomiędzy próbkami wynosi"
            +str(dist))

            dystans=[]
            dystans.append(dist)

            i += 1

        if(dist < 27000):

            userId = os.path.splitext(file)
            messagebox.showinfo(id,"Twoje id to "+ str(userId[0]))
            plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
            plt.plot(path[0],path[1], 'w') #ścieżka dopasowania
            plt.xlim((-0.5, cost.shape[0] - 0.5))
            plt.ylim((-0.5, cost.shape[1]-0.5))
            plt.title('Ścieżka dopasowania')
            plt.xlabel("Czas nagrania[s]")
            plt.ylabel("Czas nagrania z bazy[s]")
            plt.show()


            break

root = tk.Tk() # create root window
root.title("Aplikacja do identyfikacji mówcy") # title of the GUI window
root.geometry("400x400") # specify the max size the window can expand to
root.config(bg="gray25") # specify background color
root.resizable(False,False)



def Identify():
    identify= tk.Toplevel(root)
    identify.geometry("400x400") # specify the max size the window can expand to
    identify.config(bg="gray25") # specify background color
    identify.resizable(False,False)
    btn3 = tk.Button(identify,command=startRecording, bg="orange",text = "Nagraj próbkę głosową ")
    btn3.place(relx = 0.5,
               rely = 0.3,
               anchor ='center')
    btn4 = tk.Button(identify,command=wyświetl_wykresy, bg="orange",text = "Identyfikacja ")
    btn4.place(relx = 0.5,
               rely = 0.5,
               anchor ='center')

btn1 = tk.Button(root, bg="orange",text = "Nagraj do bazy ")

btn1.place(relx = 0.5,
            rely = 0.3,
            anchor ='center')
btn2 = tk.Button(root,command=Identify, bg="orange",text = "Identyfikacja mówcy ")

btn2.place(relx = 0.5,
           rely = 0.5,
           anchor ='center')


root.mainloop()