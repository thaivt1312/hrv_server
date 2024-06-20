import numpy as np

from .index import loadHRModel
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

global hr_model1, hr_model2, hr_model3, hr_model4, hr_model5, hr_model6
global sound_model1, sound_model2, sound_model3

def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array
def run_load_model():
    global hr_model1, hr_model2, hr_model3, hr_model4, hr_model5, hr_model6
    global sound_model1, sound_model2, sound_model3 
    hr_model1 = loadHRModel('server/hrv_process/models/ann.pickle')
    hr_model2 = loadHRModel('server/hrv_process/models/svc.pickle')
    hr_model3 = loadHRModel('server/hrv_process/models/knn.pickle')
    hr_model4 = loadHRModel('server/hrv_process/models/knnpickel1')
    hr_model5 = loadHRModel('server/hrv_process/models/knnpickel2')
    # hr_model6 = loadHRModel('server/hrv_process/models/ensemble_soft.pickle')

def get_mrr(rr):
    # '''rr: distance between peaks in ms'''
    return np.mean(rr)
def get_mhr(rr):
    return np.mean(60000.0 / rr)
def get_sdrr(rr, mrr):
    num = np.sum([np.math.pow(x,2) for x in rr-mrr])
    return np.sqrt(num/(np.size(rr)-1))
def get_sdhr(rr, mhr):
    num = np.sum([np.math.pow(x,2) for x in (60000.0 / rr)-mhr])
    return np.sqrt(num/(np.size(rr)-1))
def get_cvrr(sdrr, mrr):
    return sdrr*100/mrr
def get_rmssd(rr):
    num = np.sum([np.math.pow(x,2) for x in np.diff(rr)])
    return np.sqrt(num/(np.size(rr)-1))
def get_prr20(rr):
    arr = np.abs(np.diff(rr))
    count = 0
    for arr_i in arr:
        if arr_i > 20:
            count += 1 
    return count*100.0 / (np.size(rr)-1)
def get_prr25(rr):
    arr = np.abs(np.diff(rr))
    count = 0
    for arr_i in arr:
        if arr_i > 25:
            count += 1 
    return count*100.0 / (np.size(rr)-1)
def get_prr50(rr):
    arr = np.abs(np.diff(rr))
    count = 0
    for arr_i in arr:
        if arr_i > 50:
            count += 1 
    return count*100.0 / (np.size(rr)-1)
    
def prepare_model_data(arr):
    brr = convert_strings_to_floats(arr)
    rr = np.array(brr)
    # print(rr)
    mrr=get_mrr(rr)
    mhr=get_mhr(rr)
    sdrr=get_sdrr(rr, mrr)
    sdhr=get_sdhr(rr, mhr)
    cvrr=get_cvrr(sdrr, mhr)
    rmssd=get_rmssd(rr)
    prr20=get_prr20(rr)
    prr50=get_prr50(rr)
    
    returnArr = [[
        mrr,
        mhr,
        sdrr,
        sdhr,
        cvrr,
        rmssd,
        prr20,
        prr50
    ]]
    
    return np.array(returnArr)
    
def run_predict1(data):
    return hr_model1.predict(data)
def run_predict2(data):
    return hr_model2.predict(data)
def run_predict3(data):
    return hr_model3.predict(data)
def run_predict4(data):
    return hr_model4.predict(data)