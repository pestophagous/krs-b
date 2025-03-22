import datetime
import logging
import os
import shutil
import subprocess
from pathlib import Path

from krs_pageassemble import page

# FUTURE: different possibilities for items-per-page.
_ITEMS_PER_WS_PAGE = 3
_ITEMS_PER_AK_PAGE = 24
_SCRATCHPAD_DIR = "/tmp"

logger = logging.getLogger('krs_studying.' + __name__)


class Assemblor:
    def __init__(self, *, worksheets, answerkeys):
        # FUTURE: different possibilities for items-per-page.
        self._worksheets = worksheets
        self._answerkeys = answerkeys

        self._original_cwd = os.getcwd()

        for w in self._worksheets:
            assert page.page_is_sane(w)
            assert w.items_on_page == _ITEMS_PER_WS_PAGE

        for a in self._answerkeys:
            assert page.page_is_sane(a)
            assert a.items_on_page == _ITEMS_PER_AK_PAGE

        # FUTURE: consider CLI arg(s) for more image paths
        self.images_folder1 = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'inputs', 'images'))
        self.images_folder2 = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'private', 'inputs', 'images'))

    def run(self):
        os.chdir(_SCRATCHPAD_DIR)
        i = 0
        for w in self._worksheets:
            i += 1
            self.print_one_worksheet(w, page=i)

        i = 0
        for a in self._answerkeys:
            i += 1
            self.print_one_answerkey(a, page=i)

        os.chdir(self._original_cwd)

    def _with_image_paths_interpolated(self, contents):
        contents = contents.replace(
            'KRSREPLACEMEIMAGESFOLDERPATH', self.images_folder1)
        contents = contents.replace(
            'KRSREPLACEMESECONDIMAGESFOLDERPATH', self.images_folder2)
        return contents

    def print_one_worksheet(self, worksheet, *, page):
        logger.info('print_one_worksheet')
        template = os.path.normpath(os.path.join(
            os.path.dirname(__file__), 'simple_tex', 'subpage_of_worksheet.tex'))
        contents = Path(template).read_text()
        contents = self._with_image_paths_interpolated(contents)

        for i, prompt in enumerate(worksheet.prompts):
            # TODO: when printing sheet, must put date with uniq-id
            tex_content = contents.replace(
                'KRSREPLACEMEPROMPT', prompt)
            tex_content = tex_content.replace(
                'KRSREPLACEMEID', worksheet.unique_ids[i])

            single_prompt_inputfile = os.path.join(
                _SCRATCHPAD_DIR, f"tmp{i+1}.tex")
            with open(single_prompt_inputfile, "w") as text_file:
                text_file.write(tex_content)

            subprocess.run(
                ["pdflatex", "-output-directory", _SCRATCHPAD_DIR, single_prompt_inputfile])

        # We enter the next loop if the page needs "leftover placeholders".
        # This happens if worksheet.prompts contained FEWER than _ITEMS_PER_WS_PAGE.
        while i < (_ITEMS_PER_WS_PAGE-1):
            i += 1
            # Nice-to-have: why did empty string fail where single period works?
            tex_content = contents.replace(
                'KRSREPLACEMEID', '')
            tex_content = tex_content.replace(
                'KRSREPLACEMEPROMPT', '')

            single_prompt_inputfile = os.path.join(
                _SCRATCHPAD_DIR, f"tmp{i+1}.tex")
            with open(single_prompt_inputfile, "w") as text_file:
                text_file.write(tex_content)

            subprocess.run(
                ["pdflatex", "-output-directory", _SCRATCHPAD_DIR, single_prompt_inputfile])

        template = os.path.normpath(os.path.join(
            os.path.dirname(__file__), 'simple_tex', 'one_whole_worksheet_page.tex'))

        ws_basename = f"worksheet{worksheet.unique_ids[0]}"
        ws_path_in_scratchdir = os.path.join(
            _SCRATCHPAD_DIR, f"{ws_basename}.pdf")
        subprocess.run(
            ["pdflatex", f"-jobname={ws_basename}", template])
        shutil.copy2(
            ws_path_in_scratchdir,
            os.path.join(self._original_cwd, f"{ws_basename}.pdf"))

    def print_one_answerkey(self, answerkey, *, page):
        logger.info('print_one_answerkey')

        template = os.path.normpath(os.path.join(
            os.path.dirname(__file__), 'simple_tex', 'page_of_answerkey.tex'))
        contents = Path(template).read_text()
        contents = self._with_image_paths_interpolated(contents)

        keyed_answers = ''
        for i, answer in enumerate(answerkey.answers):
            keyed_answers += '\\texttt{' + answerkey.unique_ids[i]
            keyed_answers += '.    }'
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
        shutil.copy2(
            os.path.join(_SCRATCHPAD_DIR, f"{outname}.pdf"),
            os.path.join(self._original_cwd, f"{outname}.pdf"))
