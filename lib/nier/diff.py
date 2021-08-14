"""
Object and binary data diff utilities

:author: Doug Skrypa
"""

import math
from collections import deque
from difflib import SequenceMatcher, unified_diff

from .utils import colored, to_hex_and_str, pseudo_json, pseudo_json_rows

DIFF_TAG_OUTPUT_MAP = {'equal': (' ', None), 'delete': ('-', 1), 'insert': ('+', 2)}


def pseudo_json_diff(a, b, lines: bool, line_term: str = ''):
    func = pseudo_json_rows if lines else pseudo_json
    a, b = func(a).splitlines(), func(b).splitlines()
    for i, line in enumerate(unified_diff(a, b, n=2, lineterm=colored(f' {line_term}', 7))):
        if line.startswith('+'):
            if i > 1:
                print(colored(line, 2))
        elif line.startswith('-'):
            if i > 1:
                print(colored(line, 1))
        elif line.startswith('@@ '):
            print(colored(line, 3))
        else:
            print(line)


def unified_byte_diff(
    a: bytes,
    b: bytes,
    n: int = 3,
    lineterm: str = '',
    color: bool = True,
    per_line: int = 20,
    line_diff: bool = False,
    **kwargs
):
    print_func = _print_line_diff if line_diff else _print_grouped_diff
    offset_fmt = '{{}} 0x{{:0{}X}}:'.format(len(hex(max(len(a), len(b)))) - 2).format
    av, bv = memoryview(a), memoryview(b)
    a = [av[i: i + per_line] for i in range(0, len(a), per_line)]
    b = [bv[i: i + per_line] for i in range(0, len(b), per_line)]

    groups = []
    auto_junk_threshold = n * 2 + 10
    for group in SequenceMatcher(None, a, b).get_grouped_opcodes(n):
        (a1, b1), (a2, b2) = group[0][1:4:2], group[-1][2:5:2]
        if a2 - a1 > auto_junk_threshold or b2 - b1 > auto_junk_threshold:
            # SequenceMatcher is slower with autojunk=False, but more accurate for binary data.
            # In some cases, a false-positive match of a large range of 0s will ruin the diff with autojunk=True
            # In those cases, we can re-try with autojunk=False.  Specifying a junk function for 0s did not work.
            groups = SequenceMatcher(None, a, b, autojunk=False).get_grouped_opcodes(n)
            break
        else:
            groups.append(group)

    for group in groups:
        (a1, b1), (a2, b2) = group[0][1:4:2], group[-1][2:5:2]
        range_str = colored(f'@@ -{_format_range_unified(a1, a2)} +{_format_range_unified(b1, b2)} @@', 6, color)
        print(f'{range_str} {lineterm}' if lineterm else range_str)
        print_func(a, b, group, offset_fmt, per_line, color, kwargs)


def unified_byte_line_diff(
    a: bytes, b: bytes, n: int = 3, lineterm: str = '', color: bool = True, per_line: int = 20, **kwargs
):
    offset = '{{}} 0x{{:0{}X}}:'.format(len(hex(max(len(a), len(b)))) - 2).format
    av, bv = memoryview(a), memoryview(b)
    a = [av[i: i + per_line] for i in range(0, len(a), per_line)]
    b = [bv[i: i + per_line] for i in range(0, len(b), per_line)]

    bpl = per_line
    for group in group_diff_lines(a, b, n):
        range_str = colored('@@ -{0} +{0} @@'.format(_format_range_unified(group[0][1], group[-1][2])), 6, color)
        print(f'{range_str} {lineterm}' if lineterm else range_str)
        for tag, start, end in group:
            if tag == 'replace':
                for i, (rmv_b, add_b) in enumerate(zip(a[start:end], b[start:end]), start):
                    print(colored(to_hex_and_str(offset('-', i * bpl), rmv_b.tobytes(), fill=bpl, **kwargs), 1, color))
                    print(colored(to_hex_and_str(offset('+', i * bpl), add_b.tobytes(), fill=bpl, **kwargs), 2, color))
            else:
                _print_diff_sub_group(a, tag, start, end, offset, bpl, color, kwargs)


def group_diff_lines(a, b, n: int = 3):
    group = []
    last = None
    for tag, start, end in _group_diff_lines(a, b, n):
        if last is None or start - last == 1:
            group.append((tag, start, end + 1))
        else:
            if group:
                yield group
            group = [(tag, start, end + 1)]

        last = end

    if group:
        yield group


