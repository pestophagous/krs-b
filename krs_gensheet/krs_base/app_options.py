import logging
import os
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
        ifile_argname = 'inputfile'
        ifile_arg = parser.add_argument(
            ifile_argname,
            nargs='+',
            help='Either exactly one "metafile", or 1+ problemset files')

        cfg_filename = "krscfg.toml"
        if os.path.isfile(cfg_filename):
            logger.info(f'Reading options from {cfg_filename}')
            # When we have better documentation and automation of dependencies,
            # this import might move to elsewhere. For now, keeping it here allows
            # any user to avoid this dependency by simply not using krscfg.toml
            try:
                import tomllib
            except ModuleNotFoundError:
                import pip._vendor.tomli as tomllib

            with open(cfg_filename, "rb") as f:
                cfg_dict = tomllib.load(f)
                # Note: CLI opts listed in the command line when invoking the
                # program can still override and/or supplement these as a user
                # so chooses:
                parser.set_defaults(**cfg_dict)

                if ifile_argname in cfg_dict:
                    # If we don't remove the usual 'required' property from the
                    # positional argument, then 'parser.parse_args()' can fail
                    # below when in reality we _did_ receive an inputfile arg,
                    # but via the toml config.
                    ifile_arg.required = False

        self.args = parser.parse_args()

    def get_args(self):
        return self.args
