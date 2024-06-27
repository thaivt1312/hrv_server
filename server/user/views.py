from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.function import hash_password
from common.web_firebase_token import updateFirebaseToken, sendToUser

from config.db_connect import mydb
from config.msg import ACCOUNT_EXISTS, ACCOUNT_NOT_FOUND, WRONG_PASSWORD, LOGIN_SUCCESS, REGISTER_SUCCESS, UNAUTHORIZED

from .token_manage.token import decode_token, create_token
    
mycursor = mydb.cursor()

def validateToken(BearerToken):
    try:
        token = BearerToken.split(' ')[1]
        print(token)
        user_data = decode_token(token)
        return user_data.get('user_id')
    except:
        return None
    

def checkAccount(username):
    query = """SELECT username FROM account WHERE username=%s and is_deleted=%s"""
    params=(username, 0)
    mycursor.execute(query, params)
    
    res = mycursor.fetchone()
    mycursor.reset()
    print(res)
    if not res:
        return None
    else:
        return res[0]


class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        username = data.get('username')
        password = data.get('password')
        
        query = """SELECT id, password, account_type FROM account WHERE username=%s and is_deleted=%s"""
        params=(username, 0)
        mycursor.execute(query, params)
        res = mycursor.fetchone()
        mycursor.reset()
        
        print(res)
        if not res:
            response = {
                "msg": ACCOUNT_NOT_FOUND,
                "success": False
            }
        else:
            print(res[1], password)
            hashcode = hash_password(password)
            if hashcode == res[1]:
                firebaseToken = data.get('firebaseToken')
                updateFirebaseToken(res[0], firebaseToken)
                token = create_token(res[0], res[2])
                if res[2] == 0:
                    response = {
                        "msg": LOGIN_SUCCESS,
                        "data": {
                            "user_token": token,
                        },
                        "success": True
                    }
                else:
                    response = {
                        "msg": LOGIN_SUCCESS,
                        "data": {
                            "admin_token": token,
                        },
                        "success": True
                    }
                sendToUser(res[0], "test msg")
            else:
                response = {
                    "msg": WRONG_PASSWORD,
                    "success": False
                }
        print(response)
        return Response(response, status=status.HTTP_200_OK)
    

class deviceApi(APIView):
    def get(self, request, *args, **kwargs):
        # data = request.data
        # name = request.args.get("name")
        BearerToken = request.headers.get('Authorization')
        user_id = validateToken(BearerToken)
        if not user_id:
            response = {
                "msg": UNAUTHORIZED,
                "success": False
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            query = """SELECT * FROM device_manager"""
            params=(0,)
            mycursor.execute(query, params)
            res = mycursor.fetchall()
            mycursor.reset()
            print(res)
            
            response = {
                "data": map(
                    lambda x: {
                        "id": x[0],
                        "carer_id": x[1],
                        "device_id": x[2],
                        "device_information": x[4],
                        "user_information": x[5],
                        "is_active": x[6],
                        "is_running": x[7]
                    }, 
                    res
                ),
                "success": True
            }
            return Response(response, status=status.HTTP_200_OK)
        
class getNotificationList():
    def get(self, request, *args, **kwargs):
        data = request.data