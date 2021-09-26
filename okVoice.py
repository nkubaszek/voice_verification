import librosa
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import librosa.display
from dtw import dtw
from numpy.linalg import norm


import os

directory = "audioRefrence/"

from soundrecording import *
# from enrol import *
startRecording()



for filename in os.listdir(directory):
    i = 0
    if filename.endswith(".wav"):
        file = os.path.join(filename)
        stringFile = str(file);
        y1, sr1 = librosa.load('1.wav')
        y2, sr2 = librosa.load("audioRefrence/"+stringFile)


        plt.subplot(1, 2, 1)
        plt.title('MFCC nagrania')
        mfcc1 = librosa.feature.mfcc(y1,sr1)   #Liczenie wartości współćzynników mfcc
        librosa.display.specshow(mfcc1,x_axis='time')
        plt.xlabel("Czas[s]")
        plt.ylabel("Współczynniki MFCC")
        sub2=plt.subplot(1, 2, 2)

        plt.title('MFCC dla nagrań z bazy')
        mfcc2 = librosa.feature.mfcc(y2, sr2)
        librosa.display.specshow(mfcc2,x_axis='time')
        plt.xlabel('Czas[s]')
        sub2.set_ylabel('Współczynniki MFCC')
        plt.show()

        dist,cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
        print("Dystans pomiędzy próbkami wynosi : ",dist)
        plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
        plt.plot(path[0],path[1], 'w') #ścieżka dopasowania
        plt.xlim((-0.5, cost.shape[0] - 0.5))
        plt.ylim((-0.5, cost.shape[1]-0.5))
        plt.title('DTW')
        plt.xlabel("Czas nagrania[s]")
        plt.ylabel("Czas nagrania z bazy[s]")
        plt.show()

        dystans=[]
        dystans.append(dist)

        i += 1

    if(dist < 27000):
        userId = os.path.splitext(file)
        print("Twoje id to "+ str(userId[0]))
        break
