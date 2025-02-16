import logging
import os

from krs_base import set

_VALID_LINE1_FORMAT_VERSION_MARK = 'krs_v1'
_HALF_OF_DELIM = '-----'
_INNER_DELIM = '---'

logger = logging.getLogger('krs_studying.' + __name__)


class _WrappedIter:
    def __init__(self, line_iter):
        self._line_num = 0
        self._iter = line_iter

    def get_next(self, *, dont_strip=False):
        l = next(self._iter)  # can raise StopIteration
        self._line_num += 1
        if not dont_strip:
            l = l.rstrip("\r\n")
        return (self._line_num, l)


class ExtractText:
    def __init__(self, files):
        for f in files:
            assert os.path.isfile(f)

        self._files = files

    def _next_non_comment(self, *, line_iter):
        while True:
            try:
                linenum, l = line_iter.get_next()
                if not l.startswith('#'):
                    return l
            except StopIteration:
                return None

        return None

    def _parse_prompt(self, *, line_iter):
        prompt = None
        expect_other_delim_half = False

        while True:
            try:
                linenum, line = line_iter.get_next(dont_strip=True)
            except StopIteration:
                return prompt

            if line.startswith(_HALF_OF_DELIM) and expect_other_delim_half:
                return prompt
            elif line.startswith(_HALF_OF_DELIM):
                expect_other_delim_half = True
            else:
                if prompt is None:
                    prompt = ''
                prompt += line

        return None

    def _parse_item(self, *, line_iter):
        the_id = self._next_non_comment(line_iter=line_iter)
        if the_id:
            the_answer = self._next_non_comment(line_iter=line_iter)
            if the_answer:
                the_tags = self._next_non_comment(line_iter=line_iter)
                if the_tags is not None:
                    the_inner_delim = self._next_non_comment(
                        line_iter=line_iter)
                    if the_inner_delim == _INNER_DELIM:
                        tags = []
                        if the_tags:
                            tags = the_tags.split(",")
                        the_prompt = self._parse_prompt(line_iter=line_iter)
                        if the_prompt:
                            item = set.Item(
                                unique_id=the_id,
                                answer=the_answer,
                                tags=tags,
                                prompt=the_prompt)
                            return item

        # TODO: log some error or warning, ideally with line num! (except EOF)
        return None

    def _parse_file(self, *, filepath):
        s = set.Set()

        with open(filepath) as file:
            line_iter = _WrappedIter(file)

            try:
                linenum, first_line = line_iter.get_next()
            except StopIteration:
                logger.error(f'Empty file: {filepath}')
                return s

            if first_line != _VALID_LINE1_FORMAT_VERSION_MARK:
                logger.error(
                    f'File lacks valid version_marker on first line: {filepath}')
                return s

            expect_other_delim_half = False

            while True:
                try:
                    linenum, line = line_iter.get_next()
                except StopIteration:
                    logger.error(
                        f'Failed to find any items in file: {filepath}')
                    return s

                if not line:
                    continue  # skip blank line when not "in" an item
                if line and line[0] == '#':
                    continue  # skip comment lines

                if line.startswith(_HALF_OF_DELIM) and expect_other_delim_half:
                    while True:
                        item = self._parse_item(line_iter=line_iter)
                        if item:
                            s.append(item)
                        else:
                            return s
                elif line.startswith(_HALF_OF_DELIM):
                    expect_other_delim_half = True
                else:
                    expect_other_delim_half = False

    def parse(self):
        s = set.Set()

        for f in self._files:
            set_from_file = self._parse_file(filepath=f)
            set_from_file.drop_all_but(percent=1.0)
            s.union(set_from_file, fail_on_duplicate=True)

        logger.info(f'Total items: {len(s._items)}')
        return s
