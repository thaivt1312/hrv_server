
from datetime import datetime, timedelta

from config.FCMManage import sendPush

from ..devices_manage.get_data import getDeviceInfo, getUserInfo, getLastestRecord
from ..devices_manage.save_data import insertNewUser, updateFirebaseToken

from ..variables.interval import setInterval
from ..variables.thread_control import findThreadIndex, isNewThread, stopThread, appendNew, changeValue

intervalTime = 45

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
                if isNewThread(userId):
                    if abs(datetime.now() - date_time1) > timedelta(minutes=2):
                        stopThread(userId)
                        newPrediction = "Smart watch has been disconnected, last prection is: " + prediction + ", at " + date_time + "."
                        print ("\n" + newPrediction + ".\n")
            
                        healthData2 = {
                            "user_id": "01hw37jjx5c74az9e786k50nvc",
                            "stress_level": 0,
                            "datetime": date_time,
                            "latitude": latitude,
                            "longitude": longitude,
                            "average_heart_rate": avg_heartbeat,
                            "device_id": deviceId,
                            "prediction": newPrediction,
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
                            "prediction": newPrediction,
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
        appendNew(newUserId, setInterval(intervalTime, action))
        return "false"
    else:
        updateFirebaseToken(deviceId, firebaseToken)
        print("\nUpdate firebase token success\n")
        get = getUserInfo(firebaseToken)
        userId = get[1]
        (curIndex, check) = stopThread(userId)
        action()
        if check:
            changeValue(curIndex, userId, setInterval(intervalTime, action))
        else: 
            appendNew(userId, setInterval(intervalTime, action))
        return "true"