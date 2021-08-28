#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging
from collections import defaultdict
from io import StringIO

from nier.cli import ArgParser, get_steam_dir
from nier.save_file import GameData, Header, SaveFile
from nier.utils import colored, collapsed_ranges_str

log = logging.getLogger(__name__)


def parser():
    parser = ArgParser(description='Nier Replicant ver.1.22474487139... Save File Diff Tool')

    count_parser = parser.add_subparser('action', 'count', 'Count changes to fields')
    count_parser.add_argument('--unknowns', '-u', action='store_true', help='Only show unknown fields in output')
    count_parser.add_argument('--show_names', '-n', action='store_true', help='Show the names of the files with the unique values')

    diff_parser = parser.add_subparser('action', 'diff', 'Show the diff for a particular field')
    diff_parser.add_argument('location', choices=('header', 'save'), help='The field to display')
    diff_parser.add_argument('field', help='The field to display')
    diff_parser.add_argument('--global', '-g', action='store_true', help='Highlight changes across all lines (default: only between the lines where they changed)')
    group = diff_parser.add_argument_group('Diff Options')
    group.add_argument('--per_line', '-L', type=int, default=8, help='Number of bytes to print per line (binary data only)')
    group.add_argument('--binary', '-b', action='store_true', help='Show the binary version, even if a higher level representation is available')
    fields = diff_parser.add_argument_group('Field Options').add_mutually_exclusive_group()
    fields.add_argument('--keys', '-k', nargs='+', help='Specific keys/attributes to include in the diff (default: all)')
    fields.add_argument('--unknowns', '-u', action='store_true', help='Only show unknown fields in output')

    for _parser in (count_parser, diff_parser):
        _parser.add_argument('--dir', '-d', metavar='PATH', help='Directory containing GAMEDATA files saved by save_watcher')
        _parser.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')
    parser.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')
    return parser


def main():
    args = parser().parse_args()
    log_fmt = '%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s' if args.verbose else '%(message)s'
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format=log_fmt)

    action = args.action
    if action == 'count':
        count_changes(load_data(args.dir), args.unknowns, args.show_names)
    elif action == 'diff':
        save_data = load_data(args.dir)
        multi_diff(args.location, args.field, save_data, getattr(args, 'global'))
    else:
        raise ValueError(f'Unexpected {action=}')


def load_data(save_dir: str = None) -> dict[Path, tuple[Header, SaveFile]]:
    save_dir = Path(save_dir).expanduser().resolve() if save_dir else get_steam_dir()
    pat = 'GAMEDATA_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9]'
    save_data = {}
    for pat in (pat, pat + '[0-9]'):
        for path in save_dir.glob(pat):
            gd = GameData.load(path)
            save_data[path] = (gd.header, max(gd.slots))
    return save_data


def count_changes(
    save_data: dict[Path, tuple[Header, SaveFile]], only_unknowns: bool = False, show_names: bool = False
):
    header_fields = defaultdict(lambda: defaultdict(list))
    slot_fields = defaultdict(lambda: defaultdict(list))
    for path, (header, slot) in save_data.items():
        # print(f'{path.name}: {header}, {slot}')
        for field, value in header.raw_items():
            header_fields[field][value].append(path)
        for field, value in slot.raw_items():
            slot_fields[field][value].append(path)

    print(f'Total file count: {len(save_data)}')
    for label, field_dict in {'Header': header_fields, 'Save file slot': slot_fields}.items():
        print(f'{label} field unique value counts:')
        for field, val_paths in field_dict.items():
            if (not only_unknowns or field.startswith('_')) and (num_values := len(val_paths)) > 1:
                print(f'  - {field} (len={len(next(iter(val_paths)))}): {num_values}')
                if show_names:
                    for value, paths in val_paths.items():
                        print('     - {}'.format(collapsed_ranges_str((path.name for path in paths))))


def multi_diff(
    location: str, field: str, save_data: dict[Path, tuple[Header, SaveFile]], global_highlights: bool = False
):
    name_val_map = {
        path.name: (header if location == 'header' else slot).raw(field) for path, (header, slot) in save_data.items()
    }
    highlight = highlight_indices(name_val_map.values()) if global_highlights else None
    fmt = '{{:<{}s}}: {{}}'.format(max(map(len, name_val_map)))
    last = None
    for name, value in name_val_map.items():
        if value != last:
            sio = StringIO()
            hex_val = value.hex(' ', -4)
            highlights = highlight if global_highlights else () if last is None else highlight_indices((last, value))
            n = 0
            for a, b in highlights:
                sio.write(hex_val[n:a])
                sio.write(colored(hex_val[a:b], fg=11, bg=2))
                n = b
            sio.write(hex_val[n:])
            last = value

            print(fmt.format(name, sio.getvalue()))


def _all_equal(values) -> bool:
    ivalues = iter(values)
    first = next(ivalues)
    return all(first == value for value in ivalues)


def highlight_indices(values):
    changed = (not _all_equal(vals) for vals in zip(*values))
    highlight = [(n, n + 2) for i, b in enumerate(changed) if b and (n := i * 2 + i // 4) is not None]  # noqa
    return highlight


if __name__ == '__main__':
    main()
