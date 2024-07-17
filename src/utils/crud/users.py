from sqlalchemy.orm import Session
from typing import Optional
from ... import models
from fastapi import HTTPException, status
from ...schemas import users
from sqlalchemy import or_
from functools import partial
from ..password import get_password_hash

from .generic import get_item, get_items, delete_item, update_item


# def get_user_by_email(db: Session, user_email: EmailStr) -> Optional[models.Users]:
#     user_data = db.query(models.Users).filter(models.Users.email == user_email).first()
#     if user_data is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Missing user, wrong email"
#         )

#     return user_data


def get_user_by_email(db: Session, email: str) -> Optional[models.Users]:
    user_data = db.query(models.Users).filter(models.Users.email == email).first()
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Missing user, wrong email"
        )

    return user_data


def get_user_by_credentials(db: Session, credentials: str) -> Optional[models.Users]:
    user_data = get_user_by_email(db, credentials)
    return user_data


def create_user(
    db: Session, user_data: users.UserRegistration
) -> Optional[models.Users]:
    user_data = user_data.model_dump()

    username = user_data["username"]
    email = user_data["email"]

    user_match = (
        db.query(models.Users)
        .filter(or_(models.Users.username == username, models.Users.email == email))
        .first()
    )

    if user_match is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with such credentials already exists",
        )

    hashed_password = get_password_hash(user_data["password"])

    # user_data = {k: v for k, v in user_data.items() if k != "password"}
    del user_data["password"]

    new_user = models.Users(**(user_data), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


get_user = partial(get_item, models.Users)
get_users = partial(get_items, models.Users)
delete_user = partial(delete_item, models.Users)
update_user = partial(update_item, models.Users)
