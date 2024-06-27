from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .data_db_process.account_control import registerNewCarer, checkLogin, checkToken

class accountRegisterApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        response = registerNewCarer(username, password)
        return Response(response, status=status.HTTP_200_OK)
    
class adminAccountRegisterApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        token = data.get('token')
        if token == 1:
            username = data.get('username')
            password = data.get('password')
            response = registerNewCarer(username, password)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = "Donot have permission to create admin account"
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

class checkTokenApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        token = data.get('token')
        response = checkToken(token)
        return Response(response, status=status.HTTP_200_OK)

class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        response = checkLogin(data.get('username'), data.get('password'))
        # a = generate_password()
        print(response)
        # response = {
        #     "result": res,
        #     "hash": a
        # }
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
    