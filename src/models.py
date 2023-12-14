from .database import Base
from sqlalchemy import INTEGER, BOOLEAN, REAL, TEXT, DATETIME, Column, ForeignKey
from sqlalchemy.orm import relationship


class TableRepr:
    def __repr__(self):
        attrs = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        line = f'<{self.__class__.__name__} {", ".join(attrs)}>'
        return line


class User(Base, TableRepr):
    __tablename__ = "user"

    id = Column(INTEGER, primary_key=True, index=True)
    full_name = Column(TEXT)
    username = Column(TEXT, unique=True)
    email = Column(TEXT, unique=True)
    hashed_password = Column(TEXT)
    user_role = Column(TEXT)

    orders = relationship("ServiceOrder", back_populates="user")
    bookings = relationship("Booking", back_populates="user")


class Room(Base, TableRepr):
    __tablename__ = "room"

    id = Column(INTEGER, primary_key=True, index=True)
    room_number = Column(TEXT, unique=True)
    room_description = Column(TEXT)
    room_type = Column(TEXT)
    bed_count = Column(INTEGER)
    price = Column(REAL)
    facilities = Column(TEXT)
    is_available = Column(BOOLEAN)

    photos = relationship("RoomPhoto", back_populates="room")
    orders = relationship("ServiceOrder", back_populates="room")
    bookings = relationship("Booking", back_populates="room")


class RoomPhoto(Base, TableRepr):
    __tablename__ = "room_photo"

    id = Column(INTEGER, primary_key=True, index=True)
    room_id = Column(
        INTEGER,
        ForeignKey("room.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    photo_url = Column(TEXT)

    room = relationship("Room", back_populates="photos")


class RoomService(Base, TableRepr):
    __tablename__ = "room_service"

    id = Column(INTEGER, primary_key=True, index=True)
    room_service_name = Column(TEXT, unique=True)
    room_service_description = Column(TEXT)
    price = Column(REAL)
    is_available = Column(BOOLEAN)

    orders = relationship("ServiceOrder", back_populates="service")


class ServiceOrder(Base, TableRepr):
    __tablename__ = "service_order"

    id = Column(INTEGER, primary_key=True, index=True)
    user_id = Column(
        INTEGER,
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    room_id = Column(
        INTEGER,
        ForeignKey("room.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    service_id = Column(
        INTEGER,
        ForeignKey("room_service.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    order_date = Column(DATETIME, default=DATETIME("now"))
    order_status = Column(TEXT, default="in processing")

    user = relationship("User", back_populates="orders")
    room = relationship("Room", back_populates="orders")
    service = relationship("RoomService", back_populates="orders")


class Booking(Base, TableRepr):
    __tablename__ = "booking"

    id = Column(INTEGER, primary_key=True, index=True)
    user_id = Column(
        INTEGER,
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    room_id = Column(
        INTEGER,
        ForeignKey("room.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    booking_date = Column(DATETIME, default=DATETIME("now"))
    check_in_date = Column(DATETIME)
    check_out_date = Column(DATETIME)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
