import jwt
import datetime

from config.msg import TOKEN_EXPIRED, INVALID_TOKEN
SECRET_KEY = '20194667_DATN_20232'

def create_token(user_id, account_type):
    payload = {
        'user_id': user_id,
        'account_type': account_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expires in 1 day
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        print(TOKEN_EXPIRED)
        return {
            "user_id": None,
            "msg": TOKEN_EXPIRED
        }
    except jwt.InvalidTokenError:
        print(INVALID_TOKEN)
        return {
            "user_id": None,
            "msg": INVALID_TOKEN
        }