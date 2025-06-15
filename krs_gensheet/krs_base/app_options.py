import logging
import argparse

logger = logging.getLogger('krs_studying.' + __name__)


class AppOptions:
    def __init__(self):
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

        self.args = parser.parse_args()

    def get_args(self):
        return self.args
