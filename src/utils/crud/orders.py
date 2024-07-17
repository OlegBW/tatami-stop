from .generic import get_item, get_items, update_item, delete_item, create_item
from functools import partial
from ... import models

get_order = partial(get_item, models.ServicesOrders)
get_orders = partial(get_items, models.ServicesOrders)
update_order = partial(update_item, models.ServicesOrders)
delete_order = partial(delete_item, models.ServicesOrders)
create_order = partial(create_item, models.ServicesOrders)
