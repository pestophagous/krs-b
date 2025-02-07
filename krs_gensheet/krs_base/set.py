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

        # Dummy for now. TODO: real impl
        self._ordered_items.append(
            Item(
                unique_id='a844695',
                answer='x=1, x=-1',
                tags=['gcf', 'factoring', 'solve-for-x'],
                prompt='$$ 4x^2 - 4 = 0 $$'
            ))

    def get_all_items(self):
        return copy.deepcopy(self._ordered_items)
