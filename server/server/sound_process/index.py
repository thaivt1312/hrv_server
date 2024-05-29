import librosa
import io
from pydub import AudioSegment
import os
import numpy as np
from .keras_yamnet import params
from .keras_yamnet.yamnet import YAMNet, class_names
from .keras_yamnet.preprocessing import preprocess_input
from pathlib import Path

global sound_model
def check_file(file):
        print("File does not exist at the specified path")
def load_sound_model():
    mypath = Path().absolute()
    global sound_model
    sound_model = YAMNet(weights=mypath/'server/sound_process/keras_yamnet/yamnet.h5')

def run_sound_predict(file):
    RATE = params.SAMPLE_RATE
    WIN_SIZE_SEC = 0.975
    CHUNK = int(WIN_SIZE_SEC * RATE)
 
    mypath = Path().absolute()
    yamnet_classes = class_names(mypath/'server/sound_process/keras_yamnet/yamnet_class_map.csv')
 
    # file = 'test4.mp3'
    print(file)
    
    # if os.path.isfile(file):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(io.BytesIO(file.read()), format="mp3")

        # Export the audio to a file-like object in WAV format
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)  # Seek to the start so librosa can read it
        y, sr = librosa.load(wav_io, sr=None)
        print("File loaded successfully")
        frames = librosa.util.frame(y, frame_length=CHUNK, hop_length=CHUNK)
        frames = frames.T  # Chuyển vị ma trận
    
        predictions = []
        # Chia dữ liệu âm thanh thành các khung có kích thước phù hợp
        for frame in frames:
            data = preprocess_input(frame, sr)
            prediction = sound_model.predict(np.expand_dims(data, 0))[0]
            # get the highest probability class and its name
            prediction = np.argmax(prediction)
            print(prediction)
            # prediction = yamnet_classes[prediction]
            predictions.append((prediction, yamnet_classes[prediction]))
    
        predictions = np.array(predictions)
        print(predictions)
        return predictions
    except Exception as e:
        print(f"An error occurred: {e}")
    # else:
    #     print("File does not exist at the specified path")
 