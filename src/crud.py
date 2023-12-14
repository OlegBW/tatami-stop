from sqlalchemy.orm import Session
from . import models, schemas
from argon2 import PasswordHasher
from pydantic import EmailStr
from functools import partial

ph = PasswordHasher()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: EmailStr):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user_data: schemas.UserRegistrationIn):
    user_data = user_data.model_dump()
    hashed_password = ph.hash(user_data["password"])
    
    user_data = {k:v for k,v in user_data.items() if k != 'password'}

    new_user = models.User(**(user_data), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, id: int, new_data: schemas.UserRegistrationIn):
    new_data_dict = new_data.model_dump()
    user_data = db.query(models.User).get(id)
    user_data.update(new_data_dict)
    db.commit()
    return user_data


def delete_user(db: Session, id: int):
    user_data = db.query(models.User).get(id)
    db.delete(user_data)
    db.commit()


# def login_user(db: Session, login_data: schemas.UserLoginEmailIn | schemas.UserLoginUserNameIn):
#     login_data_dict = login_data.model_dump()
#     user_data = None

#     if 'email' in login_data_dict:
#         user_data = get_user_by_email(db, login_data_dict['email'])
#     else:
#         user_data = get_user_by_username(db, login_data_dict['username'])

#     if user_data is None:
#         return False

#     is_valid = ph.verify(user_data.hashed_password, login_data_dict['password'])
#     return is_valid


def get_items(model, db: Session, skip: int, limit: int):
    return db.query(model).offset(skip).limit(limit).all()


get_users = partial(get_items, models.User)
get_orders = partial(get_items, models.ServiceOrder)
get_rooms = partial(get_items, models.Room)
get_services = partial(get_items, models.RoomService)
get_bookings = partial(get_items, models.Booking)
