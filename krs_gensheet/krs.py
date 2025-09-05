#!/usr/bin/env python3

import logging

from krs_base import app_context, app_options
from krs_inputloader import extract_text
from krs_pageassemble import assemble
from krs_select import select

logger = None  # This is initialized in __main__


def main():
    global logger

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    )

    logger = logging.getLogger('krs_studying.' + __name__)

    options = app_options.AppOptions()
    args = options.get_args()

    the_app_context = app_context.AppContext(args=args)

    extractor = extract_text.ExtractText(context=the_app_context)
    inputset = extractor.parse()

    if args.report_mode:
        logger.info('Skipping page assembly due to report_mode argument.')
    else:
        selector = select.Selector(inputset=inputset)
        assemblor = assemble.Assemblor(
            context=the_app_context,
            worksheets=selector.get_worksheets(),
            answerkeys=selector.get_answerkeys())
        assemblor.run()

    logger.info('Done')


if __name__ == '__main__':
    main()
