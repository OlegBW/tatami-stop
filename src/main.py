from fastapi import FastAPI, Depends
from . import models, schemas
from .database import engine, get_db
from .crud import create_user
from sqlalchemy.orm import Session

from .routers import oauth, users, rooms

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(oauth.router)
app.include_router(users.router)
app.include_router(rooms.router)
