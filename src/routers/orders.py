from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.crud import orders as crud
from ..schemas import orders
from typing import List

router = APIRouter()


@router.get("/order/{order_id}", response_model=orders.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)


@router.get("/order", response_model=List[orders.OrderOut])
def get_orders(page: int, size: int, db: Session = Depends(get_db)):
    return crud.get_orders(db, page, size)


@router.post("/order", response_model=orders.OrderOut)
def create_order(new_order: orders.Order, db: Session = Depends(get_db)):
    print(new_order)
    return crud.create_order(db, new_order)


@router.put("/order/{order_id}", response_model=orders.OrderOut)
def update_order(order_id: int, new_order: orders.Order, db: Session = Depends(get_db)):
    return crud.update_order(db, order_id, new_order)


@router.delete("/order/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    crud.delete_order(db, order_id)
    return {"success": True}
