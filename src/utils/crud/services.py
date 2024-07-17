from .generic import get_item, get_items, update_item, delete_item, create_item
from sqlalchemy.orm import Session
from functools import partial
from ... import models

get_service = partial(get_item, models.RoomsServices)
get_services = partial(get_items, models.RoomsServices)
update_service = partial(update_item, models.RoomsServices)
delete_service = partial(delete_item, models.RoomsServices)
create_service = partial(create_item, models.RoomsServices)


def update_service_availability(db: Session, service_id: int, is_available: bool):
    service = get_service(db, service_id)
    service.is_available = is_available
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
