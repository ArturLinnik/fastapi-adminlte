
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from .util import OAuth2PasswordBearerWithCookie

SECRET_KEY = "253c7198aef00ddf07d524fbfa7b4861e66190c0c22c377e92ecb2730247bb1d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt