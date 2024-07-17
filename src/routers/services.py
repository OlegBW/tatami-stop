from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.crud import services as crud
from ..schemas import services
from typing import List

router = APIRouter()


@router.get("/service/{service_id}", response_model=services.RoomServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    return crud.get_service(db, service_id)


@router.get("/service", response_model=List[services.RoomServiceOut])
def get_services(page: int, size: int, db: Session = Depends(get_db)):
    return crud.get_services(db, page, size)


@router.post("/service", response_model=services.RoomServiceOut)
def create_service(new_service: services.RoomService, db: Session = Depends(get_db)):
    print(new_service)
    return crud.create_service(db, new_service)


@router.put("/service/{service_id}", response_model=services.RoomServiceOut)
def update_service(
    service_id: int, new_service: services.RoomService, db: Session = Depends(get_db)
):
    return crud.update_service(db, service_id, new_service)


@router.delete("/service/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    crud.delete_service(db, service_id)
    return {"success": True}
