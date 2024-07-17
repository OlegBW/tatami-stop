from pydantic import BaseModel, EmailStr


class OrmModel:
    class Config:
        from_attributes = True


class UserRegistration(BaseModel, OrmModel):
    username: str
    full_name: str
    password: str
    email: EmailStr


class UserData(BaseModel, OrmModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    user_role: str


# class UserLoginBase(UserBase):
#     password: str


# class UserLoginEmail(UserLoginBase):
#     email: EmailStr


# class UserLoginUserName(UserLoginBase):
#     username: str
