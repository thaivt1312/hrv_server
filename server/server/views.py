from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from pathlib import Path

import time, threading

from .hrv_process.index import setInterval
from .hrv_process.saveToDB import checklogin, checkDeviceId, saveHRData
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
        thread=threading.Thread(target=loginProcess, args=(len(threadArr) + 1,))
        thread.start()
        threadArr.append({
            'index': len(threadArr) + 1,
            't': thread
        })
        checklogin("", "")
        response = {
            "login": "started"
        }
        return Response(response, status=status.HTTP_200_OK)

class LogoutApi(APIView):
    def post(self, request, *args, **kwargs):
        index = request.data
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
        run_sound_predict(file)
        # else:
        response = {
            "success": "true"
        }
        
        return Response(response, status=status.HTTP_200_OK)