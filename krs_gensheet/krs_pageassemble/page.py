import logging
from dataclasses import dataclass, field

logger = logging.getLogger('krs_studying.' + __name__)

# FUTURE: different possibilities for items-per-page.
_ITEMS_PER_WS_PAGE = 2
# FUTURE: cli (and toml config) option (for plots-as-answers):
_ITEMS_PER_AK_PAGE = 18  # need to lower when answers are large plots


@dataclass
class WorksheetPage:
    unique_ids: list = field(init=True)
    prompts: list = field(init=True)
    items_on_page: int = field(default=_ITEMS_PER_WS_PAGE)
    is_worksheet: bool = field(default=True)
    is_answerkey: bool = field(default=False)


@dataclass
class AnswerKeyPage:
    unique_ids: list = field(init=True)
    answers: list = field(init=True)
    items_on_page: int = field(default=_ITEMS_PER_AK_PAGE)
    is_worksheet: bool = field(default=False)
    is_answerkey: bool = field(default=True)


def page_is_sane(p):
    # TODO: impl
    return True
