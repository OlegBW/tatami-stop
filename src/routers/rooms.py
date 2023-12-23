from fastapi import (
    APIRouter,
    Depends,
    Body,
    Path,
    Query,
    UploadFile,
    HTTPException,
    status,
)
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils.crud import rooms as crud
from ..schemas import rooms
from typing import Annotated
import shutil
import os

router = APIRouter(prefix="/rooms")


@router.post("/")
def add_room(room_data: rooms.RoomData, db: Session = Depends(get_db)):
    crud.create_room(db, room_data)
    return {"status": "success"}


@router.delete("/{room_id}")
def delete_room(
    room_id: Annotated[int, Path(title="Room ID")], db: Session = Depends(get_db)
):
    crud.delete_room(db, room_id)
    return {"status": "success"}


@router.put("/{room_id}")
def update_room(
    room_id: Annotated[int, Path(title="Room ID")],
    new_data: Annotated[rooms.RoomData, Body(embed=True)],
    db: Session = Depends(get_db),
):
    crud.update_room(db, room_id, new_data)
    return {"status": "success"}


@router.get("/{room_id}")
def get_room(
    room_id: Annotated[int, Path(title="Room ID")], db: Session = Depends(get_db)
):
    room_data = crud.get_room(db, room_id)
    room_data.photos
    return room_data


@router.get("/", response_model=list[rooms.RoomData])
def get_rooms(
    db: Session = Depends(get_db),
    page: Annotated[int | None, Query()] = None,
    size: Annotated[int | None, Query()] = None,
):
    if all([page, size]):
        return crud.get_rooms(db, page, size)

    return crud.get_rooms(db)


# ToDo
@router.post("/{room_id}/photos")
def create_room_photo(
    room_id: Annotated[int, Path(title="Room ID")],
    files: list[UploadFile],
    db: Session = Depends(get_db),
):
    file_exists = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="File already exists"
    )

    for file in files:
        file_path = os.path.join("static", file.filename)
        if os.path.exists(file_path):
            raise file_exists
        if crud.is_photo_url_exists(db, file_path):
            raise file_exists

        new_photo = rooms.RoomPhotoData(room_id=room_id, photo_url=file_path)
        crud.create_room_photo(db, new_photo)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"status": "success"}
