from pydantic import BaseModel
import datetime


class RoomService(BaseModel):
    id: int
    room_service_name: str
    room_service_description: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True


class ServiceOrder(BaseModel):
    id: int
    user_id: int
    room_id: int
    service_id: int
    order_date: datetime.datetime
    order_status: str = "in processing"
