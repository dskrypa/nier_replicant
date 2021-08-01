"""
Higher level classes for working with NieR Replicant ver.1.22474487139... save files.

:author: Doug Skrypa
"""

import logging
import shutil
from datetime import datetime, timedelta
from difflib import unified_diff
from functools import cached_property
from pathlib import Path
from typing import Union, Optional, Iterator, Collection

from construct.lib.containers import ListContainer, Container

from .constants import MAP_ZONE_MAP, SEED_RESULT_MAP
from .constructs import Gamedata, Savefile, Plot
from .utils import to_hex_and_str, pseudo_json, colored, unified_byte_diff, cached_classproperty, unique_path

__all__ = ['GameData', 'SaveFile']
log = logging.getLogger(__name__)


class Constructed:
    def __init_subclass__(cls, construct):  # noqa
        cls._construct = construct

    def __init__(self, data: bytes, parsed=None):
        self._data = data
        self._parsed = parsed or self._construct.parse(data)

    def __getitem__(self, key: str):
        return _clean(self._parsed[key])

    __getattr__ = __getitem__

    def __setitem__(self, key: str, value):
        self._parsed[key] = value

    @cached_classproperty
    def _offsets_and_sizes(cls):
        offsets_and_sizes = {}
        offset = 0
        for subcon in cls._construct.subcons:
            size = subcon.sizeof()  # TODO: Handle arrays differently?
            offsets_and_sizes[subcon.name] = (offset, size)
            offset += size
        return offsets_and_sizes

    def _build(self):
        return _build(self._parsed)

    def raw(self, key: str) -> bytes:
        offset, size = self._offsets_and_sizes[key]
        return self._data[offset: offset + size]  # noqa

    def raw_items(self):
        for key, (offset, size) in self._offsets_and_sizes.items():
            yield key, self._data[offset: offset + size]

    def diff(
        self,
        other: 'Constructed',
        *,
        max_len: Optional[int] = 30,
        per_line: int = 20,
        byte_diff: bool = False,
        keys: Collection[str] = None,
    ):
        found_difference = False
        for key, own_raw in self.raw_items():
            if keys and key not in keys:
                continue
            other_raw = other.raw(key)
            if own_raw != other_raw:
                own_val = self[key]
                if not found_difference:
                    found_difference = True
                    print(f'--- {self}')
                    print(f'+++ {other}')

                if isinstance(self, GameData) and key == 'slots':
                    for own_slot, other_slot in zip(self.slots, other.slots):
                        own_slot.diff(other_slot, max_len=max_len, per_line=per_line, byte_diff=byte_diff, keys=keys)
                elif not byte_diff and own_val != own_raw and not isinstance(own_val, (float, int, str)):
                    print(colored(f'@@ {key} @@', 6))
                    a, b = pseudo_json(own_val).splitlines(), pseudo_json(other[key]).splitlines()
                    for i, line in enumerate(unified_diff(a, b, n=2, lineterm='')):
                        if line.startswith('+'):
                            if i > 1:
                                print(colored(line, 2))
                        elif line.startswith('-'):
                            if i > 1:
                                print(colored(line, 1))
                        elif not line.startswith('@@ '):
                            print(line)
                elif max_len and isinstance(own_raw, bytes) and len(own_raw) > max_len:
                    unified_byte_diff(own_raw, other_raw, lineterm=key, struct=repr, per_line=per_line)
                else:
                    print(colored(f'@@ {key} @@', 6))
                    print(colored(f'- {own_val}', 1))
                    print(colored(f'+ {other[key]}', 2))

    def view(self, key: str, per_line: int = 40, hide_empty: Union[bool, int] = 10, **kwargs):
        data = self.raw(key)
        if isinstance(hide_empty, int):
            hide_empty = (len(data) / per_line) > hide_empty

        offset_fmt = '0x{{:0{}X}}:'.format(len(hex(len(data))) - 2)
        nul = b'\x00' * per_line
        last_os = len(data) // per_line
        is_empty, need_ellipsis = False, True
        for offset in range(0, len(data), per_line):
            nxt = offset + per_line
            line = data[offset:nxt]
            if hide_empty:
                was_empty = is_empty
                if (is_empty := line == nul) and was_empty and offset != last_os and data[nxt: nxt + per_line] == nul:
                    if need_ellipsis:
                        print('...')
                        need_ellipsis = False
                    continue

            need_ellipsis = True
            print(to_hex_and_str(offset_fmt.format(offset), line, fill=per_line, **kwargs))

    def view_unknowns(self, per_line: int = 40, hide_empty: Union[bool, int] = 10, **kwargs):
        for key in self._offsets_and_sizes:
            if key.startswith('_unk'):
                print(colored('\n{}  {}  {}'.format('=' * 30, key, '=' * 30), 14))
                self.view(key, per_line, hide_empty, **kwargs)

    def _pprint(self, key: str, val):
        if isinstance(val, dict):
            val = pseudo_json(val)
        print(f'{colored(key, 14)}: {val}')

    def pprint(self, unknowns: bool = False, keys: Collection[str] = None, **kwargs):
        last_was_view = False
        for key in self._offsets_and_sizes:
            if keys and key not in keys:
                continue
            val = self[key]
            if isinstance(val, bytes):
                if unknowns or not key.startswith('_unk'):
                    print(colored('\n{}  {}  {}'.format('=' * 30, key, '=' * 30), 14))
                    self.view(key, **kwargs)
                    last_was_view = True
            else:
                if last_was_view:
                    print()
                self._pprint(key, val)
                last_was_view = False


