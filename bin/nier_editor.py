#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging
from datetime import datetime

from nier.constants import FERTILIZER, FERTILIZER_ALIASES
from nier.save_file import GameData
from nier.utils import ArgParser, colored

ITEM_SECTIONS = ('recovery', 'cultivation', 'fishing', 'raw_materials')
log = logging.getLogger(__name__)


def parser():
    parser = ArgParser(description='Nier Replicant ver.1.22474487139... Save File Editor')
    # region View/Edit Options
    view_parser = parser.add_subparser('action', 'view', 'View information from a save file')
    edit_parser = parser.add_subparser('action', 'edit', 'Edit information in a save file')

    _parsers = [parser, view_parser, edit_parser]

    def _view_and_edit(name: str, desc: str = None):
        desc = desc or name
        _view = view_parser.add_subparser('item', name, f'View {desc}')
        _edit = edit_parser.add_subparser('item', name, f'Edit {desc}')
        _parsers.append(_view)
        _parsers.append(_edit)
        return _view, _edit

    view_garden, edit_garden = _view_and_edit('garden', 'garden plots')
    gt_group = edit_garden.add_argument_group('Time Options').add_mutually_exclusive_group()
    gt_group.add_argument('--time', '-t', metavar='YYYY-MM-DD HH:MM:SS', type=datetime.fromisoformat, help='A specific time to set as the plant time')
    gt_group.add_argument('--hours', '-H', type=int, help='Set the plant time to be the given number of hours earlier than now')
    edit_garden.add_argument('--fertilizer', '-f', choices=FERTILIZER_ALIASES.keys(), help='The fertilizer to use')
    fert_group = edit_garden.add_argument_group('Fertilizer Options')
    fert_group.add_argument('--only_planted', '-P', action='store_true', help='Only set the specified fertilizer for plots with a seed planted (default: all)')
    fert_group.add_argument('--only_unfertilized', '-F', action='store_true', help='Only set the specified fertilizer for plots with no fertilizer already in place (default: all)')
    edit_garden.add_argument('--water', '-w', type=int, choices=(1, 2), help='Number of times to water')

    view_items, edit_items = _view_and_edit('items')
    edit_items.add_argument('name', help='Item name')
    edit_items.add_argument('quantity', type=int, help='Number of the given item to set')

    view_attr = view_parser.add_subparser('item', 'attrs', 'View SaveFile attributes')
    _parsers.append(view_attr)
    view_attr.add_argument('attr', nargs='*', help='The attribute(s) to view')
    view_attr.add_argument('--binary', '-b', action='store_true', help='Show the binary version, even if a higher level representation is available')
    view_attr.add_argument('--unknowns', '-u', action='store_true', help='Include unknown fields in output')
    view_attr.add_argument('--no_sort', '-S', dest='sort_keys', action='store_false', help='Do not sort keys in output')
    view_bin_group = view_attr.add_argument_group('Binary Data Options', 'Options that apply when viewing binary data')
    view_bin_group.add_argument('--per_line', '-L', type=int, default=40, help='Number of bytes to print per line')
    view_bin_group.add_argument('--hide_empty', '-e', type=int, default=10, help='Line threshold above which repeated lines of zeros will be hidden')

    for _parser in _parsers:
        _parser.add_argument('--path', '-p', help='Save file path')
        _parser.add_argument('--slot', '-s', type=int, choices=(1, 2, 3), help='Save slot to load/modify')
        _parser.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')

    # endregion
    # region Diff Options
    diff_parser = parser.add_subparser('action', 'diff', 'View the difference between 2 save files/slots')
    diff_files = diff_parser.add_subparser('item', 'files', 'View the difference between 2 save files')
    diff_files.add_argument('paths', nargs=2, help='The save files to process')
    diff_files.add_argument('--slot1', '-s1', type=int, choices=(1, 2, 3), help='Save slot in file 1. If specified, must also specify --slot2/-s2 (default: full file diff)')
    diff_files.add_argument('--slot2', '-s2', type=int, choices=(1, 2, 3), help='Save slot in file 2. If specified, must also specify --slot1/-s1 (default: full file diff)')
    diff_files.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')

    diff_slots = diff_parser.add_subparser('item', 'saves', 'View the difference between 2 save slots')
    diff_slots.add_argument('slots', nargs=2, type=int, choices=(1, 2, 3), help='The save slots/entries to compare')
    diff_slots.add_argument('--path', '-p', help='Save file path')
    diff_slots.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')

    for _parser in (diff_files, diff_slots):
        _group = _parser.add_argument_group('Diff Options')
        _group.add_argument('--per_line', '-L', type=int, default=40, help='Number of bytes to print per line (binary data only)')
        _group.add_argument('--binary', '-b', action='store_true', help='Show the binary version, even if a higher level representation is available')
        _fields = _group.add_argument_group('Field Options').add_mutually_exclusive_group()
        _fields.add_argument('--keys', '-k', nargs='+', help='Specific keys/attributes to include in the diff (default: all)')
        _fields.add_argument('--unknowns', '-u', action='store_true', help='Only show unknown fields in output')
    # endregion
    return parser


