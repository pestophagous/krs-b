#!/usr/bin/env python3

import os
import sys

from krs_inputloader import extract_text
from krs_pageassemble import assemble
from krs_select import select


def main():
    # FUTURE: pass in more than one input file
    p = os.path.normpath(os.path.join(os.getcwd(), sys.argv[1]))
    print(p)  # TODO: logger
    extractor = extract_text.ExtractText([p])
    inputset = extractor.parse()
    selector = select.Selector(inputset=inputset)
    assemblor = assemble.Assemblor(
        worksheets=selector.get_worksheets(),
        answerkeys=selector.get_answerkeys())
    assemblor.run()

    print('Done.')  # TODO: logger


if __name__ == '__main__':
    main()