class GameData(Constructed, construct=Gamedata):
    def __init__(self, data: bytes, path: Path = None):
        super().__init__(data)
        self._path = path
        self.slots = [SaveFile(slot, i) for i, slot in enumerate(self._parsed.slots, 1)]

    @classmethod
    def load(cls, path: Union[str, Path]) -> 'GameData':
        path = Path(path).expanduser()
        log.debug(f'Loading game data from path={path.as_posix()}')
        with path.open('rb') as f:
            return cls(f.read(), path)

    def save(self, path: Union[str, Path] = None, backup: bool = True):
        """
        Save changes.

        :param path: Location where save file should be written (defaults to the path from which this save file was read
          if :meth:`.load` was used or an explicit path was provided)
        :param backup: Whether a backup copy of the original save file should be saved
        """
        path = path or self._path
        if not path:
            raise ValueError(f'A path is required to save {self}')
        if backup and path.exists():
            bkp_path = unique_path(path.parent, path.name, '.bkp')
            log.info(f'Creating backup: {bkp_path.as_posix()}')
            shutil.copy(path, bkp_path)
        log.info(f'Saving {path.as_posix()}')
        with Path(path).expanduser().open('wb') as f:
            f.write(self._construct.build(self._build()))

    def __repr__(self) -> str:
        return '<GameData[\n{}]>'.format(''.join(map('    {!r}\n'.format, self.slots)))

    @property
    def ok(self) -> bool:
        return all(f.ok for f in self.slots)

    def __getitem__(self, slot_or_key: Union[int, str]):
        return self.slots[slot_or_key] if isinstance(slot_or_key, int) else self._parsed[slot_or_key]

    def __iter__(self):
        yield from self.slots


class SaveFile(Constructed, construct=Savefile):
    """Represents one save slot."""

    def __init__(self, slot: Container, num: int):
        super().__init__(slot.data, slot.value)  # data/value are set by RawCopy for the raw bytes and parsed value
        self._num = num

    def __repr__(self) -> str:
        name = self.character if self.name.lower() in self.character.lower() else f'{self.name} ({self.character})'
        return (
            f'<SaveFile#{self._num}[{name}, Lv.{self.level} @ {self.location}][{self.play_time}]'
            f'[{self.save_time.isoformat(" ")}]>'
        )

    @property
    def ok(self) -> bool:
        return self._parsed.corruptness == 200

    @cached_property
    def play_time(self) -> str:
        hours, seconds = divmod(int(self._parsed.total_play_time), 3600)
        minutes, seconds = divmod(seconds, 60)
        return f'{hours:01d}:{minutes:02d}:{seconds:02d}'

    @cached_property
    def known_words(self) -> list[str]:
        return [w for w, v in self.words.items() if v]

    @cached_property
    def location(self) -> str:
        loc_part = '_'.join(self._parsed.map.split('_')[1:3])
        return MAP_ZONE_MAP.get(loc_part, self._parsed.map)

    @cached_property
    def garden(self) -> 'Garden':
        return Garden(self)

    def _pprint(self, key: str, val):
        if key == 'garden':
            print(f'{colored(key, 14)}:')
            self.garden.show(prefix='    ')
        else:
            super()._pprint(key, val)


