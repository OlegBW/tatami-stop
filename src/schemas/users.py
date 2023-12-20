from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    class Config:
        from_attributes = True


class UserRegistration(UserBase):
    username: str
    full_name: str
    password: str
    email: EmailStr


class UserData(UserBase):
    id: int
    username: str
    full_name: str
    email: EmailStr


class UserLoginBase(UserBase):
    password: str


class UserLoginEmail(UserLoginBase):
    email: EmailStr


class UserLoginUserName(UserLoginBase):
    username: str
