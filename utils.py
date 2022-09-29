from datetime import timedelta, datetime
import models
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expire_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username, password, session):
    db_user = session.query(models.User).filter(models.User.username==username).first()
    if not db_user:
        return False
    try:
        pass_check = pwd_context.verify(password, db_user.password)
        return pass_check
    except Exception:
        return False
