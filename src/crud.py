from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models
from .schemas import users, rooms, services, bookings
from argon2 import PasswordHasher
from pydantic import EmailStr
from functools import partial
from fastapi import HTTPException
from typing import Optional

ph = PasswordHasher()


def get_user(db: Session, user_id: int) -> Optional[models.Users]:
    user_data = db.query(models.Users).get(user_id)
    if user_data is None:
        raise HTTPException(status_code=404, detail="Missing user, wrong id")

    return user_data


def get_user_by_email(db: Session, user_email: EmailStr) -> Optional[models.Users]:
    user_data = db.query(models.Users).filter(models.Users.email == user_email).first()
    if user_data is None:
        raise HTTPException(status_code=404, detail="Missing user, wrong email")

    return user_data


def get_user_by_username(db: Session, username: str) -> Optional[models.Users]:
    user_data = db.query(models.Users).filter(models.Users.username == username).first()
    if user_data is None:
        raise HTTPException(status_code=404, detail="Missing user, wrong username")

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

    if user_match is None:
        raise HTTPException(
            status_code=409, detail="A user with such credentials already exists"
        )

    hashed_password = ph.hash(user_data["password"])

    user_data = {k: v for k, v in user_data.items() if k != "password"}

    new_user = models.Users(**(user_data), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(
    db: Session, user_id: int, new_data: users.UserRegistration
) -> Optional[models.Users]:
    new_data_dict = new_data.model_dump()
    user_data = db.query(models.Users).get(user_id)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data.update(new_data_dict)
    db.commit()
    return user_data


def delete_user(db: Session, user_id: int):
    user_data = db.query(models.Users).get(user_id)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_data)
    db.commit()


def get_items(model, db: Session, skip: int = 0, limit: int = 20):
    item_data = db.query(model).offset(skip).limit(limit).all()

    if len(item_data) == 0:
        raise HTTPException(status_code=404, detail="No items found")

    return item_data


get_users = partial(get_items, models.Users)
get_orders = partial(get_items, models.ServicesOrders)
get_rooms = partial(get_items, models.Rooms)
get_services = partial(get_items, models.RoomsServices)
get_bookings = partial(get_items, models.Bookings)