def _group_diff_lines(a, b, n: int = 3):
    same_buf = deque(maxlen=n)
    post_diff = False
    diff_start = diff_end = None
    for i, (a_line, b_line) in enumerate(zip(a, b)):
        if same_buf and ((post_diff and len(same_buf) == n) or (diff_start is not None and diff_start == diff_end)):
            e1 = same_buf.popleft()
            yield 'equal', e1, same_buf.pop() if same_buf else e1
            same_buf.clear()
            post_diff = False

        if a_line == b_line:
            same_buf.append(i)
            if diff_end is not None:
                yield 'replace', diff_start, diff_end
                diff_start = diff_end = None
                post_diff = True
        else:
            diff_end = i
            if diff_start is None:
                diff_start = i

    if same_buf and post_diff:
        e1 = same_buf.popleft()
        yield 'equal', e1, same_buf.pop() if same_buf else e1
    elif diff_end is not None:
        yield 'replace', diff_start, diff_end


def _print_grouped_diff(a, b, group, offset_fmt, per_line, color, kwargs):
    for tag, i1, i2, j1, j2 in group:
        if tag == 'replace':
            _print_diff_sub_group(a, 'delete', i1, i2, offset_fmt, per_line, color, kwargs)
            _print_diff_sub_group(b, 'insert', j1, j2, offset_fmt, per_line, color, kwargs)
        else:
            data, start, end = (a, i1, i2) if tag in {'equal', 'delete'} else (b, j1, j2)
            _print_diff_sub_group(data, tag, start, end, offset_fmt, per_line, color, kwargs)


def _print_line_diff(a, b, group, offset_fmt, bpl, color, kwargs):
    print('Group:',  '++ '.join(f'{tag} a[{i1}:{i2}] b[{j1}:{j2}]' for tag, i1, i2, j1, j2 in group))
    for tag, i1, i2, j1, j2 in group:
        print(f'{tag} a[{i1}:{i2}] b[{j1}:{j2}]')
        if tag == 'replace':
            # This could potentially fail with different sized inputs, but for this, they will always be the same
            start, end = min(i1, j1), max(i2, j2)
            for i, (rmv_b, add_b) in enumerate(zip(a[start:end], b[start:end]), start):
                print(colored(to_hex_and_str(offset_fmt('-', i * bpl), rmv_b.tobytes(), fill=bpl, **kwargs), 1, color))
                print(colored(to_hex_and_str(offset_fmt('+', i * bpl), add_b.tobytes(), fill=bpl, **kwargs), 2, color))
        else:
            data, start, end = (a, i1, i2) if tag in {'equal', 'delete'} else (b, j1, j2)
            _print_diff_sub_group(data, tag, start, end, offset_fmt, bpl, color, kwargs)


def _print_diff_sub_group(data, tag, start, end, offset_fmt, bpl, do_color, kwargs):
    prefix, color = DIFF_TAG_OUTPUT_MAP[tag]
    for i, line in enumerate(map(memoryview.tobytes, data[start:end]), start):
        print(colored(to_hex_and_str(offset_fmt(prefix, i * bpl), line, fill=bpl, **kwargs), color, do_color))


def _format_range_unified(start: int, stop: int) -> str:
    """Convert range to the "ed" format. Copied from difflib"""
    # Per the diff spec at http://www.unix.org/single_unix_specification/
    return str(start + 1) if (length := stop - start) == 1 else f'{start + 1 if length else start},{length}'


def bit_diff_index(a: int, b: int) -> int:
    """
    Determines which bit changed between values a and b.  Intended to make it easier to decode bit-packed arrays of
    booleans.

    For given bytes (as ints) a and b, the difference is computed via ``diff = a xor b``.  The bit that changed (the
    exponent of 2 such that ``2 ** exp == diff``) is computed via ``exp = math.log(diff, 2)``.  The value that this
    function returns is that exponent.
    """
    if not (0 <= a <= 255 and 0 <= b <= 255):
        raise ValueError('bit_diff_index only supports a diff between 2 individual bytes')
    diff = a ^ b
    exp = math.log(diff, 2)
    index = int(exp)
    if exp != index:
        raise ValueError(f'{a=} and {b=} differ by more than 1 bit')
    return index
