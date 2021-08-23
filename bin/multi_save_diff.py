#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging

from nier.cli import ArgParser, get_steam_dir
from nier.save_file import GameData
from nier.utils import colored

log = logging.getLogger(__name__)


def parser():
    parser = ArgParser(description='Nier Replicant ver.1.22474487139... Save File Diff Tool')
    parser.add_argument('--dir', '-d', metavar='PATH', help='Directory containing GAMEDATA files saved by save_watcher')

    group = parser.add_argument_group('Diff Options')
    group.add_argument('--per_line', '-L', type=int, default=8, help='Number of bytes to print per line (binary data only)')
    group.add_argument('--binary', '-b', action='store_true', help='Show the binary version, even if a higher level representation is available')
    fields = parser.add_argument_group('Field Options').add_mutually_exclusive_group()
    fields.add_argument('--keys', '-k', nargs='+', help='Specific keys/attributes to include in the diff (default: all)')
    fields.add_argument('--unknowns', '-u', action='store_true', help='Only show unknown fields in output')

    parser.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')
    return parser


def main():
    args = parser().parse_args()
    log_fmt = '%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s' if args.verbose else '%(message)s'
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format=log_fmt)

    save_dir = Path(args.dir).expanduser().resolve() if args.dir else get_steam_dir()
    pat = 'GAMEDATA_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9]'

    save_data = {}
    for pat in (pat, pat + '[0-9]'):
        for path in save_dir.glob(pat):
            gd = GameData.load(path)
            save_data[path] = (gd.header, max(gd.slots))

    # TODO: Show tabular diff of a selected field across files
    for path, (header, slot) in save_data.items():
        print(f'{path.name}: {header}, {slot}')


# def diff(item: str, args):
#     if item == 'files':
#         obj_a, obj_b = GameData.load(get_path(args.paths[0])), GameData.load(get_path(args.paths[1]))
#         if args.slot1 or args.slot2:
#             if not (args.slot1 and args.slot2):
#                 raise ValueError('Either both --slot1/-s1 and --slot2/-s2 must be provided, or neither may be provided')
#             obj_a, obj_b = obj_a[args.slot1 - 1], obj_b[args.slot2 - 1]
#     elif item == 'saves':
#         game_data = GameData.load(get_path(args.path))
#         obj_a, obj_b = game_data[args.slots[0] - 1], game_data[args.slots[1] - 1]
#     else:
#         raise ValueError(f'Unexpected {item=} to compare')
#
#     if args.unknowns:
#         keys = {k for k in obj_a._offsets_and_sizes if k.startswith('_unk')}
#     else:
#         keys = set(args.keys) if args.keys else None
#
#     obj_a.diff(obj_b, per_line=args.per_line, byte_diff=args.binary, keys=keys, max_len=1)


if __name__ == '__main__':
    main()
