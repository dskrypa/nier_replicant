#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging
from argparse import ArgumentParser
from datetime import datetime

from nier.save_file import GameData
from nier.utils import colored

log = logging.getLogger(__name__)


def parser():
    parser = ArgumentParser(description='Nier Replicant ver.1.22474487139... Save File Editor')

    actions = parser.add_subparsers(dest='action', title='subcommands')
    garden = actions.add_parser('garden', help='Examine or modify the garden', description='Examine or modify the garden')

    garden_actions = garden.add_subparsers(dest='sub_action', title='subcommands')
    garden_view = garden_actions.add_parser('view', help='View the current garden state', description='View the current garden state')
    garden_time = garden_actions.add_parser('time', help='Change the plant time for all plots', description='Change the plant time for all plots')
    gt_group = garden_time.add_mutually_exclusive_group()
    gt_group.add_argument('--time', '-t', metavar='YYYY-MM-DD HH:MM:SS', type=datetime.fromisoformat, help='A specific time to set as the plant time')
    gt_group.add_argument('--hours', '-H', type=int, help='Set the plant time to be the given number of hours earlier than now')

    for _parser in (parser, garden, garden_view, garden_time):
        _parser.add_argument('--path', '-p', help='Save file path')
        _parser.add_argument('--slot', '-s', type=int, choices=(1, 2, 3), help='Save slot to load/modify')
        _parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase logging verbosity (can specify multiple times)')
    return parser


def main():
    args = parser().parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    path = get_path(args.path)
    log.debug(f'Loading data from path={path.as_posix()}')
    game_data = GameData.load(path)
    slots = game_data.slots if args.slot is None else [game_data.slots[args.slot]]
    action, sub_action = args.action, args.sub_action
    if action == 'garden':
        if sub_action == 'view':
            prefix = '    ' if len(slots) > 1 else ''
            for i, slot in enumerate(slots):
                if i:
                    print()
                if prefix:
                    print(colored(f'{slot}:', 14))
                slot.show_garden(prefix=prefix)
        elif sub_action == 'time':
            if len(slots) > 1:
                raise ValueError('--slot is required for setting garden plant times')
            slots[0].set_plant_times(args.time, args.hours)
            log.info('Updated plant times:')
            slots[0].show_garden()
            game_data.save(path)
        else:
            raise ValueError(f'Unexpected {sub_action=}')
    else:
        raise ValueError(f'Unexpected {action=}')


def get_path(path):
    if path:
        path = Path(path).expanduser()
    else:
        steam_dir = Path('~/Documents/My Games/NieR Replicant ver.1.22474487139/Steam/').expanduser()
        if not steam_dir.exists():
            raise PathRequired(f'steam_dir={steam_dir.as_posix()} does not exist')
        steam_dirs = list(steam_dir.iterdir())
        if len(steam_dirs) != 1:
            raise PathRequired(f'a single directory under steam_dir={steam_dir.as_posix()} does not exist')
        path = steam_dirs[0].joinpath('GAMEDATA')
    if not path.exists():
        raise PathRequired(f'path={path.as_posix()} does not exist')
    return path


class PathRequired(Exception):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return f'--path is required because {self.reason}'


if __name__ == '__main__':
    main()
