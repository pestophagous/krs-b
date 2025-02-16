import copy
import logging
import math
import random
from dataclasses import dataclass, field

# @dataclass(eq=True, frozen=True)
# @dataclass gives us __repr__ printability for free
# (eq=True, frozen=True) gives us hashability

logger = logging.getLogger('krs_studying.' + __name__)


@dataclass
class Item:
    unique_id: str = field(init=True)
    answer: str = field(init=True)
    tags: list = field(init=True)
    prompt: str = field(init=True)


class Set:
    def __init__(self):
        self._items = []
        self._item_ids = {}

    def get_all_items(self):
        return copy.deepcopy(self._items)

    def append(self, item):
        if item.unique_id in self._item_ids:
            raise ValueError(f"Duplicate id not allowed: {item.unique_id}")

        self._item_ids[item.unique_id] = 1
        self._items.append(item)

    def union(self, other_set, *, fail_on_duplicate=True):
        for item in other_set._items:
            try:
                self.append(item)
            except ValueError as e:
                if fail_on_duplicate:
                    raise e

    def drop_all_but(self, *, percent):
        item_count = len(self._items)

        if item_count <= 1:
            return

        pct = percent
        if pct < 0:
            pct = 0
        elif pct > 1:
            pct = 1

        num_to_drop = math.floor(item_count*(1-pct))
        assert item_count >= 2
        if num_to_drop == item_count:
            num_to_drop -= 1

        logger.info(f'dropping {num_to_drop} of {item_count}')
        num_to_keep = item_count - num_to_drop

        random.shuffle(self._items)
        self._items = self._items[0:num_to_keep]
        logger.info(f'remaining {len(self._items)}')
