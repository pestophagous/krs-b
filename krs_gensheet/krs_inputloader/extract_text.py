import os

from krs_base import set


class ExtractText:
    def __init__(self, files):
        for f in files:
            assert os.path.isfile(f)
        # we're gonna at least make sure the files exist

    def parse(self):
        # TODO-NEXT: parse the file!
        s = set.Set()
        return s
