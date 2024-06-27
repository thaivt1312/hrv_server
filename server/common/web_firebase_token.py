from config.FCMManage import sendPush 

firebaseTokenArr = []

def getIndex(user_id):
    for i in range(len(firebaseTokenArr)):
        if firebaseTokenArr[i]['user_id'] == user_id:
            return i
    return -1

def addNew(user_id, firebaseToken):
    firebaseTokenArr.append({
        "user_id": user_id,
        "firebase_token": firebaseToken
    })

def updateFirebaseToken(user_id, firebaseToken):
    index = getIndex(user_id)
    if index == -1:
        addNew(user_id, firebaseToken)
    else:
        firebaseTokenArr[index] = {
            "user_id": user_id,
            "firebase_token": firebaseToken
        }

def getFirebaseToken(user_id):
    index = getIndex(user_id)
    if index == -1:
        return ""
    else:
        return firebaseTokenArr[index]['firebase_token']
    
def sendToUser(user_id, msg):
    index = getIndex(user_id)
    if index == -1:
        return "User not login"
    else:
        token = firebaseTokenArr[index]['firebase_token']
        return sendPush('send', msg, [token])
