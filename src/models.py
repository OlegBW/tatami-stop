from .database import Base
from sqlalchemy import INTEGER, BOOLEAN, REAL, TEXT, DATETIME, Column, ForeignKey
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
    user_role = Column(TEXT)

    orders = relationship("ServicesOrders", back_populates="user")
    bookings = relationship("Bookings", back_populates="user")


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

    photos = relationship("RoomsPhotos", back_populates="room")
    orders = relationship("ServicesOrders", back_populates="room")
    bookings = relationship("Bookings", back_populates="room")


class RoomsPhotos(Base, TableRepr):
    __tablename__ = "rooms_photos"

    id = Column(INTEGER, primary_key=True, index=True)
    room_id = Column(
        INTEGER,
        ForeignKey("room.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    photo_url = Column(TEXT)

    room = relationship("Rooms", back_populates="photos")


class RoomsServices(Base, TableRepr):
    __tablename__ = "rooms_services"

    id = Column(INTEGER, primary_key=True, index=True)
    room_service_name = Column(TEXT, unique=True)
    room_service_description = Column(TEXT)
    price = Column(REAL)
    is_available = Column(BOOLEAN)

    orders = relationship("ServicesOrders", back_populates="service")


class ServicesOrders(Base, TableRepr):
    __tablename__ = "services_orders"

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

    user = relationship("Users", back_populates="orders")
    room = relationship("Rooms", back_populates="orders")
    service = relationship("RoomsServices", back_populates="orders")


class Bookings(Base, TableRepr):
    __tablename__ = "bookings"

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

    user = relationship("Users", back_populates="bookings")
    room = relationship("Rooms", back_populates="bookings")
