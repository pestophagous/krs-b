#!/usr/bin/env python3

import argparse
import logging

from krs_base import app_context
from krs_inputloader import extract_text
from krs_pageassemble import assemble
from krs_select import select

logger = None  # This is initialized in __main__


parser = argparse.ArgumentParser(
    prog='krs',
    description='Generator of pdf worksheets, supporting LaTeX math expressions.')

parser.add_argument(
    '-t',
    '--include-tags',
    action='extend',
    metavar='some_tag',
    nargs='+',
    help='Tags of desired problems. Problems with these tags are kept. All else is dropped.')
parser.add_argument(
    '-v',
    '--exclude-tags',
    action='extend',
    metavar='some_tag',
    nargs='+',
    help='Problems with these tags will be filtered out. It happens after --include-tags are applied.')
parser.add_argument(
    '-r',
    '--report-mode',
    action='store_true',
    help='Skip pdf generation. Output a "report" of tags and problems to STDOUT')
parser.add_argument(
    'inputfile',
    nargs='+',
    help='Either exactly one "metafile", or 1+ problemset files')


def main():
    global logger

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    )

    logger = logging.getLogger('krs_studying.' + __name__)

    args = parser.parse_args()

    the_app_context = app_context.AppContext(args=args)

    extractor = extract_text.ExtractText(context=the_app_context)
    inputset = extractor.parse()

    if args.report_mode:
        logger.info('Skipping page assembly due to report_mode argument.')
    else:
        selector = select.Selector(inputset=inputset)
        assemblor = assemble.Assemblor(
            worksheets=selector.get_worksheets(),
            answerkeys=selector.get_answerkeys())
        assemblor.run()

    logger.info('Done')


if __name__ == '__main__':
    main()
