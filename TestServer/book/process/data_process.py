import numpy as np

def get_mrr(rr):
    # '''rr: distance between peaks in ms'''
    return np.mean(rr)
def get_mhr(rr):
    return np.mean(60000/rr)
def get_sdrr(rr, mrr):
    num = np.sum([np.math.pow(x,2) for x in rr-mrr])
    return np.sqrt(num/(np.size(rr)-1))
def get_sdhr(rr, mhr):
    num = np.sum([np.math.pow(x,2) for x in (60000/rr)-mhr])
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
    return count*100 / (np.size(rr)-1)
def get_prr25(rr):
    arr = np.abs(np.diff(rr))
    count = 0
    for arr_i in arr:
        if arr_i > 25:
            count += 1 
    return count*100 / (np.size(rr)-1)
def get_prr50(rr):
    arr = np.abs(np.diff(rr))
    count = 0
    for arr_i in arr:
        if arr_i > 50:
            count += 1 
    return count*100 / (np.size(rr)-1)

def prepare_model1_data(rr):
    print(rr)

def preprae_model2_data(rr):
    print(rr)