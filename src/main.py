from fastapi import FastAPI
from . import models
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
