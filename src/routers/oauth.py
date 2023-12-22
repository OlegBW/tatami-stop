from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import tokens, users
from typing import Annotated
from ..utils.token import access_token_expires, create_access_token
from ..utils.token import authenticate_user, get_current_user

router = APIRouter()


@router.post("/token", response_model=tokens.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
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


# @router.get("/users/me/", response_model=users.UserData)
# async def read_users_me(
#     current_user: Annotated[users.UserData, Depends(get_current_user)],
# ):
#     return current_user
