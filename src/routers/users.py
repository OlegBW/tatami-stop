from fastapi import APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import crud
from ..schemas import users

router = APIRouter()


@router.get("/users", response_model=list[users.UserData])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
