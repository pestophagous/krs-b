import logging
import random

from krs_pageassemble import assemble, page

logger = logging.getLogger('krs_studying.' + __name__)


class Selector:
    # FUTURE: Selector will filter by tag or other criteria.
    def __init__(self, *, inputset):
        # inputset has method: get_all_items
        self._inputset = inputset

    def get_worksheets(self):
        # FUTURE: Selector will filter by tag or other criteria.
        sheets = []

        # We shuffle for worksheets. We >sort< for answer key. do we need copies?
        random.shuffle(self._inputset._items)

        ids_on_one_page = []
        prompts_on_one_page = []
        for item in self._inputset._items:
            ids_on_one_page.append(item.unique_id)
            prompts_on_one_page.append(item.prompt)

            if len(ids_on_one_page) == assemble._ITEMS_PER_WS_PAGE:
                # make a WorksheetPage, add it to sheets list.
                # reset 2 parallel lists.
                p = page.WorksheetPage(
                    unique_ids=ids_on_one_page,
                    prompts=prompts_on_one_page)
                sheets.append(p)
                ids_on_one_page = []
                prompts_on_one_page = []

        if ids_on_one_page:
            # "stragglers" that weren't a multiple of _ITEMS_PER_WS_PAGE
            p = page.WorksheetPage(
                unique_ids=ids_on_one_page,
                prompts=prompts_on_one_page)
            sheets.append(p)

        return sheets

    def get_answerkeys(self):
        # Even when WorksheetPage(s) are generated with some filtering, it is
        # debatable if we ever need to filter the answers
        keypages = []

        # FUTURE: need option of which uniq-id to start with.
        # We shuffle for worksheets. We >sort< for answer key. do we need copies?
        sorted_items = sorted(self._inputset._items,
                              key=lambda x: x.unique_id)

        ids_on_one_page = []
        answers_on_one_page = []
        for item in sorted_items:
            ids_on_one_page.append(item.unique_id)
            answers_on_one_page.append(item.answer)

            if len(ids_on_one_page) == assemble._ITEMS_PER_AK_PAGE:
                # make a AnswerKeyPage, add it to keypages list.
                # reset 2 parallel lists.
                p = page.AnswerKeyPage(
                    unique_ids=ids_on_one_page,
                    answers=answers_on_one_page)
                keypages.append(p)
                ids_on_one_page = []
                answers_on_one_page = []

        if ids_on_one_page:
            # "stragglers" that weren't a multiple of _ITEMS_PER_AK_PAGE
            p = page.AnswerKeyPage(
                unique_ids=ids_on_one_page,
                answers=answers_on_one_page)
            keypages.append(p)

        return keypages
