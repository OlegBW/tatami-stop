from .generic import get_item, get_items, update_item, delete_item, create_item
from functools import partial
from ... import models

get_service = partial(get_item, models.RoomsServices)
get_services = partial(get_items, models.RoomsServices)
update_service = partial(update_item, models.RoomsServices)
delete_service = partial(delete_item, models.RoomsServices)
create_service = partial(create_item, models.RoomsServices)
