import time, threading
import pickle
from pathlib import Path
from tensorflow.keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
import transformers
# from .MLModel.Model1.ML1 import build_model, run_predict

StartTime=time.time()

# def action() :
#     print('action ! -> time : {:.1f}s'.format(time.time()-StartTime))
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

# start action every 0.6s
# inter=setInterval(0.6,action)
# print('just after setInterval -> time : {:.1f}s'.format(time.time()-StartTime))

# # will stop interval in 5s
# t=threading.Timer(5,inter.cancel)
# t.start()

# def run_model():
    # hr_model1 = build_model()
# def prepareDataModel1(rr):
