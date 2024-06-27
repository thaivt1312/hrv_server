from config.FCMManage import sendPush
from .index import setInterval

from datetime import datetime, timedelta
# from .data_process import prepare_model_data, run_predict1, run_predict2, run_predict3, run_predict4
from .index import send_to_stresswatch2, send_to_stresswatch3
from ..devices_manage.get_data import getDeviceInfo, getUserInfo, getLastestRecord
from ..devices_manage.save_data import insertNewUser, updateFirebaseToken, saveHeartRateData

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
            latitude = record[2]
            longitude = record[3]
            deviceId = record[4]
            prediction = record[6]
            date_time1 = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            userId = record[5]
            (curIndex, check) = findThreadIndex(userId)
            if check:
                if threadArr[curIndex]['isNew'] == False:
                    if abs(datetime.now() - date_time1) > timedelta(minutes=2):
                        stopInterval(userId)
                        
                        print ("\nSmart watch has been disconnected, last prection is: " + prediction + ", at " + date_time + ".\n")
            
                        healthData2 = {
                            "user_id": "01hw37jjx5c74az9e786k50nvc",
                            "stress_level": 0,
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
                            "stressLevel": 0,
                            "datetime": date_time,
                            "latitude": latitude,
                            "longitude": longitude,
                            "averageHeartRate": avg_heartbeat,
                            "prediction": "Smart watch has been disconnected, last prection is: " + prediction,
                            "stepCount": 0,
                            "soundFile": 'No file available',
                        }
                        # send_to_stresswatch2(healthData2)
                        # send_to_stresswatch3(healthData3)
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
    # hrdata = data.get('hrData')
    heartBeatData = data.get('heartBeatData')
    firebaseToken = data.get('firebaseToken')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    get = getUserInfo(firebaseToken)
    deviceId = get[0]
    userId = get[1]
    avgHeartBeat = 0
    hrsum = 0
    string = heartBeatData[1:len(heartBeatData)-1]
    if (len(string)):
        arr = string.split(", ")
        for x in arr:
            y = float(x)
            hrsum += y
        avgHeartBeat = hrsum/len(arr)
    avgHeartBeat = round(avgHeartBeat, 2)
    sendPush('get', 'getRecord', [firebaseToken])
    if avgHeartBeat > 0:
        prediction = "Average heart beat is " + str(avgHeartBeat) + "."
    else:
        prediction = "Cannot get heart beat data."

    if latitude == "" or longitude == "":
        prediction = prediction + " Cannot get position data."
    else:
        latitude = float(latitude)
        longitude = float(longitude)
        
    params=(
        deviceId,
        userId, 
        datetime.now(), 
        avgHeartBeat,
        latitude,
        longitude,
        prediction
    )
    saveHeartRateData(params)
    (curIndex, check) = findThreadIndex(userId)
    if check:
        threadArr[curIndex]['isNew'] = False