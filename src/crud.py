from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models
from .schemas import users, rooms, services, bookings
from pydantic import EmailStr
from functools import partial
from fastapi import HTTPException, status
from typing import Optional
from .utils.password import get_password_hash


def get_user_by_email(db: Session, user_email: EmailStr) -> Optional[models.Users]:
    user_data = db.query(models.Users).filter(models.Users.email == user_email).first()
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Missing user, wrong email"
        )

    return user_data


def get_user_by_username(db: Session, username: str) -> Optional[models.Users]:
    user_data = db.query(models.Users).filter(models.Users.username == username).first()
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Missing user, wrong username"
        )

    return user_data


def get_user_by_credentials(
    db: Session, credentials: str | EmailStr
) -> Optional[models.Users]:
    user_data = None

    if "@" in credentials:
        user_data = get_user_by_email(db, credentials)
    else:
        user_data = get_user_by_username(db, credentials)
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


def update_user(
    db: Session, user_id: int, new_data: users.UserRegistration
) -> Optional[models.Users]:
    new_data_dict = new_data.model_dump()
    user_data = db.query(models.Users).get(user_id)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    for key, value in new_data_dict.items():
        setattr(user_data, key, value)

    db.commit()
    return user_data


def delete_user(db: Session, user_id: int):
    user_data = db.query(models.Users).get(user_id)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(user_data)
    db.commit()


def create_room(db: Session, room_data: rooms.RoomData) -> Optional[rooms.RoomData]:
    room_data = room_data.model_dump()
    room_number = room_data["room_number"]

    room_match = (
        db.query(models.Rooms).filter(models.Rooms.room_number == room_number).first()
    )
    if room_match is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A room with such number already exists",
        )

    new_room = models.Rooms(**room_data)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


def delete_room(db: Session, room_id: int):
    room_data = db.query(models.Rooms).get(room_id)
    if room_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    db.delete(room_data)
    db.commit()


def update_room(
    db: Session, room_id: int, new_data: rooms.RoomData
) -> Optional[models.Users]:
    new_data_dict = new_data.model_dump()
    room_data = db.query(models.Rooms).get(room_id)
    if room_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    for key, value in new_data_dict.items():
        setattr(room_data, key, value)

    db.commit()
    return room_data


def get_item(model, db: Session, item_id):
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Missing item, wrong id"
        )

    return item_data


get_user = partial(get_item, models.Users)
get_room = partial(get_item, models.Rooms)


def get_items(model, db: Session, page: int = 0, size: int = 20):
    skip = page * size

    item_data = db.query(model).offset(skip).limit(size).all()

    if len(item_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No items found"
        )

    return item_data


get_users = partial(get_items, models.Users)
get_orders = partial(get_items, models.ServicesOrders)
get_rooms = partial(get_items, models.Rooms)
get_services = partial(get_items, models.RoomsServices)
get_bookings = partial(get_items, models.Bookings)
