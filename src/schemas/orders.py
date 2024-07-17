from pydantic import BaseModel


class Order(BaseModel):
    user_id: int
    room_id: int
    service_id: int
    order_status: str


class OrderOut(Order):
    id: int
