import jwt
from datetime import datetime, timedelta
from flask import current_app

def generar_token(user_id, role):
    payload = {
        'sub': user_id,
        'role': role,
        'exp': datetime.now() + timedelta(hours=2)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verificar_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None