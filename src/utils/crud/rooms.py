from sqlalchemy.orm import Session
from typing import Optional
from ... import models
from fastapi import HTTPException, status
from ...schemas import rooms
from functools import partial
import os

from .generic import get_item, get_items, delete_item, update_item


def create_room(db: Session, room_data: rooms.RoomData) -> Optional[rooms.RoomDataOut]:
    room_data = room_data.model_dump()
    room_number = room_data["room_number"]

    room_match = (
        db.query(models.Rooms).filter(models.Rooms.room_number == room_number).first()
    )
    if room_match is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A room with such number already exists",
        )

    new_room = models.Rooms(**room_data)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


def create_room_photo(
    db: Session, photo_data: rooms.RoomPhotoData
) -> Optional[rooms.RoomPhoto]:
    photo_data = photo_data.model_dump()
    photo_url = photo_data["photo_url"]

    photo_match = (
        db.query(models.RoomsPhotos)
        .filter(models.RoomsPhotos.photo_url == photo_url)
        .first()
    )
    if photo_match is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A photo with such path already exists",
        )

    new_photo = models.RoomsPhotos(**photo_data)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo


def is_photo_url_exists(db: Session, photo_url: str):
    photo_data = (
        db.query(models.RoomsPhotos)
        .filter(models.RoomsPhotos.photo_url == photo_url)
        .first()
    )

    return photo_data is not None


def delete_room(db: Session, room_id: int):
    photos_data = (
        db.query(models.RoomsPhotos.photo_url)
        .filter(models.RoomsPhotos.room_id == room_id)
        .all()
    )
    item_data = db.query(models.Rooms).get(room_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    db.delete(item_data)
    db.commit()

    for photo in photos_data[0]:
        os.remove(photo)


get_room = partial(get_item, models.Rooms)
get_rooms = partial(get_items, models.Rooms)
delete_room_photo = partial(delete_item, models.RoomsPhotos)
update_room = partial(update_item, models.Rooms)
update_room_photo = partial(update_item, models.RoomsPhotos)
