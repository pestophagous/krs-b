import logging
import subprocess
import sys

logger = logging.getLogger('krs_studying.' + __name__)


def run_pdflatex_subprocess(*, cmd_tokens_list):
    # Note: halt-on-error and nonstopmode 'sound like' a contradiction but they
    # are not. nonstopmode tells pdflatex that ZERO INTERACTION is possible, so
    # that it won't sit and ask you to find a missing file before continuing.
    # A missing file does not simply 'halt-on-error' but triggers interaction,
    # whereas a syntax error triggers a halt-on-error. So these make sense together.
    pre_tokens = ['pdflatex', '-halt-on-error',
                  '-file-line-error', '-interaction=nonstopmode']
    total_tokens = pre_tokens + cmd_tokens_list
    result = subprocess.run(total_tokens,
                            capture_output=True,  # Python >= 3.7 only?
                            text=True,  # Python >= 3.7 only?
                            )
    if result.returncode != 0:
        logger.error(f'Dumping error from command: {total_tokens}')
        print(result.stderr)
        print(result.stdout)
        logger.error(
            f'Finished dumping error (above) from command: {total_tokens}')
        sys.exit(result.returncode)
