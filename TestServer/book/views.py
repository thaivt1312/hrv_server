from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from django.core.files.storage import default_storage
import time, threading
from threading import Event
from book.process.index import setInterval, loadModel
from config.db_connect import mydb
from book.process.saveToDB import checklogin

# Create your views here.
threadArr = []
global hr_model1, hr_model2, hr_model3
global sound_model1, sound_model2, sound_model3

hr_model1 = loadModel('book/process/models/model1_1')
hr_model2 = loadModel('book/process/models/model1_2')
hr_model3 = loadModel('book/process/models/model2.pickle')

def loginProcess(index): 
    StartTime=time.time()
    def action():
        print(index, 'action ! -> time : {:.1f}s'.format(time.time()-StartTime))
    run=setInterval(5, action)

class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        StartTime=time.time()
        index = len(threadArr) + 1
        def action():
            print(index, 'action ! -> time : {:.1f}s'.format(time.time()-StartTime))
        run=setInterval(5, action)
        # thread=threading.Thread(target=loginProcess, args=(len(threadArr) + 1,))
        # thread.start()
        threadArr.append({
            'index': len(threadArr) + 1,
            't': run
        })
        checklogin("", "")
        response = "started"
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
        # thread=threading.Thread(target=loginProcess)
        # thread.start()
        # threadArr.append({
        #     'index': len(threadArr) + 1,
        #     't': thread 
        # })
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        response = ""
        print(data.get('file'))
        if data.get('file'):
            print(request.FILES.get('file').name)
            response = request.FILES.get('file').name
            file = request.FILES.get('file')
            file_name = default_storage.save(file.name, file)
        else:
            response = data
        
        return Response(response, status=status.HTTP_200_OK)