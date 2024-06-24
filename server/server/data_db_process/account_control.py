
from config.db_connect import mydb

mycursor = mydb.cursor()
import random
import string

def generate_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
    
def registerNewCarer(username, password):
    hashcode = hash(password) ^ hash(username)
    query = """INSERT INTO account (username, password) VALUES (%s, %s)"""
    params=(username, hashcode)
    mycursor.execute(query, params)
    mydb.commit()
    
def checkLogin(username, password):
    hashcode = hash(password) ^ hash(username)
    query = """SELECT password FROM account WHERE username=%s"""
    params=(username,)
    mycursor.execute(query, params)
    
    res = mycursor.fetchone()
    mycursor.reset()
    print(res)
    if not res:
        return "Account not found"
    print(res[0], password)
    if password == res[0]:
        return "Login success"
    else:
        return "Wrong password"
    
# def checkDevice(deviceId, deviceInformation):
    
# def addNewDevice(deviceId, deviceInformation):
    
    