from pydantic import BaseModel
import datetime


class booking(BaseModel):
    id: int
    user_id: int
    room_id: int
    booking_date: datetime.datetime
    check_in_date: datetime.datetime
    check_out_date: datetime.datetime
