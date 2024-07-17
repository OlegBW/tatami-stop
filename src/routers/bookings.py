from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import literal
from ..database import get_db
from ..schemas import bookings
from ..utils.crud import bookings as crud, rooms
from ..models import Bookings
from typing import List

router = APIRouter()


# TODO: Handle update
# TODO: Handle booking date availability
@router.post("/booking", response_model=bookings.BookingOut)
def create_booking(booking_data: bookings.Booking, db: Session = Depends(get_db)):
    room_id = booking_data.room_id
    room = rooms.get_room(db, room_id)
    if not room.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available",
            headers={"WWW-Authenticate": "Bearer"},
        )

    overlapping_bookings_query = db.query(Bookings).filter(
        Bookings.room_id == room_id,
        Bookings.check_out_date > booking_data.check_in_date,
        Bookings.check_in_date < booking_data.check_out_date,
    )

    is_match = (
        db.query(literal(True)).filter(overlapping_bookings_query.exists()).scalar()
    )
    if is_match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room booking is not available in this time range",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return crud.create_booking(db, booking_data)


@router.delete("/booking/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    crud.delete_booking(db, booking_id)
    return {"success": True}


@router.get("/booking/{booking_id}", response_model=bookings.BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    return crud.get_booking(db, booking_id)


@router.get("/booking", response_model=List[bookings.BookingOut])
def get_bookings(page: int, size: int, db: Session = Depends(get_db)):
    return crud.get_bookings(db, page, size)
