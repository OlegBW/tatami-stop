from fastapi import APIRouter, Depends, Body, Path, Query
from ..database import get_db
from sqlalchemy.orm import Session
from .. import crud
from ..schemas import rooms
from typing import Annotated


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


@router.get("/{room_id}", response_model=rooms.RoomData)
def get_room(
    room_id: Annotated[int, Path(title="Room ID")], db: Session = Depends(get_db)
):
    return crud.get_room(db, room_id)


@router.get("/", response_model=list[rooms.RoomData])
def get_rooms(
    db: Session = Depends(get_db),
    page: Annotated[int | None, Query()] = None,
    size: Annotated[int | None, Query()] = None,
):
    if all([page, size]):
        return crud.get_rooms(db, page, size)

    return crud.get_rooms(db)
