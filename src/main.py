from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from . import models  # noqa: E402
from .database import engine  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from .routers import (  # noqa: E402
    oauth_router,
    users_router,
    rooms_router,
    bookings_router,
    services_router,
    orders_router,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)

app.include_router(oauth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(services_router)
app.include_router(orders_router)
