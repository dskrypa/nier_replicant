import json
import sys
from collections.abc import Mapping, KeysView, ValuesView, Callable
from datetime import datetime, date, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from struct import calcsize, unpack_from, error as StructError
from traceback import format_tb
from types import TracebackType
from typing import Union
from unicodedata import category

from colored import stylize, fg


def colored(text, fg_color):
    return stylize(text, fg(fg_color))


def to_hex_and_str(
    pre,
    data: bytes,
    *,
    encoding: str = 'utf-8',
    fill: int = 0,
    struct: Union[str, Callable] = None,
    offset: int = 0,
    pad: bool = False,
) -> str:
    """
    Format the given bytes to appear similar to the format used by xxd.  Intended to be called for each line - splitting
    the data into the amount to appear on each line should be done before calling this function.

    :param pre: Line prefix
    :param data: The binary data to be converted
    :param encoding: Encoding to use for the str portion
    :param fill: Ensure hex fills the amount of space that would be required for this many bytes
    :param struct: Interpret contents as an array of the given struct format character
    :param offset: Offset to apply before processing contents as a struct array
    :param pad: Pad the string portion to ensure alignment when escaped characters are found
    :return: String containing both the hex and str representations
    """
    try:
        replacements = to_hex_and_str._replacements
    except AttributeError:
        repl_map = {c: '.' for c in map(chr, range(sys.maxunicode + 1)) if category(c) == 'Cc'}
        to_hex_and_str._replacements = replacements = str.maketrans(repl_map | {'\r': '\\r', '\n': '\\n', '\t': '\\t'})

    as_hex = data.hex(' ', -4)
    if pad:
        esc = {'\r', '\n', '\t'}
        as_str = ''.join(c if c in esc else f' {c}' for c in data.decode(encoding, 'replace')).translate(replacements)
    else:
        as_str = data.decode(encoding, 'replace').translate(replacements)
    if fill:
        if (to_fill := fill * 2 + (fill // 4) - 1 - len(as_hex)) > 0:
            as_hex += ' ' * to_fill
        if to_fill := fill * (1 + int(pad)) - len(as_str):
            as_str += ' ' * to_fill

    if struct:
        if isinstance(struct, str):
            from_struct = []
            for i in range(offset, len(data), calcsize(struct)):
                try:
                    from_struct.extend(unpack_from(struct, data, i))
                except StructError:
                    pass
        elif isinstance(struct, Callable):
            from_struct = struct(data)
        else:
            raise TypeError(f'Unexpected struct type={type(struct)}')
        return f'{pre} {as_hex}  |  {as_str}  |  {from_struct}'
    return f'{pre} {as_hex}  |  {as_str}'


def to_bin_str(data: bytes, sep: str = ' '):
    return sep.join(map('{:08b}'.format, data))


class PseudoJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (set, KeysView)):
            return sorted(o)
        elif isinstance(o, ValuesView):
            return list(o)
        elif isinstance(o, Mapping):
            return dict(o)
        elif isinstance(o, bytes):
            try:
                return o.decode('utf-8')
            except UnicodeDecodeError:
                return o.hex(' ', -4)
        elif isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S %Z')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, (type, timedelta)):
            return str(o)
        elif isinstance(o, TracebackType):
            return ''.join(format_tb(o)).splitlines()
        elif hasattr(o, '__to_json__'):
            return o.__to_json__()
        elif hasattr(o, '__serializable__'):
            return o.__serializable__()
        try:
            return super().default(o)
        except TypeError:
            return repr(o)
        except UnicodeDecodeError:
            return o.decode('utf-8', 'replace')


def pseudo_json(data) -> str:
    return json.dumps(data, cls=PseudoJsonEncoder, sort_keys=True, indent=4, ensure_ascii=False)


def unified_byte_diff(
    a: bytes, b: bytes, n: int = 3, lineterm: str = '', color: bool = True, per_line: int = 20, **kwargs
):
    offset_fmt = '{{}} 0x{{:0{}X}}:'.format(len(hex(max(len(a), len(b)))) - 2).format
    av = memoryview(a)
    bv = memoryview(b)
    a = [av[i: i + per_line] for i in range(0, len(a), per_line)]
    b = [bv[i: i + per_line] for i in range(0, len(b), per_line)]

    for group in SequenceMatcher(None, a, b).get_grouped_opcodes(n):
        first, last = group[0], group[-1]
        file1_range = _format_range_unified(first[1], last[2])
        file2_range = _format_range_unified(first[3], last[4])
        range_str = f'@@ -{file1_range} +{file2_range} @@'
        range_str = colored(range_str, 6) if color else range_str
        print(f'{range_str} {lineterm}' if lineterm else range_str)

        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                for i, line in enumerate(a[i1:i2], i1):
                    print(to_hex_and_str(offset_fmt(' ', i * per_line), line.tobytes(), fill=per_line, **kwargs))
                continue
            if tag in {'replace', 'delete'}:
                for i, line in enumerate(a[i1:i2], i1):
                    line_str = to_hex_and_str(offset_fmt('-', i * per_line), line.tobytes(), fill=per_line, **kwargs)
                    print(colored(line_str, 1) if color else line_str)
            if tag in {'replace', 'insert'}:
                for i, line in enumerate(b[j1:j2], j1):
                    line_str = to_hex_and_str(offset_fmt('+', i * per_line), line.tobytes(), fill=per_line, **kwargs)
                    print(colored(line_str, 2) if color else line_str)


def _format_range_unified(start: int, stop: int) -> str:
    """Convert range to the "ed" format. Copied from difflib"""
    # Per the diff spec at http://www.unix.org/single_unix_specification/
    beginning = start + 1     # lines start numbering with one
    length = stop - start
    if length == 1:
        return str(beginning)
    if not length:
        beginning -= 1        # empty ranges begin at line just before the range
    return f'{beginning},{length}'


class cached_classproperty:
    def __init__(self, func):
        self.__doc__ = func.__doc__
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.func = func
        self.values = {}

    def __get__(self, obj, cls):
        try:
            return self.values[cls]
        except KeyError:
            self.values[cls] = value = self.func.__get__(obj, cls)()  # noqa
            return value


def unique_path(parent: Path, stem: str, suffix: str, seps=('_', '-'), n: int = 1, add_date: bool = True) -> Path:
    """
    :param parent: Directory in which a unique file name should be created
    :param stem: File name without extension
    :param suffix: File extension, including `.`
    :param seps: Separators between stem and date/n, respectfully.
    :param n: First number to try; incremented by 1 until adding this value would cause the file name to be unique
    :param add_date: Whether a date should be added before n. If True, a date will always be added.
    :return: Path with a file name that does not currently exist in the target directory
    """
    date_sep, n_sep = seps
    if add_date:
        stem = f'{stem}{date_sep}{datetime.now().strftime("%Y-%m-%d")}'
    name = stem + suffix
    while (path := parent.joinpath(name)).exists():
        name = f'{stem}{n_sep}{n}{suffix}'
        n += 1
    return path
