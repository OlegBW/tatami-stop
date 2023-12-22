from fastapi import APIRouter, Depends, Body, Path, Query
from ..database import get_db
from sqlalchemy.orm import Session
from .. import crud
from ..schemas import users
from typing import Annotated


router = APIRouter()


@router.get("/users", response_model=list[users.UserData])
def get_users(
    db: Session = Depends(get_db),
    page: Annotated[int | None, Query()] = None,
    size: Annotated[int | None, Query()] = None,
):
    return crud.get_users(db, page, size)


@router.post("/users/registration")
def register_user(
    user_data: Annotated[users.UserRegistration, Body(embed=True)],
    db: Session = Depends(get_db),
):
    crud.create_user(db, user_data)
    return {"status": "success"}


@router.post("/users/{user_id}", response_model=users.UserData)
def get_user(
    user_id: Annotated[int, Path(title="The ID of the user")],
    db: Session = Depends(get_db),
):
    return crud.get_user(db, user_id)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: Annotated[int, Path(title="The ID of the user")],
    db: Session = Depends(get_db),
):
    crud.delete_user(db, user_id)
    return {"status": "success"}


@router.put("/users/{user_id}")
def update_user(
    user_id: Annotated[int, Path(title="The ID of the user")],
    new_data: Annotated[users.UserRegistration, Body(embed=True)],
    db: Session = Depends(get_db),
):
    crud.update_user(db, user_id, new_data)
    return {"status": "success"}
