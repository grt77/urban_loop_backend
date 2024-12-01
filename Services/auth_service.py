from flask import request, jsonify
import jwt
from  dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone


def get_token(mobile_number):
    try:
        load_dotenv()
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        token = jwt.encode(
                    {
                        "mobile_number": mobile_number,
                        "exp": datetime.now(timezone.utc) + timedelta(minutes=120)  
                    },
                    JWT_SECRET_KEY,
                    algorithm="HS256"
                )
        return token
    except Exception as e:
        return {"Message":"Error"}


def token_required(f):
    def wrapper(*args, **kwargs):
        load_dotenv()
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"message": "Auth Token is missing"}), 401
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            request.user = data  
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Auth Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Auth Invalid token"}), 401

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
