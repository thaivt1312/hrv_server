from config.db_connect import mydb

def insertNewUser(deviceId, firebaseToken):
    mycursor = mydb.cursor()
    query = """INSERT INTO device_manager (device_id, firebase_token) VALUES (%s, %s)"""
    params=(deviceId, firebaseToken)
    mycursor.execute(query, params)
    mydb.commit()
    
def updateFirebaseToken(deviceId, firebaseToken):
    mycursor = mydb.cursor()
    query = """UPDATE device_manager SET firebase_token=%s WHERE device_id=%s AND id <> 0"""
    mycursor.execute(query, [firebaseToken, deviceId])
    mydb.commit()
    
def saveHeartRateData(params):
    mycursor = mydb.cursor()
    query = """INSERT INTO hr_data 
        (device_id, user_id, time, avg_heartbeat, latitude, longitude, prediction) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    mycursor.execute(query, params)
    mydb.commit()
    
def updatePrediction(recordId, prediction, latitude, longitude):
    mycursor = mydb.cursor()
    query = """UPDATE hr_data SET prediction=%s, latitude=%s, longitude=%s WHERE id=%s"""
    mycursor.execute(query, [prediction, latitude, longitude, recordId])
    mydb.commit()
    