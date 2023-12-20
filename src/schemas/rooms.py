from pydantic import BaseModel


class RoomPhoto(BaseModel):
    id: int
    room_id: int
    photo_url: str

    class Config:
        from_attributes = True


class Room(BaseModel):
    id: int
    room_number: str
    room_description: str
    room_type: str
    bed_count: int
    price: float
    facilities: str
    is_available: bool

    photos: list[RoomPhoto] = []

    class Config:
        from_attributes = True
