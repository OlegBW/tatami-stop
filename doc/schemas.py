from pydantic import BaseModel, EmailStr
import datetime


# class UserBase(BaseModel):
#     class Config:
#         from_attributes = True


# class UserRegistrationIn(UserBase):
#     username: str
#     full_name: str
#     password: str
#     email: EmailStr


# class UserRegistrationOut(UserBase):
#     id: int
#     username: str
#     full_name: str
#     email: EmailStr


# class UserLoginBase(UserBase):
#     password: str


# class UserLoginEmailIn(UserLoginBase):
#     email: EmailStr


# class UserLoginUserNameIn(UserLoginBase):
#     username: str


# class UserLoginOut(UserBase):
#     id: int
#     email_or_username: EmailStr | str


# class RoomPhoto(BaseModel):
#     id: int
#     room_id: int
#     photo_url: str

#     class Config:
#         from_attributes = True


# class Room(BaseModel):
#     id: int
#     room_number: str
#     room_description: str
#     room_type: str
#     bed_count: int
#     price: float
#     facilities: str
#     is_available: bool

#     photos: list[RoomPhoto] = []

#     class Config:
#         from_attributes = True


# class RoomService(BaseModel):
#     id: int
#     room_service_name: str
#     room_service_description: str
#     price: float
#     is_available: bool

#     class Config:
#         from_attributes = True


# class service_order(BaseModel):
#     id: int
#     user_id: int
#     room_id: int
#     service_id: int
#     order_date: datetime.datetime
#     order_status: str = "in processing"


# class booking(BaseModel):
#     id: int
#     user_id: int
#     room_id: int
#     booking_date: datetime.datetime
#     check_in_date: datetime.datetime
#     check_out_date: datetime.datetime
