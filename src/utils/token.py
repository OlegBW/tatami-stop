from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "e13009ab11178f287f8cdee033193484af625ed09b2d77543f8d531bf11fdd9e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
