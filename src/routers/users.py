from fastapi import APIRouter, Depends, Body, Path, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import crud
from ..schemas import tokens, users
from typing import Annotated
from ..utils.password import verify_password
from ..utils.token import decode_access_token, access_token_expires, create_access_token
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


def authenticate_user(db: Session, username_or_email: str, password: str):
    user = crud.get_user_by_credentials(db, username_or_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.hashed_password, password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
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


@router.get("/users", response_model=list[users.UserData])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.post("/users/registration")
def register_user(
    user_data: Annotated[users.UserRegistration, Body(embed=True)],
    db: Session = Depends(get_db),
):
    crud.create_user(db, user_data)
    return {"status": "success"}


@router.post("/users/{user_id}", response_model=users.UserData)
def get_user(
    user_id: Annotated[int, Path(title="The ID of the user")],
    db: Session = Depends(get_db),
):
    return crud.get_user(db, user_id)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: Annotated[int, Path(title="The ID of the user")],
    db: Session = Depends(get_db),
):
    crud.delete_user(db, user_id)
    return {"status": "success"}


@router.put("/users/{user_id}")
def update_user(
    user_id: Annotated[int, Path(title="The ID of the user")],
    new_data: Annotated[users.UserRegistration, Body(embed=True)],
    db: Session = Depends(get_db),
):
    crud.update_user(db, user_id, new_data)
    return {"status": "success"}

@router.post("/token", response_model=tokens.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=users.UserData)
async def read_users_me(
    current_user: Annotated[users.UserData, Depends(get_current_user)]
):
    return current_user