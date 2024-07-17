from pydantic import BaseModel
import datetime


class Booking(BaseModel):
    # id: int
    user_id: int
    room_id: int
    # booking_date: datetime.datetime
    check_in_date: datetime.date
    check_out_date: datetime.date


class BookingOut(Booking):
    id: int
    booking_date: datetime.date
