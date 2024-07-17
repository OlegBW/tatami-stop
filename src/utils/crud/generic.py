from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import TypeVar

M = TypeVar("M", bound=BaseModel)


def get_item(model, db: Session, item_id: int):
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Missing item, wrong id"
        )

    return item_data


def get_items(model, db: Session, page: int = 0, size: int = 20):
    skip = page * size

    item_data = db.query(model).offset(skip).limit(size).all()

    if len(item_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No items found"
        )

    return item_data


def delete_item(model, db: Session, item_id: int):
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    db.delete(item_data)
    db.commit()


def update_item(model, db: Session, item_id: int, new_data: M):
    new_data_dict = new_data.model_dump()
    item_data = db.query(model).get(item_id)
    if item_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    for key, value in new_data_dict.items():
        if value is not None:
            setattr(item_data, key, value)

    db.commit()
    db.refresh(item_data)
    return item_data


def create_item(model, db: Session, new_data: M):
    new_data_dict = new_data.model_dump()
    new_item = model(**new_data_dict)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
