from fastapi import (
    APIRouter,
    Depends,
    Body,
    Path,
    Query,
    UploadFile,
    HTTPException,
    status,
    Form,
    File,
)
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils.crud import rooms as crud
from ..schemas import rooms
from typing import Annotated
import shutil
import os

router = APIRouter(prefix="/rooms")


@router.delete("/{room_id}")
def delete_room(
    room_id: Annotated[int, Path(title="Room ID")], db: Session = Depends(get_db)
):
    crud.delete_room(db, room_id)
    return {"status": "success"}


@router.put("/{room_id}")
def update_room(
    room_id: Annotated[int, Path()],
    room_number: Annotated[str, Form()],
    room_description: Annotated[str, Form()],
    room_type: Annotated[str, Form()],
    bed_count: Annotated[int, Form()],
    price: Annotated[float, Form()],
    facilities: Annotated[str, Form()],
    is_available: Annotated[bool, Form()],
    files: Annotated[list[UploadFile], File()],
    db: Session = Depends(get_db),
):
    room_data = crud.get_room(db, room_id)
    room_id = room_data.id
    room_photos = room_data.photos

    new_data = {
        "room_number": room_number,
        "room_description": room_description,
        "room_type": room_type,
        "bed_count": bed_count,
        "price": price,
        "facilities": facilities,
        "is_available": is_available,
    }
    crud.update_room(db, room_id, rooms.RoomData(**new_data))

    file_exists = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="File already exists"
    )

    # Delete existing data!
    for room_photo in room_photos:
        file_path = room_photo.photo_url
        if os.path.exists(file_path):
            os.remove(file_path)

    crud.delete_room_photos(db, room_id)

    for file in files:
        file_path = os.path.join("static/uploads/rooms", file.filename)
        if os.path.exists(file_path):
            raise file_exists
        if crud.is_photo_url_exists(db, file_path):
            raise file_exists

        new_photo = rooms.RoomPhotoData(room_id=room_id, photo_url=file_path)
        crud.create_room_photo(db, new_photo)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"status": "success"}


@router.get("/{room_id}", response_model=rooms.RoomDataOut)
def get_room(
    room_id: Annotated[int, Path(title="Room ID")], db: Session = Depends(get_db)
):
    room_data = crud.get_room(db, room_id)
    room_data.photos
    return room_data


@router.get("/", response_model=list[rooms.RoomDataOut])
def get_rooms(
    db: Session = Depends(get_db),
    page: Annotated[int | None, Query()] = None,
    size: Annotated[int | None, Query()] = None,
):
    if all([page, size]):
        return crud.get_rooms(db, page, size)

    return crud.get_rooms(db)


@router.post("/")
def add_room_data(
    room_number: Annotated[str, Form()],
    room_description: Annotated[str, Form()],
    room_type: Annotated[str, Form()],
    bed_count: Annotated[int, Form()],
    price: Annotated[float, Form()],
    facilities: Annotated[str, Form()],
    is_available: Annotated[bool, Form()],
    files: Annotated[list[UploadFile], File()],
    db: Session = Depends(get_db),
):
    room_data = {
        "room_number": room_number,
        "room_description": room_description,
        "room_type": room_type,
        "bed_count": bed_count,
        "price": price,
        "facilities": facilities,
        "is_available": is_available,
    }

    new_room = crud.create_room(db, rooms.RoomData(**room_data))
    room_id = new_room.id

    file_exists = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="File already exists"
    )

    for file in files:
        file_path = os.path.join("static/uploads/rooms", file.filename)
        if os.path.exists(file_path):
            raise file_exists
        if crud.is_photo_url_exists(db, file_path):
            raise file_exists

        new_photo = rooms.RoomPhotoData(room_id=room_id, photo_url=file_path)
        crud.create_room_photo(db, new_photo)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"status": "success"}
