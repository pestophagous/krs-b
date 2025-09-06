import copy
import logging
import math
import pprint
import random
from dataclasses import dataclass, field

# @dataclass(eq=True, frozen=True)
# @dataclass gives us __repr__ printability for free
# (eq=True, frozen=True) gives us hashability

logger = logging.getLogger('krs_studying.' + __name__)


def one_line_ify(s):
    s = s.replace('\r\n', ' ')
    s = s.replace('\r', ' ')
    s = s.replace('\n', ' ')
    return s


@dataclass
class Item:
    unique_id: str = field(init=True)
    answer: str = field(init=True)
    tags: list = field(init=True)
    prompt: str = field(init=True)

    def is_tagged_with_any_of(self, list_of_tags):
        intersection = set(self.tags).intersection(set(list_of_tags))
        return bool(intersection)

    def reported_prompt(self):
        return [self.unique_id, one_line_ify(self.prompt)]


class Set:
    def __init__(self, *, context):
        self._context = context
        self._items = []
        self._item_ids = {}
        self._include_tags = context.args.include_tags
        self._exclude_tags = context.args.exclude_tags
        self._set_of_all_tags = set()

    def get_all_items(self):
        return copy.deepcopy(self._items)

    def log_all_tags(self):
        as_a_list = sorted(list(self._set_of_all_tags))
        logger.info(f'All tags in set: {as_a_list}')
        if self._context.args.report_mode:
            for t in as_a_list:
                # intentional use of bare 'print' here:
                print(t)

            item_report = [i.reported_prompt() for i in self._items]
            pprint.pprint(item_report, width=1)

    def append(self, item):
        if item.unique_id in self._item_ids:
            raise ValueError(f"Duplicate id not allowed: {item.unique_id}")

        keep_it = True
        if self._include_tags:
            keep_it = item.is_tagged_with_any_of(self._include_tags)

        if keep_it and self._exclude_tags:
            keep_it = not item.is_tagged_with_any_of(self._exclude_tags)

        logger.debug(
            f'keep_it={keep_it} for {item.unique_id} with tags: {item.tags}')

        if keep_it:
            self._item_ids[item.unique_id] = 1
            self._items.append(item)
            self._set_of_all_tags.update(set(item.tags))

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

        if pct < 1 and self._context.args.report_mode:
            logger.error('We strongly advise AGAINST simultaneous use of metalist weights '
                         'and report_mode in the same run. Weight is ignored in this case.')
            pct = 1

        num_to_drop = math.floor(item_count*(1-pct))
        assert item_count >= 2
        if num_to_drop == item_count:
            num_to_drop -= 1

        logger.info(f'dropping {num_to_drop} of {item_count}')
        num_to_keep = item_count - num_to_drop

        if num_to_keep == len(self._items):
            pass  # nothing to do. keep all.
        else:
            # We need num_to_drop valid indices AT RANDOM.
            # Note: previously we would perform a `shuffle` and drop the droppable
            #   quantity off of the end, to achieve the drop-at-random goal.
            #   However, we now wish to PRESERVE original order while dropping at random.
            # `sample` grabs droppable indices without replacement, as we require:
            to_drop = random.sample(
                list(range(0, len(self._items))), num_to_drop)

            for i in to_drop:
                self._items[i] = None  # marked for deletion

            self._items = [i for i in self._items if i is not None]

        logger.info(f'remaining {len(self._items)}')
