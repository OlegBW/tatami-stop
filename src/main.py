from fastapi import FastAPI, Depends
from . import models, schemas
from .database import engine, get_db
from .crud import create_user
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
