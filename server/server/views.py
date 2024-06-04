from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from pathlib import Path
import os

import requests
import time, threading

from .hrv_process.index import setInterval
from .hrv_process.saveToDB import checklogin, checkDeviceId, saveHRData, getLastestRecord
from .hrv_process.data_process import run_load_model

from .sound_process.index import load_sound_model, run_sound_predict

# Create your views here.
threadArr = []
run_load_model()
load_sound_model()
def loginProcess(index): 
    StartTime=time.time()
    def action():
        print(index, 'action ! -> time : {:.1f}s'.format(time.time()-StartTime))
    action()
    run=setInterval(5, action)

class checkDevice(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        deviceId = data.get('deviceId')
        firebase_token = data.get('firebaseToken')
        check = checkDeviceId(deviceId, firebase_token)
        
        response = {
            'login' : check,
        }
        return Response(response, status=status.HTTP_200_OK)

class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        StartTime=time.time()
        index = len(threadArr) + 1
        def action():
            print(index, 'action ! -> time : {:.1f}s'.format(time.time()-StartTime))
        # action()
        # run=setInterval(5, action)
        # thread=threading.Thread(target=setInterval(5, action))
        # thread.start()
        threadArr.append({
            'index': len(threadArr) + 1,
            't': setInterval(5, action)
        })
        # checklogin("", "")
        response = {
            "login": "started"
        }
        return Response(response, status=status.HTTP_200_OK)

class LogoutApi(APIView):
    def post(self, request, *args, **kwargs):
        index = request.data
        # curIndex = 0
        # check = False
        # for x in threadArr:
        #     if x['index'] == int(index):
        #         check = True
        #         break
        #     curIndex = curIndex + 1
        print(index)
        # if check:
        #     threadArr[curIndex]['t'].cancel()
            # thread.start()
            # threadArr.append({
            #     'index': int(userId),
            #     't': thread
            # })
        print(threadArr[index])
        threadArr[index]['t'].cancel()
        response = "done"
        return Response(response, status=status.HTTP_200_OK)


class TestAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        response = {
            "abcde" : 123,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        response = data
        
        return Response(response, status=status.HTTP_200_OK)
    
class HRVDataAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        saveHRData(data)
        response = data
        
        return Response(response, status=status.HTTP_200_OK)
    
class SoundDataAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        # response = "server received"
        print(data.get('file'))
        # print(request.FILES.get('file').name)
        response = request.FILES.get('file').name
        file = request.FILES.get('file')
        file_name = default_storage.save(file.name, file)
        mypath = Path().absolute()
        print(mypath/file_name)
        
        soundArr = run_sound_predict(mypath/file_name)
        soundArr = list(set(soundArr))
        
        print(soundArr)
        os.remove(mypath/file_name)
        
        soundStr = ""
        index = 0
        for ele in soundArr:
            if index == len(soundArr) - 1:
                soundStr += ele
            else:
                soundStr += ele + ', '
            index = index + 1
        
        record = getLastestRecord(data.get('firebaseToken'))
        
        avg_heartbeat = record[0]
        date_time = record[1]
        stress_level = record[2]
        latitude = record[3]
        longitude = record[4]
        deviceId = record[5]
        userId = record[6]
        # print(soundArr, stress_level, avg_heartbeat, date_time)
        # else:
        stress_level_str = ''
        if stress_level == 3:
            stress_level_str = "High"
        elif stress_level > 2:
            stress_level_str = "Medium"
        elif stress_level >= 1:
            stress_level_str = "Low"
        if len(soundStr) > 0:
            prediction = "Stress level " + stress_level_str + ". In audio has: " + soundStr + '.'
        else:
            prediction = "Stress level " + stress_level_str + ". No dangerous predicted in audio."
        healthData = {
            "user_id": "01hw37jjx5c74az9e786k50nvc",
            "stress_level": stress_level,
            "datetime": date_time,
            "latitude": latitude,
            "longitude": longitude,
            "average_heart_rate": avg_heartbeat,
            "device_id": deviceId,
            "prediction": prediction,
            "step_count": 0,
        }
        print(prediction)
        print(healthData)
        mobileResponse = requests.post('http://222.252.10.203:32311/v1/stressdata', data = healthData)
        # print(mobileResponse)
        print (mobileResponse.content)
        # mobileResponse.text
        response = {
            "success": "true"
        }
        
        return Response(response, status=status.HTTP_200_OK)