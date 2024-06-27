import firebase_admin
from firebase_admin import credentials, messaging
from pathlib import Path

mypath = Path().absolute()
cred = credentials.Certificate(mypath/'config/serviceAccountKey.json')
# cred = credentials.Certificate("D:\Python\hrv_server\TestServer\config\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

firebaseTokenArr = []

def sendPush(title, msg, registration_token):
    message = messaging.MulticastMessage(
        # notification=messaging.Notification(title=title, body=msg),
        data={
            "data": msg
        },
        tokens=registration_token
    )

    response = messaging.send_multicast(message)
    print("Sent " + msg + " with token: " + registration_token[0])
    return "Sent " + msg + " with token: " + registration_token[0]