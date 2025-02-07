from krs_pageassemble import page

# FUTURE: different possibilities for items-per-page.
_ITEMS_PER_WS_PAGE = 3
_ITEMS_PER_AK_PAGE = 24


class Assemblor:
    def __init__(self, *, worksheets, answerkeys):
        # FUTURE: different possibilities for items-per-page.
        self._worksheets = worksheets
        self._answerkeys = answerkeys

        for w in self._worksheets:
            assert page.page_is_sane(w)
            assert w.items_on_page == _ITEMS_PER_WS_PAGE

        for a in self._answerkeys:
            assert page.page_is_sane(a)
            assert a.items_on_page == _ITEMS_PER_AK_PAGE

    def run(self):
        i = 0
        for w in self._worksheets:
            i += 1
            self.print_one_worksheet(w, page=i)

        i = 0
        for a in self._answerkeys:
            i += 1
            self.print_one_answerkey(a, page=i)

    def print_one_worksheet(self, worksheet, *, page):
        # when printing sheet, must put date with uniq-id
        # TODO: logger

        # def get_worksheets(self):
        #     s = page.WorksheetPage(
        #         unique_ids=['a844695'],
        #         prompts=['$$ 4x^2 - 4 = 0 $$'])
        #     return [s]

        print('print_one_worksheet')

    def print_one_answerkey(self, worksheet, *, page):
        # FUTURE: need option of which uniq-id to start with
        # when printing sheet, must put date

        # def get_answerkeys(self):
        #     s = page.AnswerKeyPage(
        #         unique_ids=['a844695'],
        #         answers=['x=1, x=-1'])
        #     return [s]

        print('print_one_answerkey')
