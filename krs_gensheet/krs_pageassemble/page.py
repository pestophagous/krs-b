import logging
from dataclasses import dataclass, field

logger = logging.getLogger('krs_studying.' + __name__)


@dataclass
class WorksheetPage:
    unique_ids: list = field(init=True)
    prompts: list = field(init=True)
    items_on_page: int = field(default=3)
    is_worksheet: bool = field(default=True)
    is_answerkey: bool = field(default=False)


@dataclass
class AnswerKeyPage:
    unique_ids: list = field(init=True)
    answers: list = field(init=True)
    items_on_page: int = field(default=24)
    is_worksheet: bool = field(default=False)
    is_answerkey: bool = field(default=True)


def page_is_sane(p):
    # TODO: impl
    return True
