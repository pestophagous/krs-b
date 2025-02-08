import copy
from dataclasses import dataclass, field

# @dataclass(eq=True, frozen=True)
# @dataclass gives us __repr__ printability for free
# (eq=True, frozen=True) gives us hashability


@dataclass
class Item:
    unique_id: str = field(init=True)
    answer: str = field(init=True)
    tags: list = field(init=True)
    prompt: str = field(init=True)


class Set:
    def __init__(self):
        self._ordered_items = []

    def get_all_items(self):
        return copy.deepcopy(self._ordered_items)

    def append(self, item):
        self._ordered_items.append(item)
