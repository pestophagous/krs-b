from krs_pageassemble import page


class Selector:
    # FUTURE: Selector will filter by tag or other criteria.
    def __init__(self, *, inputset):
        # inputset has method: get_all_items
        self._inputset = inputset

    def get_worksheets(self):
        s = page.WorksheetPage(
            unique_ids=['a844695'],
            prompts=['$$ 4x^2 - 4 = 0 $$'])
        return [s]

    def get_answerkeys(self):
        s = page.AnswerKeyPage(
            unique_ids=['a844695'],
            answers=['x=1, x=-1'])
        return [s]
