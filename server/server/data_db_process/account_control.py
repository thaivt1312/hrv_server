
from config.db_connect import mydb
from config.msg import ACCOUNT_EXISTS, ACCOUNT_NOT_FOUND, WRONG_PASSWORD, LOGIN_SUCCESS, REGISTER_SUCCESS
import hashlib
from ..account_manage.token_manage import create_token, decode_token

import random
import string

mycursor = mydb.cursor()

def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()
def generate_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
    
def checkAccount(username):
    query = """SELECT username FROM account WHERE username=%s"""
    params=(username,)
    mycursor.execute(query, params)
    
    res = mycursor.fetchone()
    mycursor.reset()
    print(res)
    if not res:
        return False
    else:
        return True
    
def registerNewCarer(username, password, accountType = 0):
    user = checkAccount(username)
    if not user:
        hashcode = hash_password(password)
        query = """INSERT INTO account (username, password, account_type) VALUES (%s, %s)"""
        params=(username, hashcode, accountType)
        mycursor.execute(query, params)
        mydb.commit()
        return REGISTER_SUCCESS
    else:
        return ACCOUNT_EXISTS
    
def checkLogin(username, password):
    query = """SELECT id, password FROM account WHERE username=%s"""
    params=(username,)
    mycursor.execute(query, params)
    
    res = mycursor.fetchone()
    mycursor.reset()
    print(res)
    if not res:
        return {
            "msg": ACCOUNT_NOT_FOUND
        }
    print(res[1], password)
    hashcode = hash_password(password)
    if hashcode == res[1]:
        token = create_token(res[0])
        return {
            "msg": LOGIN_SUCCESS,
            "token": token
        }
    else:
        return {
            "msg": WRONG_PASSWORD,
        }

def checkToken(token):
    try:
        res = decode_token(token)
        return res
    except Exception as e:
        print(e)
# def checkDevice(deviceId, deviceInformation):
    
# def addNewDevice(deviceId, deviceInformation):
    
    