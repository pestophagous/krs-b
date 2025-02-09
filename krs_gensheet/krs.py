#!/usr/bin/env python3

import os
import sys

from krs_inputloader import extract_text
from krs_pageassemble import assemble
from krs_select import select


def main():
    inputfiles = []
    inputfiles.append(os.path.normpath(os.path.join(os.getcwd(), sys.argv[1])))
    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            inputfiles.append(os.path.normpath(
                os.path.join(os.getcwd(), sys.argv[i])))

    extractor = extract_text.ExtractText(inputfiles)
    inputset = extractor.parse()
    selector = select.Selector(inputset=inputset)
    assemblor = assemble.Assemblor(
        worksheets=selector.get_worksheets(),
        answerkeys=selector.get_answerkeys())
    assemblor.run()

    print('Done.')  # TODO: logger


if __name__ == '__main__':
    main()
