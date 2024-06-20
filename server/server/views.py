from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from pathlib import Path
import os

from .hrv_process.index import send_to_stresswatch2, send_to_stresswatch3
from .hrv_process.saveToDB import checkDeviceId, saveHRData
from .hrv_process.data_process import run_load_model

from .sound_process.index import load_sound_model, run_sound_predict

# Create your views here.
threadArr = []
run_load_model()
load_sound_model()
    
# send_to_stresswatch3()

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
        # print(data.get('file'))
        # print(request.FILES.get('file').name)
        response = request.FILES.get('file').name
        file = request.FILES.get('file')
        file_name = default_storage.save(file.name, file)
        mypath = Path().absolute()
        print('\n', mypath/file_name, '\n')
        
        record = run_sound_predict(mypath/file_name, data.get('firebaseToken'))
        os.remove(mypath/file_name)
        
        avg_heartbeat = record[0]
        date_time = record[1]
        stress_level = record[2]
        latitude = record[3]
        longitude = record[4]
        deviceId = record[5]
        prediction = record[6]
        
        # print(prediction)
        
        healthData2 = {
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
        # print(healthData2)
        send_to_stresswatch2(healthData2, False)
        
        healthData3 = {
            "client_secret": "N1rB1JetZs9IEzP",
            "grant_type": "password",
            "client_id": "stress_watch_1_test",
            "smartWatchId": deviceId,
            "stressLevel": stress_level,
            "datetime": date_time,
            "latitude": latitude,
            "longitude": longitude,
            "averageHeartRate": avg_heartbeat,
            "prediction": prediction,
            "stepCount": 0,
            "soundFile": file,
        }
        send_to_stresswatch3(healthData3, False)
        
        response = {
            "success": "true"
        }
        
        return Response(response, status=status.HTTP_200_OK)