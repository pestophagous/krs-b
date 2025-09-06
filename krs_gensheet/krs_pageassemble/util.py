import logging
import subprocess
import sys

logger = logging.getLogger('krs_studying.' + __name__)


def run_pdflatex_subprocess(*, cmd_tokens_list):
    pre_tokens = ['pdflatex', '-halt-on-error', '-file-line-error']
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
