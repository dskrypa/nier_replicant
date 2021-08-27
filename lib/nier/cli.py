"""
Utils for the CLI

:author: Doug Skrypa
"""

from argparse import ArgumentParser
from contextlib import suppress
from pathlib import Path


class ArgParser(ArgumentParser):
    def _get_subparser(self, dest: str):
        try:
            return next((sp for sp in self._subparsers._group_actions if sp.dest == dest), None)
        except AttributeError:  # If no subparsers exist yet
            return None

    def add_subparser(self, dest: str, name: str, help_desc: str = None, **kwargs) -> 'ArgParser':
        """
        Add a subparser for a subcommand to the subparser group with the given destination variable name.  Creates the
        group if it does not already exist.

        :param dest: The subparser group destination for this subparser
        :param name: The name of the subcommand/subparser to add
        :param help_desc: The text to be used as both the help and description for this subcommand
        :param kwargs: Keyword args to pass to the :func:`add_parser` function
        :return: The parser that was created
        """
        sp_group = self._get_subparser(dest) or self.add_subparsers(dest=dest, title='subcommands')
        sub_parser = sp_group.add_parser(
            name, help=kwargs.pop('help', help_desc), description=kwargs.pop('description', help_desc), **kwargs
        )
        return sub_parser  # noqa

    def parse_args(self, *args, **kwargs):
        args = super().parse_args(*args, **kwargs)
        with suppress(AttributeError):
            if missing := next((sp for sp in self._subparsers._group_actions if getattr(args, sp.dest) is None), None):
                self.error(f'missing required positional argument: {missing.dest} (use --help for more details)')
        return args


def get_path(path: str) -> Path:
    if path:
        path_obj = Path(path).expanduser()
        if not path_obj.exists() and '/' not in path and '\\' not in path:
            path_obj = get_steam_dir().joinpath(path)
    else:
        path_obj = get_steam_dir().joinpath('GAMEDATA')
    if not path_obj.exists():
        raise PathRequired(f'path={path_obj.as_posix()} does not exist')
    return path_obj


def get_steam_dir() -> Path:
    steam_dir = Path('~/Documents/My Games/NieR Replicant ver.1.22474487139/Steam/').expanduser()
    if not steam_dir.exists():
        raise PathRequired(f'steam_dir={steam_dir.as_posix()} does not exist')
    steam_dirs = list(steam_dir.iterdir())
    if len(steam_dirs) != 1:
        raise PathRequired(f'a single directory under steam_dir={steam_dir.as_posix()} does not exist')
    return steam_dirs[0]


class PathRequired(Exception):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return f'--path is required because {self.reason}'
