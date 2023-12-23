from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from . import models  # noqa: E402
from .database import engine  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from .routers import oauth, users, rooms  # noqa: E402

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)

app.include_router(oauth.router)
app.include_router(users.router)
app.include_router(rooms.router)
