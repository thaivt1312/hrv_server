from config.db_connect import mydb


def checklogin(passcode, deviceId):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM hrv_data")
    res = mycursor.fetchall()
    for x in res:
        print(x)