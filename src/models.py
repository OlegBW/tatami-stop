from .database import Base
from sqlalchemy import (
    INTEGER,
    BOOLEAN,
    REAL,
    TEXT,
    DATETIME,
    DATE,
    Column,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship


class TableRepr:
    def __repr__(self):
        attrs = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        line = f'<{self.__class__.__name__} {", ".join(attrs)}>'
        return line


class Users(Base, TableRepr):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    full_name = Column(TEXT)
    username = Column(TEXT, unique=True)
    email = Column(TEXT, unique=True)
    hashed_password = Column(TEXT)
    user_role = Column(TEXT, default="client")

    orders = relationship(
        "ServicesOrders", back_populates="user", cascade="all, delete"
    )
    bookings = relationship("Bookings", back_populates="user", cascade="all, delete")


class Rooms(Base, TableRepr):
    __tablename__ = "rooms"

    id = Column(INTEGER, primary_key=True, index=True)
    room_number = Column(TEXT, unique=True)
    room_description = Column(TEXT)
    room_type = Column(TEXT)
    bed_count = Column(INTEGER)
    price = Column(REAL)
    facilities = Column(TEXT)
    is_available = Column(BOOLEAN)

    photos = relationship("RoomsPhotos", back_populates="room", cascade="all, delete")
    orders = relationship(
        "ServicesOrders", back_populates="room", cascade="all, delete"
    )
    bookings = relationship("Bookings", back_populates="room", cascade="all, delete")


class RoomsPhotos(Base, TableRepr):
    __tablename__ = "rooms_photos"

    id = Column(INTEGER, primary_key=True, index=True)
    room_id = Column(
        INTEGER,
        ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    photo_url = Column(TEXT, unique=True)

    room = relationship("Rooms", back_populates="photos", cascade="all, delete")


class RoomsServices(Base, TableRepr):
    __tablename__ = "rooms_services"

    id = Column(INTEGER, primary_key=True, index=True)
    room_service_name = Column(TEXT, unique=True)
    room_service_description = Column(TEXT)
    price = Column(REAL)
    is_available = Column(BOOLEAN)

    orders = relationship(
        "ServicesOrders", back_populates="service", cascade="all, delete"
    )


class ServicesOrders(Base, TableRepr):
    __tablename__ = "services_orders"

    id = Column(INTEGER, primary_key=True, index=True)
    user_id = Column(
        INTEGER,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    room_id = Column(
        INTEGER,
        ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    service_id = Column(
        INTEGER,
        ForeignKey("rooms_services.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    order_date = Column(DATETIME, default=func.now())
    order_status = Column(TEXT, default="in processing")

    user = relationship("Users", back_populates="orders", cascade="all, delete")
    room = relationship("Rooms", back_populates="orders", cascade="all, delete")
    service = relationship(
        "RoomsServices", back_populates="orders", cascade="all, delete"
    )


class Bookings(Base, TableRepr):
    __tablename__ = "bookings"

    id = Column(INTEGER, primary_key=True, index=True)
    user_id = Column(
        INTEGER,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    room_id = Column(
        INTEGER,
        ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    booking_date = Column(DATE, default=func.current_date())
    check_in_date = Column(DATE)
    check_out_date = Column(DATE)

    user = relationship("Users", back_populates="bookings", cascade="all, delete")
    room = relationship("Rooms", back_populates="bookings", cascade="all, delete")
