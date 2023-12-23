from pydantic import BaseModel


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


class RoomDataOut(RoomData):
    id: int


class Room(OrmModel, RoomData):
    id: int
    photos: list[RoomPhoto] = []
