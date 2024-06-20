from config.FCMManage import sendPush
from .index import setInterval

from datetime import datetime, timedelta
from .data_process import prepare_model_data, run_predict1, run_predict2, run_predict3, run_predict4
from .index import send_to_stresswatch2, send_to_stresswatch3
from ..data_db_process.get_data import getDeviceInfo, getUserInfo, getLastestRecord
from ..data_db_process.save_data import insertNewUser, updateFirebaseToken, saveHeartRateData
import math

threadArr = []
intervalTime = 50

def findThreadIndex(userId):
    curIndex = 0
    check = False
    for x in threadArr:
        if x['index'] == int(userId):
            check = True
            break
        curIndex = curIndex + 1
    return [curIndex, check]
def stopInterval(userId):
    (curIndex, check) = findThreadIndex(userId)
    if check:
        threadArr[curIndex]['t'].cancel()
    return (curIndex, check)
    
def checkDeviceId(deviceId,firebaseToken):
    def action():
        record = getLastestRecord(firebaseToken)
        if len(record) > 0:
    
            avg_heartbeat = record[0]
            date_time = record[1]
            stress_level = record[2]
            latitude = record[3]
            longitude = record[4]
            deviceId = record[5]
            prediction = record[7]
            date_time1 = datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S")
            userId = record[6]
            (curIndex, check) = findThreadIndex(userId)
            if check:
                if threadArr[curIndex]['isNew'] == False:
                    if abs(datetime.now() - date_time1) > timedelta(minutes=2):
                        stopInterval(userId)
            
                        healthData2 = {
                            "user_id": "01hw37jjx5c74az9e786k50nvc",
                            "stress_level": stress_level,
                            "datetime": date_time,
                            "latitude": latitude,
                            "longitude": longitude,
                            "average_heart_rate": avg_heartbeat,
                            "device_id": deviceId,
                            "prediction": "Smart watch has been disconnected, last prection is: " + prediction,
                            "step_count": 0,
                        }
            
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
                            "prediction": "Smart watch has been disconnected, last prection is: " + prediction,
                            "stepCount": 0,
                            "soundFile": 'No file available',
                        }
                        send_to_stresswatch2(healthData2)
                        send_to_stresswatch3(healthData3)
                        return
        sendPush('get', 'getHRData', [firebaseToken])
    
    res = getDeviceInfo(deviceId)
    
    if len(res) == 0:
        insertNewUser(deviceId, firebaseToken)
        print("\nInsert new user success\n")
        get = getUserInfo(firebaseToken)
        newUserId = get[1]
        action()
        threadArr.append({
            'index': newUserId,
            'isNew': True,
            't': setInterval(intervalTime, action)
        })
        return "false"
    else:
        updateFirebaseToken(deviceId, firebaseToken)
        print("\nUpdate firebase token success\n")
        get = getUserInfo(firebaseToken)
        userId = get[1]
        (curIndex, check) = stopInterval(userId)
        action()
        if check:
            threadArr[curIndex] = {
                'index': int(userId),
                'isNew': True,
                't': setInterval(intervalTime, action)
            }
        else: 
            threadArr.append({
                'index': int(userId),
                'isNew': True,
                't': setInterval(intervalTime, action)
            })
        return "true"
        
def saveHRData(data):
    hrdata = data.get('hrData')
    firebaseToken = data.get('firebaseToken')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    get = getUserInfo(firebaseToken)
    deviceId = get[0]
    userId = get[1]
    avgHeartBeat = 0
    hrsum = 0
    string = hrdata[1:len(hrdata)-1]
    if (len(string)):
        arr = string.split(", ")
        for x in arr:
            y = float(x)
            hrsum += 60000.0 / y
        avgHeartBeat = hrsum/len(arr)

        data = prepare_model_data(arr)
        
        res1 = run_predict1(data)
        res2 = run_predict2(data)
        res3 = run_predict3(data)
        # res4 = run_predict4(data)
        res = sum([res1, res2, res3]) / 3
        print('\n', res1, res2, res3, res, '\n')
        if (res >= 1):
            sendPush('get', 'getRecord', [firebaseToken])
            
        stress_level = math.floor(res)
        stress_level_str = ''
        if stress_level == 3:
            stress_level_str = "High"
        elif stress_level > 2:
            stress_level_str = "Medium"
        elif stress_level >= 1:
            stress_level_str = "Low"
        prediction = "Stress level " + str(stress_level_str) + ", average heart beat is " + str(avgHeartBeat) + "."
        params=(
            str(hrdata), 
            deviceId,
            userId, 
            datetime.now(), 
            avgHeartBeat,
            math.floor(res),
            float(latitude),
            float(longitude),
            prediction
        )
        saveHeartRateData(params)
        (curIndex, check) = findThreadIndex(userId)
        if check:
            threadArr[curIndex]['isNew'] = False