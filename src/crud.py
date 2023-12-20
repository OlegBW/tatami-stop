from sqlalchemy.orm import Session
from . import models
from .schemas import users, rooms, services, bookings
from argon2 import PasswordHasher
from pydantic import EmailStr
from functools import partial

ph = PasswordHasher()


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, user_email: EmailStr):
    return db.query(models.Users).filter(models.Users.email == user_email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()


def create_user(db: Session, user_data: users.UserRegistration):
    user_data = user_data.model_dump()
    hashed_password = ph.hash(user_data["password"])

    user_data = {k: v for k, v in user_data.items() if k != "password"}

    new_user = models.Users(**(user_data), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, id: int, new_data: users.UserRegistration):
    new_data_dict = new_data.model_dump()
    user_data = db.query(models.Users).get(id)
    user_data.update(new_data_dict)
    db.commit()
    return user_data


def delete_user(db: Session, id: int):
    user_data = db.query(models.Users).get(id)
    db.delete(user_data)
    db.commit()


def get_items(model, db: Session, skip: int = 0, limit: int = 20):
    return db.query(model).offset(skip).limit(limit).all()


get_users = partial(get_items, models.Users)
get_orders = partial(get_items, models.ServicesOrders)
get_rooms = partial(get_items, models.Rooms)
get_services = partial(get_items, models.RoomsServices)
get_bookings = partial(get_items, models.Bookings)
