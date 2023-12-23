from fastapi import FastAPI, Depends
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from .routers import oauth, users, rooms

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)

app.include_router(oauth.router)
app.include_router(users.router)
app.include_router(rooms.router)
