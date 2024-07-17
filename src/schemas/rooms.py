from pydantic import BaseModel
from typing import List


class OrmModel:
    class Config:
        from_attributes = True


class RoomPhotoData(BaseModel):
    room_id: int
    photo_url: str


class RoomPhoto(OrmModel, RoomPhotoData):
    id: int


class RoomData(BaseModel):
    room_number: str
    room_description: str
    room_type: str
    bed_count: int
    price: float
    facilities: str
    is_available: bool


class RoomDataUpdate(BaseModel):
    room_number: str | None = None
    room_description: str | None = None
    room_type: str | None = None
    bed_count: int | None = None
    price: float | None = None
    facilities: str | None = None
    is_available: bool | None = None


class RoomDataOut(RoomData):
    id: int
    photos: List[RoomPhoto]


class Room(OrmModel, RoomData):
    id: int
    photos: list[RoomPhoto] = []
