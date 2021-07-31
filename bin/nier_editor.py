#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging
from argparse import ArgumentParser
from datetime import datetime

from nier.constants import FERTILIZER
from nier.save_file import GameData
from nier.utils import colored

log = logging.getLogger(__name__)


def parser():
    parser = ArgumentParser(description='Nier Replicant ver.1.22474487139... Save File Editor')

    actions = parser.add_subparsers(dest='action', title='subcommands')
    garden = actions.add_parser('garden', help='Examine or modify the garden', description='Examine or modify the garden')

    garden_actions = garden.add_subparsers(dest='sub_action', title='subcommands')
    garden_view = garden_actions.add_parser('view', help='View the current garden state', description='View the current garden state')
    garden_edit = garden_actions.add_parser('edit', help='Edit garden plots', description='Edit garden plots')
    gt_group = garden_edit.add_argument_group('Time Options').add_mutually_exclusive_group()
    gt_group.add_argument('--time', '-t', metavar='YYYY-MM-DD HH:MM:SS', type=datetime.fromisoformat, help='A specific time to set as the plant time')
    gt_group.add_argument('--hours', '-H', type=int, help='Set the plant time to be the given number of hours earlier than now')
    garden_edit.add_argument('--fertilizer', '-f', choices=FERTILIZER, help='The fertilizer to use')
    garden_edit.add_argument('--water', '-w', type=int, choices=(1, 2), help='Number of times to water')

    items = actions.add_parser('items', help='Examine or modify items', description='Examine or modify items')
    items_actions = items.add_subparsers(dest='sub_action', title='subcommands')
    items_view = items_actions.add_parser('view', help='View current items', description='View current items')
    items_edit = items_actions.add_parser('edit', help='Edit items', description='Edit items')
    items_edit.add_argument('item', help='Item name')
    items_edit.add_argument('quantity', type=int, help='Number of the given item to set')

    for _parser in (parser, garden, garden_view, garden_edit, items_view, items_edit):
        _parser.add_argument('--path', '-p', help='Save file path')
        _parser.add_argument('--slot', '-s', type=int, choices=(1, 2, 3), help='Save slot to load/modify')
        _parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase logging verbosity (can specify multiple times)')
    return parser


def main():
    args = parser().parse_args()
    log_fmt = '%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s' if args.verbose else '%(message)s'
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format=log_fmt)

    game_data = GameData.load(get_path(args.path))
    slots = game_data.slots if args.slot is None else [game_data.slots[args.slot - 1]]

    if args.action == 'garden':
        if args.sub_action == 'view':
            prefix = '    ' if len(slots) > 1 else ''
            for i, slot in enumerate(slots):
                if i:
                    print()
                if prefix:
                    print(colored(f'{slot}:', 14))
                slot.garden.show(prefix=prefix)
        elif args.sub_action == 'edit':
            if len(slots) > 1:
                raise ValueError('--slot is required for setting garden plant times')
            slot = slots[0]
            slot.garden.update(args.time, args.hours, args.fertilizer, args.water)
            log.info('Updated garden:')
            slot.garden.show()
            slot['save_time'] = datetime.now()
            game_data.save()
        else:
            raise ValueError(f'Unexpected sub_action={args.sub_action!r}')
    elif args.action == 'items':
        if len(slots) > 1:
            raise ValueError('--slot is required for setting garden plant times')
        slot = slots[0]
        sections = ('recovery', 'cultivation', 'fishing', 'raw_materials')
        if args.sub_action == 'view':
            slot.pprint(keys=set(sections))
        elif args.sub_action == 'edit':
            quantity = args.quantity
            if quantity < 0 or quantity > 99:
                raise ValueError(f'Invalid {quantity=} - must be between 0 and 99')
            for section in sections:
                if args.item in slot[section]:
                    if section == 'recovery' and quantity > 10:
                        raise ValueError(f'Invalid {quantity=} - must be between 0 and 10')
                    old = slot[section][args.item]
                    log.info(f'Setting quantity for item={args.item} {old} => {quantity} in {section=}')
                    slot._parsed[section][args.item] = quantity
                    break
            else:
                raise ValueError(f'Could not find item={args.item!r} in {sections=}')
            slot['save_time'] = datetime.now()
            game_data.save()
        else:
            raise ValueError(f'Unexpected sub_action={args.sub_action!r}')
    else:
        raise ValueError(f'Unexpected action={args.action!r}')


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
