from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..utils.crud import users as crud
from ..schemas import tokens
from typing import Annotated
from ..utils.password import verify_password
from ..database import get_db
import os

from typing import TypedDict

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


class TokenPayload(TypedDict):
    username: str
    role: str
    id: int


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


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


def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_credentials(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.hashed_password, password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    try:
        payload: TokenPayload = decode_access_token(token)

        id = payload["id"]
        username = payload["username"]
        user_role = payload["role"]

        token_data = tokens.TokenData(username=username, role=user_role, id=id)
    except JWTError:
        raise credentials_exception

    user = crud.get_user(db, token_data.id)
    if user is None:
        raise credentials_exception
    return user
