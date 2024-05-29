from config.db_connect import mydb
import string
import random
from config.FCMManage import sendPush
from .index import setInterval
import threading
from datetime import datetime
from .data_process import prepare_model_data, run_predict1, run_predict2, run_predict3, run_predict4
import math

threadArr = []
def runningHR(firebaseToken):
    def action():
        # sendPush('get', 'getRecord', [firebaseToken])
        sendPush('get', 'getHRData', [firebaseToken])
    action()
    setInterval(30, action)
    
def getTableRowCount():
    mycursor = mydb.cursor()
    query="SELECT COUNT(*) FROM device_manager"
    mycursor.execute(query)
    res = mycursor.fetchall()
    return len(res)

def getUserInfo(firebaseToken):
    mycursor = mydb.cursor(dictionary=True)
    query="SELECT device_id, user_id FROM device_manager WHERE firebase_token = %s AND id <> %s"
    params=(firebaseToken,0)
    mycursor.execute(query, params)
    
    res = mycursor.fetchone()
    return res
        
def id_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def checkDeviceId(deviceId,firebaseToken):
    thread=threading.Thread(target=runningHR, args=(firebaseToken,))
    mycursor = mydb.cursor()
    query="SELECT * FROM device_manager WHERE device_id = %s AND id <> %s"
    params=(deviceId,0)
    mycursor.execute(query, params)
    # print(mycursor.statement)
    res = mycursor.fetchall()
    # for x in res:
    #     print(x)
    # print(len(res))
    if len(res) == 0:
        print("run insert")
        passcode = id_generator(6)
        # print(passcode)
        hashcode = hash(passcode) ^ hash(deviceId)
        tableCount = getTableRowCount('device_manager') + 1
        query = """INSERT INTO device_manager (device_id, token, firebase_token, is_login, user_id) VALUES (%s, %s, %s, %s, %s)"""
        params=(deviceId, hashcode, firebaseToken, '0', tableCount)
        thread.start()
        threadArr.append({
            'index': tableCount,
            't': thread
        })
        mycursor.execute(query, params)
        mydb.commit()
        return "false"
    else:
        print("run update")
        # hashcode = hash(passcode) ^ hash(deviceId)
        query = """UPDATE device_manager SET firebase_token=%s WHERE device_id=%s AND id <> 0"""
        params=(firebaseToken, deviceId)
        mycursor.execute(query, [firebaseToken, deviceId])
        mydb.commit()
        get = getUserInfo(firebaseToken)
        userId = get["user_id"]
        curThread = ''
        for x in threadArr:
            if x['index'] == int(userId):
                curThread = x
                break
        print(curThread)
        if curThread == '':
            thread.start()
            threadArr.append({
                'index': int(userId),
                't': thread
            })
        else:
            curThread['t'].cancel()
            thread.start()
            curThread['t'] = thread
        return "true"
    

def checklogin(passcode,deviceId):
    mycursor = mydb.cursor()
    hashcode = hash(passcode) ^ hash(deviceId)
    query=f"SELECT device_id, token, firebase_token FROM device_manager WHERE token = '{hashcode}'"
    mycursor.execute(query)
    res = mycursor.fetchall()
    for x in res:
        print(x)
    return hashcode
        
def saveHRData(data):
    print(data)
    hrdata = data.get('hrData')
    firebaseToken = data.get('firebaseToken')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    get = getUserInfo(firebaseToken)
    deviceId = get["device_id"]
    userId = get["user_id"]
    avgHeartBeat = 0
    hrsum=0
    string = hrdata[1:len(hrdata)-1]
    arr = string.split(", ")
    for x in arr:
        print(x)
        print(float(x))
        y = float(x)
        hrsum += 60000.0 / y
    avgHeartBeat = hrsum/len(arr)
    
    data = prepare_model_data(arr)
    # print(data)
    res1 = run_predict1(data)
    res2 = run_predict2(data)
    res3 = run_predict3(data)
    # res4 = run_predict4(data)
    res = sum([res1, res2, res3]) / 3
    print(res1, res2, res3, res)
    if (res > 1):
        sendPush('get', 'getRecord', [firebaseToken])
    
    mycursor = mydb.cursor()
    query = """INSERT INTO hr_data 
        (hr_data, device_id, user_id, time, avg_heartbeat, stress_level, latitude, longitude) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    params=(
        str(hrdata), 
        deviceId, 
        userId, 
        datetime.now(), 
        avgHeartBeat,
        math.floor(res),
        float(latitude),
        float(longitude)
    )
    mycursor.execute(query, params)
    mydb.commit()
    