def main():
    args = parser().parse_args()
    log_fmt = '%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s' if args.verbose else '%(message)s'
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format=log_fmt)

    if (action := args.action) in ('view', 'edit'):
        game_data = GameData.load(get_path(args.path))
        if action == 'view':
            view(game_data, args.item, args.slot, args)
        elif action == 'edit':
            edit(game_data, args.item, args.slot, args)
    elif action == 'diff':
        diff(args.item, args)
    else:
        raise ValueError(f'Unexpected action={args.action!r}')


def view(game_data: GameData, item: str, slot_num: int, args):
    slots = game_data.slots if slot_num is None else [game_data.slots[slot_num - 1]]
    if item == 'garden':
        prefix = '    ' if len(slots) > 1 else ''
        for i, slot in enumerate(slots):
            if i:
                print()
            if prefix:
                print(colored(f'{slot}:', 14))
            slot.garden.show(prefix=prefix)
    elif item == 'items':
        if len(slots) > 1:
            raise ValueError('--slot is required for viewing items')
        slots[0].pprint(keys=set(ITEM_SECTIONS))
    elif item == 'attrs':
        if len(slots) > 1:
            raise ValueError('--slot is required for viewing attributes')
        slots[0].pprint(
            args.unknowns,
            args.attr,
            binary=args.binary,
            per_line=args.per_line,
            hide_empty=args.hide_empty,
            sort_keys=args.sort_keys,
            struct=repr,
        )
    else:
        raise ValueError(f'Unexpected {item=} to view')


def edit(game_data: GameData, item: str, slot_num: int, args):
    if slot_num is None:
        raise ValueError('--slot is required for editing')
    slot = game_data.slots[slot_num - 1]
    if item == 'garden':
        kwargs = {'only_unfertilized': args.only_unfertilized, 'only_planted': args.only_planted}
        fertilizer = FERTILIZER_ALIASES.get(args.fertilizer)
        slot.garden.update(args.time, args.hours, fertilizer, args.water, **kwargs)
        log.info('Updated garden:')
        slot.garden.show()
    elif item == 'items':
        item_name, quantity = args.name, args.quantity
        if not 0 <= quantity <= 99:
            raise ValueError(f'Invalid {quantity=} - must be between 0 and 99')

        for section in ITEM_SECTIONS:
            if item_name in slot[section]:
                if section == 'recovery' and quantity > 10:
                    raise ValueError(f'Invalid {quantity=} - must be between 0 and 10')
                old = slot[section][item_name]
                log.info(f'Setting quantity for item={item_name} {old} => {quantity} in {section=}')
                slot._parsed[section][item_name] = quantity
                break
        else:
            raise ValueError(f'Could not find item={item_name!r} in {ITEM_SECTIONS=}')
    else:
        raise ValueError(f'Unexpected {item=} to edit')

    slot['save_time'] = datetime.now()
    game_data.save()


def diff(item: str, args):
    if item == 'files':
        obj_a, obj_b = GameData.load(get_path(args.paths[0])), GameData.load(get_path(args.paths[1]))
        if args.slot1 or args.slot2:
            if not (args.slot1 and args.slot2):
                raise ValueError('Either both --slot1/-s1 and --slot2/-s2 must be provided, or neither may be provided')
            obj_a, obj_b = obj_a[args.slot1 - 1], obj_b[args.slot2 - 1]
    elif item == 'saves':
        game_data = GameData.load(get_path(args.path))
        obj_a, obj_b = game_data[args.slots[0] - 1], game_data[args.slots[1] - 1]
    else:
        raise ValueError(f'Unexpected {item=} to compare')

    if args.unknowns:
        keys = {k for k in obj_a._offsets_and_sizes if k.startswith('_unk')}
    else:
        keys = set(args.keys) if args.keys else None

    obj_a.diff(obj_b, per_line=args.per_line, byte_diff=args.binary, keys=keys)


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
