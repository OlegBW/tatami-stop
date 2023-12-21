from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import crud
from ..schemas import tokens
from typing import Annotated
from ..utils.password import verify_password
from ..database import get_db

SECRET_KEY = "e13009ab11178f287f8cdee033193484af625ed09b2d77543f8d531bf11fdd9e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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


def authenticate_user(db: Session, username_or_email: str, password: str):
    user = crud.get_user_by_credentials(db, username_or_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.hashed_password, password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username_or_email: str = payload.get("sub")
        if username_or_email is None:
            raise credentials_exception
        token_data = tokens.TokenData(username_or_email=username_or_email)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_credentials(db, token_data.username_or_email)
    if user is None:
        raise credentials_exception
    return user
