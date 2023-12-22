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


def get_item(model, db: Session, item_id):
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Missing item, wrong id"
        )

    return item_data


get_user = partial(get_item, models.Users)
get_order = partial(get_item, models.ServicesOrders)
get_room = partial(get_item, models.Rooms)
get_room_photo = partial(get_item, models.RoomsPhotos)
get_service = partial(get_item, models.RoomsServices)
get_booking = partial(get_item, models.Bookings)


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
get_rooms_photos = partial(get_items, models.RoomsPhotos)
get_services = partial(get_items, models.RoomsServices)
get_bookings = partial(get_items, models.Bookings)


def delete_item(model, db: Session, item_id: int):
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    db.delete(item_data)
    db.commit()


delete_user = partial(delete_item, models.Users)
delete_order = partial(delete_item, models.ServicesOrders)
delete_room = partial(delete_item, models.Rooms)
delete_room_photo = partial(delete_item, models.RoomsPhotos)
delete_service = partial(delete_item, models.RoomsServices)
delete_booking = partial(delete_item, models.Bookings)


def update_item(model, db: Session, item_id: int, new_data):
    new_data_dict = new_data.model_dump()
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    for key, value in new_data_dict.items():
        setattr(item_data, key, value)

    db.commit()
    return item_data


update_user = partial(update_item, models.Users)
update_order = partial(update_item, models.ServicesOrders)
update_room = partial(update_item, models.Rooms)
update_room_photo = partial(update_item, models.RoomsPhotos)
update_service = partial(update_item, models.RoomsServices)
update_booking = partial(update_item, models.Bookings)
