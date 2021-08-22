#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging
from enum import Enum
from io import BytesIO
from struct import unpack_from, error as StructError

from nier.cli import ArgParser, get_path
from nier.utils import colored

log = logging.getLogger(__name__)

FORMATS = {
    # '?': ('bool', 1),
    'b': ('int8', 1),   'h': ('int16', 2),      'i': ('int32', 4),      'q': ('int64', 8),
    'B': ('uint8', 1),  'H': ('uint16', 2),     'I': ('unit32', 4),     'Q': ('uint64', 8),
                        'e': ('float16', 2),    'f': ('float32', 4),    'd': ('float64', 8),
}


def parser():
    parser = ArgParser(description='View the diff between lines of data stored as hex')
    parser.add_argument('file', help='Path to the file from which hex lines should be read')
    parser.add_argument('--offset', '-o', type=int, default=0, help='Offset from the beginning of the data in bytes to start struct matching')
    parser.add_argument('--endian', '-e', choices=('big', 'little', 'native'), help='Interpret values with the given endianness')
    parser.add_argument('--verbose', '-v', action='store_true', help='Increase logging verbosity')
    return parser


def main():
    args = parser().parse_args()
    log_fmt = '%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s' if args.verbose else '%(message)s'
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format=log_fmt)

    path = Path(args.file).expanduser().resolve()
    data = (''.join(line.split()) for line in path.read_text('utf-8').splitlines())

    unpacked_lines = {}
    for line in data:
        bio = BytesIO()
        for i in range(0, len(line), 2):
            bio.write(bytes.fromhex(line[i: i + 2]))

        unpacked = view_unpacked(bio.getvalue(), offset=args.offset, endian=args.endian)
        unpacked_lines[unpacked.pop('hex')] = unpacked

    bar = '=' * 50
    for i, data_type in enumerate(sorted(f[0] for f in FORMATS.values())):
        if i:
            print()
        print(colored(f'{bar} {data_type} {bar}', 14))
        for line, unpacked in unpacked_lines.items():
            print(f'{line}: {unpacked[data_type]}')


class Endian(Enum):
    NATIVE = '@'            # Native byte order, native size, native alignment
    NATIVE_STANDARD = '='   # Native byte order, standard size
    LITTLE = '<'            # Little-endian byte order, standard size
    BIG = '>'               # Big-endian byte order, standard size

    @classmethod
    def _missing_(cls, value):
        return cls._member_map_.get(value.upper() if isinstance(value, str) else value)


def view_unpacked(data: bytes, *, split: int = 4, sep: str = ' ', offset: int = 0, endian: Endian = None):
    endian = Endian(endian or '@')
    unpacked = {'bin': sep.join(map('{:08b}'.format, data)), 'hex': data.hex(sep, split)}
    for fc, (name, width) in FORMATS.items():
        fmt = endian.value + fc
        from_struct = []
        for i in range(offset, len(data), width):
            try:
                from_struct.extend(unpack_from(fmt, data, i))
            except StructError:
                pass
        unpacked[name] = from_struct
    return unpacked


if __name__ == '__main__':
    main()
