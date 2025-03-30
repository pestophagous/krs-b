import logging

logger = logging.getLogger('krs_studying.' + __name__)


class AppContext:
    def __init__(self, *, args):
        self.args = args
