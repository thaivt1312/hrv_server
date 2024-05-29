import time, threading
import pickle
from pathlib import Path
from tensorflow.keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel

StartTime=time.time()

def loadHRModel(filename):

    mypath = Path().absolute()
    print(mypath/filename)
    filepath = mypath/filename

    model = pickle.load(open(filepath, 'rb'))
    print('done HR model')
    return model
def loadSoundModel(filename):
    mypath = Path().absolute()
    print(mypath/filename)
    filepath = mypath/filename

    model = load_model(filepath, custom_objects={
        'STFT':STFT(n_fft=1024, hop_length=512),
        'Magnitude':Magnitude,
        'ApplyFilterbank':ApplyFilterbank,
        'MagnitudeToDecibel':MagnitudeToDecibel}
    )
    print('done sound model')
    return model
    
class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()