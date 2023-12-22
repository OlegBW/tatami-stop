from pydantic import BaseModel


class OrmModel:
    class Config:
        from_attributes = True


class RoomPhoto(BaseModel, OrmModel):
    id: int
    room_id: int
    photo_url: str


class RoomData(BaseModel):
    id: int
    room_number: str
    room_description: str
    room_type: str
    bed_count: int
    price: float
    facilities: str
    is_available: bool


class Room(OrmModel, RoomData):
    photos: list[RoomPhoto] = []
