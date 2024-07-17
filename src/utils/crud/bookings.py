from .generic import create_item, delete_item, get_item, get_items, update_item
from functools import partial
from ... import models

create_booking = partial(create_item, models.Bookings)
delete_booking = partial(delete_item, models.Bookings)
update_booking = partial(update_item, models.Bookings)
get_booking = partial(get_item, models.Bookings)
get_bookings = partial(get_items, models.Bookings)