class Garden:
    def __init__(self, save_file: SaveFile):
        self.save_file: SaveFile = save_file
        self.plots = [
            [GardenPlot(plot, r, i) for i, plot in enumerate(row)] for r, row in enumerate(save_file._parsed.garden)
        ]

    def __getitem__(self, row: int) -> list['GardenPlot']:
        return self.plots[row]

    def __iter__(self) -> Iterator['GardenPlot']:
        for row in self.plots:
            yield from row

    def show(self, func=str, prefix: str = ''):
        columns = [list(map(func, row)) for row in self.plots]
        row_fmt = '{}{{:>{}s}}  {{:>{}s}}  {{:>{}s}}'.format(prefix, *(max(map(len, col)) for col in columns))
        print('\n'.join(row_fmt.format(*row) for row in zip(*columns)))

    def update(self, dt: datetime = None, hours: int = None, fertilizer: Union[str, int] = None, water: int = None):
        if dt or hours:
            self.set_plant_times(dt, hours)
        if fertilizer or fertilizer == 0:
            self.set_fertilizer(fertilizer)
        if water:
            self.set_water(water)

    def set_plant_times(self, dt: datetime = None, hours: int = None):
        """
        Sets the plant time for all seeds in this garden.  Does not modify plots where a seed has not been planted.

        :param dt: The specific time to set as the time that all seeds were planted.  Mutually exclusive with ``hours``.
        :param hours: Number of hours earlier than the current time to set as the time that all seeds were planted.
          Mutually exclusive with ``dt``.
        """
        if (dt and hours) or (not dt and not hours):
            raise ValueError(f'set_plant_times() requires ONE of dt or hours')
        dt = dt or (datetime.now() - timedelta(hours=hours))
        for plot in self:
            if plot._parsed.seed != 255:
                plot._parsed.time = dt

    def set_fertilizer(self, fertilizer: Union[str, int]):
        """
        Sets the fertilizer used in all garden plots, regardless of whether a seed has been planted in that plot.

        :param fertilizer: One of ['None', 'Speed Fertilizer', 'Flowering Fertilizer', 'Bounty Fertilizer'] or an
          integer between 0-3, inclusive.
        """
        for plot in self:
            plot._parsed.fertilizer = fertilizer

    def set_water(self, water: int):
        kwargs = {'first': water >= 1, 'second': water >= 2}
        for plot in self:
            if plot._parsed.seed != 255:
                for key, val in kwargs.items():
                    setattr(plot._parsed.water, key, val)


class GardenPlot(Constructed, construct=Plot):
    def __init__(self, plot: Container, row: int, num: int):
        super().__init__(plot.data, plot.value)  # data/value are set by RawCopy for the raw bytes and parsed value
        self._row = row
        self._num = num

    @property
    def watered(self) -> str:
        return ''.join('\u25cb' if v else '\u2715' for k, v in self.water.items() if k != '_flagsenum')

    def __str__(self) -> str:
        planted = self.time.isoformat(' ') if self.time else None
        plant = SEED_RESULT_MAP.get(self.seed, self.seed)
        plant = 'None' if plant == 255 else plant
        fertilizer = self.fertilizer.split()[0]
        return f'\u2039{plant} | F:{fertilizer} | W:{self.watered} | {planted} | {self.direction:>5s}\u203a'

    def __repr__(self) -> str:
        planted = self.time.isoformat(' ') if self.time else None
        seed = 'None' if self.seed == 255 else self.seed
        plot, water, direction = f'{self._row}x{self._num}', self.watered, self.direction
        return f'<GardenPlot[{plot} @ {planted}, {seed} + {self.fertilizer}, water:{water}, dir: {direction}]>'


def _build(obj):
    if isinstance(obj, ListContainer):
        return [_build(li) for li in obj]
    elif isinstance(obj, Container):
        if set(obj) == {'offset1', 'length', 'offset2', 'data', 'value'}:
            return {'value': _build(obj.value)}
        return {key: _build(val) for key, val in obj.items() if key != '_io'}
    else:
        return obj


def _clean(obj):
    if isinstance(obj, ListContainer):
        return [_clean(li) for li in obj]
    elif isinstance(obj, Container):
        if set(obj) == {'offset1', 'length', 'offset2', 'data', 'value'}:
            return _clean(obj.value)
        return {key: _build(val) for key, val in obj.items() if key not in ('_io', '_flagsenum')}
    else:
        return obj