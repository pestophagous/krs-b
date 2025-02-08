import os

from krs_base import set

_VALID_LINE1_FORMAT_VERSION_MARK = 'krs_v1'
_HALF_OF_DELIM = '-----'
_INNER_DELIM = '---'


class ExtractText:
    def __init__(self, files):
        for f in files:
            assert os.path.isfile(f)

        self._files = files

    def _next_non_comment(self, *, line_iter):
        while True:
            try:
                l = next(line_iter)
                if not l.startswith('#'):
                    return l.rstrip("\r\n")
            except StopIteration:
                return None

        return None

    def _parse_prompt(self, *, line_iter):
        prompt = None
        expect_other_delim_half = False

        while True:
            try:
                line = next(line_iter)
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

        # TODO: print some error or warning, ideally with line num! (except EOF)
        return None

    def _parse_file(self, *, filepath, ongoing_set):
        with open(filepath) as file:
            first_line = next(file).rstrip()
            if first_line != _VALID_LINE1_FORMAT_VERSION_MARK:
                # TODO: logger
                print('Invalid file')
                return

            expect_other_delim_half = False

            for l in file:
                line = l.rstrip("\r\n")
                if not line:
                    continue  # skip blank line when not "in" an item
                if line and line[0] == '#':
                    continue  # skip comment lines

                if line.startswith(_HALF_OF_DELIM) and expect_other_delim_half:
                    while True:
                        item = self._parse_item(line_iter=file)
                        if item:
                            ongoing_set.append(item)
                        else:
                            return
                elif line.startswith(_HALF_OF_DELIM):
                    expect_other_delim_half = True
                else:
                    expect_other_delim_half = False

    def parse(self):
        s = set.Set()

        for f in self._files:
            self._parse_file(filepath=f, ongoing_set=s)

        # TODO: logger
        print(len(s._ordered_items))
        print(s._ordered_items)
        return s
