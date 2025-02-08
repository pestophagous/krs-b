import os
import subprocess
from pathlib import Path

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
        # TODO: logger
        print('print_one_worksheet')
        template = os.path.normpath(os.path.join(
            os.path.dirname(__file__), 'simple_tex', 'subpage_of_worksheet.tex'))
        contents = Path(template).read_text()

        for i, prompt in enumerate(worksheet.prompts):
            # TODO: when printing sheet, must put date with uniq-id
            tex_content = contents.replace(
                'KRSREPLACEMEPROMPT', prompt)
            tex_content = tex_content.replace(
                'KRSREPLACEMEID', worksheet.unique_ids[i])

            with open(f"tmp{i+1}.tex", "w") as text_file:
                text_file.write(tex_content)

            subprocess.run(
                ["pdflatex", "-output-directory", "/tmp", f"tmp{i+1}.tex"])

        while i < (_ITEMS_PER_WS_PAGE-1):
            i += 1
            # Nice-to-have: why did empty string fail where single period works?
            tex_content = contents.replace(
                'KRSREPLACEMEID', '')
            tex_content = tex_content.replace(
                'KRSREPLACEMEPROMPT', '')

            with open(f"tmp{i+1}.tex", "w") as text_file:
                text_file.write(tex_content)

            subprocess.run(
                ["pdflatex", "-output-directory", "/tmp", f"tmp{i+1}.tex"])

        template = os.path.normpath(os.path.join(
            os.path.dirname(__file__), 'simple_tex', 'one_whole_worksheet_page.tex'))

        subprocess.run(
            ["pdflatex", f"-jobname=worksheet{worksheet.unique_ids[0]}", template])

    def print_one_answerkey(self, worksheet, *, page):
        # FUTURE: need option of which uniq-id to start with
        # when printing sheet, must put date

        # def get_answerkeys(self):
        #     s = page.AnswerKeyPage(
        #         unique_ids=['a844695'],
        #         answers=['x=1, x=-1'])
        #     return [s]

        # TODO: logger
        print('print_one_answerkey')
