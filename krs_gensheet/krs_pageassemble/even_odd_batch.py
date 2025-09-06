import logging
import os
import shutil

from krs_pageassemble import util

logger = logging.getLogger('krs_studying.' + __name__)

_FIRST = """\documentclass{article}
\\usepackage{pdfpages}
\\usepackage[papersize={8.5in,11in},
  lmargin=0in,
  rmargin=0in,
  tmargin=0in,
  bmargin=0in]{geometry}

\pagenumbering{gobble}

\\begin{document}
      \setlength\\voffset{+0.0in}
      \setlength\hoffset{+0.0in}
      \includepdfmerge[nup=1x1,
                       noautoscale=true,
                       frame=false,
                       templatesize={8.5in}{11in}]"""

_NEXT = """
\\newpage
      \includepdfmerge[nup=1x1,
                       noautoscale=true,
                       frame=false,
                       templatesize={8.5in}{11in}]"""


class EvenOddBatch:
    def __init__(self, *, original_cwd, scratch_dir, content_name):
        self._tex_for_all_odd_pages = ''
        self._tex_for_all_even_pages = ''
        self._next_is_odd = True

        self._content_name = content_name
        self._original_cwd = original_cwd
        self._scratch_dir = scratch_dir

    def _add(self, *, page_set, path_to_page_pdf):
        if not page_set:
            page_set += _FIRST
        else:
            page_set += _NEXT

        page_set += "{"
        page_set += path_to_page_pdf
        page_set += "}\n"
        return page_set

    def add_page(self, *, path_to_page_pdf):
        if self._next_is_odd:
            self._tex_for_all_odd_pages = self._add(
                page_set=self._tex_for_all_odd_pages,
                path_to_page_pdf=path_to_page_pdf)
        else:
            self._tex_for_all_even_pages = self._add(
                page_set=self._tex_for_all_even_pages,
                path_to_page_pdf=path_to_page_pdf)

        self._next_is_odd = not self._next_is_odd

    def print(self):
        os.chdir(self._scratch_dir)
        self._close_and_print_half(
            tex_string_in_progress=self._tex_for_all_odd_pages,
            new_pdf_basename=f'{self._content_name}_odd')
        self._close_and_print_half(
            tex_string_in_progress=self._tex_for_all_even_pages,
            new_pdf_basename=f'{self._content_name}_even')

    def _close_and_print_half(self, *, tex_string_in_progress, new_pdf_basename):
        if not tex_string_in_progress:
            logger.info(f"Nothing to print for: {new_pdf_basename}")
            return

        tex_string_in_progress += "\n\end{document}\n"

        inputfile = os.path.join(
            self._scratch_dir, f"{new_pdf_basename}.tex")
        with open(inputfile, "w") as text_file:
            text_file.write(tex_string_in_progress)

        util.run_pdflatex_subprocess(
            cmd_tokens_list=["-output-directory", self._scratch_dir, inputfile])

        shutil.copy2(
            os.path.join(self._scratch_dir, f"{new_pdf_basename}.pdf"),
            os.path.join(self._original_cwd, f"{new_pdf_basename}.pdf"))

    def print_one_worksheet(self, worksheet, *, page):
        util.run_pdflatex_subprocess(
            cmd_tokens_list=["-output-directory", self._scratch_dir, single_prompt_inputfile])
