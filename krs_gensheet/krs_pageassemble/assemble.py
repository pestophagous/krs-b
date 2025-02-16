import datetime
import logging
import os
import subprocess
from pathlib import Path

from krs_pageassemble import page

# FUTURE: different possibilities for items-per-page.
_ITEMS_PER_WS_PAGE = 3
_ITEMS_PER_AK_PAGE = 24

logger = logging.getLogger('krs_studying.' + __name__)


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
        logger.info('print_one_worksheet')
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

    def print_one_answerkey(self, answerkey, *, page):
        logger.info('print_one_answerkey')

        template = os.path.normpath(os.path.join(
            os.path.dirname(__file__), 'simple_tex', 'page_of_answerkey.tex'))
        contents = Path(template).read_text()

        keyed_answers = ''
        for i, answer in enumerate(answerkey.answers):
            keyed_answers += answerkey.unique_ids[i]
            keyed_answers += '. '
            keyed_answers += answer
            keyed_answers += '\n\n'

        tex_content = contents.replace(
            'KRSREPLACEMEANSWERS', keyed_answers)

        with open("tmpanswerkey.tex", "w") as text_file:
            text_file.write(tex_content)

        timesuffix = datetime.datetime.now().isoformat().replace(':', '_')
        outname = f'answers_{timesuffix}'
        subprocess.run(
            ["pdflatex", f"-jobname={outname}", "tmpanswerkey.tex"])
