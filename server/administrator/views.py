from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.function import hash_password
from common.web_firebase_token import updateFirebaseToken, sendToUser

from config.db_connect import mydb
from config.msg import ACCOUNT_EXISTS, ACCOUNT_NOT_FOUND, WRONG_PASSWORD, LOGIN_SUCCESS, REGISTER_SUCCESS, UNAUTHORIZED

from user.token_manage.token import decode_token, create_token
    
mycursor = mydb.cursor()

def validateToken(BearerToken):
    try:
        token = BearerToken.split(' ')[1]
        print(token)
        user_data = decode_token(token)
        return user_data
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
    
    

class accountApi(APIView):
    # get list accounts
    def get(self, request, *args, **kwargs):
        BearerToken = request.headers.get('Authorization')
        user_data = validateToken(BearerToken)
        user_id = user_data.get('user_id')
        account_type = user_data.get('account_type')
        
        
        if not user_id:
            response = {
                "msg": UNAUTHORIZED,
                "success": False
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            if account_type == 0:
                response = {
                    "msg": UNAUTHORIZED,
                    "success": False
                }
                return Response(response, status=status.HTTP_200_OK)
            
            else:
                query = """SELECT id, username, account_type FROM account WHERE id!=%s and is_deleted=%s"""
                params=(user_id, 0)
                mycursor.execute(query, params)
                res = mycursor.fetchall()
                mycursor.reset()
                print(res)
                
                response = {
                    "data": map(
                        lambda x: {
                            "id": x[0],
                            "username": x[1],
                            "account_type": x[2]
                        }, 
                        res
                    ),
                    "success": True
                }
                return Response(response, status=status.HTTP_200_OK)

    # add new account
    def post(self, request, *args, **kwargs):
        data = request.data
        BearerToken = request.headers.get('Authorization')
        user_id = validateToken(BearerToken)
        if not user_id:
            response = {
                "msg": UNAUTHORIZED,
                "success": False
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            username = data.get('username')
            password = data.get('password')
            account_type = data.get('type')
            
            user = checkAccount(username)
            print(user)
            if not user:
                hashcode = hash_password(password)
                
                query = """INSERT INTO account (username, password, account_type) VALUES (%s, %s, %s)"""
                params=(username, hashcode, account_type)
                mycursor.execute(query, params)
                mydb.commit()
                
                response = {
                    "msg": REGISTER_SUCCESS,
                    "success": True
                }
            else:
                response = {
                    "msg": ACCOUNT_EXISTS,
                    "success": False
                }
            return Response(response, status=status.HTTP_200_OK)
        
    # delete account
    def delete(self, request, *args, **kwargs):
        data = request.data
        BearerToken = request.headers.get('Authorization')
        user_id = validateToken(BearerToken)
        if not user_id:
            response = {
                "msg": UNAUTHORIZED,
                "success": False
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            username = data.get('username')
            user = checkAccount(username)
            if user:
                query = """UPDATE account SET is_deleted=%s WHERE username=%s"""
                params=(1, username)
                mycursor.execute(query, params)
                mydb.commit()
                
                response = {
                    "msg": "DELETE_SUCCESS",
                    "success": True
                }
            else:
                response = {
                    "msg": ACCOUNT_NOT_FOUND,
                    "success": False
                }
            return Response(response, status=status.HTTP_200_OK)


class deviceApi(APIView):
    def get(self, request, *args, **kwargs):
        # data = request.data
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
        