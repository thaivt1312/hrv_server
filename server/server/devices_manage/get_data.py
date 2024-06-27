from config.db_connect import mydb

mycursor = mydb.cursor()

def getDeviceInfo(deviceId):
    query="SELECT * FROM device_manager WHERE device_id = %s AND id <> %s"
    params=(deviceId, 0)
    mycursor.execute(query, params)
    
    res = mycursor.fetchall()
    mycursor.reset()
    return res

def getUserInfo(firebaseToken):
    query="SELECT device_id, id as user_id FROM device_manager WHERE firebase_token = %s AND id <> %s"
    params=(firebaseToken, 0)
    mycursor.execute(query, params)
    
    res = mycursor.fetchone()
    mycursor.reset()
    return res

def getLastestRecord(firebaseToken):
    get = getUserInfo(firebaseToken)
    deviceId = get[0]
    userId = get[1]
    query=f"SELECT id, avg_heartbeat, time, latitude, longitude, prediction FROM hr_data WHERE user_id = '{userId}' ORDER BY time DESC LIMIT 1 "
    mycursor.execute(query)
    res = mycursor.fetchone()
    mycursor.reset()
    if res:
        recordId = res[0]
        avg_heartbeat = res[1]
        date_time = res[2].strftime("%Y-%m-%d %H:%M:%S")
        # stress_level = res[2]
        latitude = res[3]
        longitude = res[4]
        prediction = res[5]
        return [avg_heartbeat, date_time, latitude, longitude, deviceId, userId, prediction, recordId]
    else:
        return []
    
