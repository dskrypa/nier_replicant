"""
Higher level classes for working with NieR Replicant ver.1.22474487139... save files.

:author: Doug Skrypa
"""

import gzip
import logging
import shutil
import struct
from base64 import b64decode
from copy import deepcopy
from datetime import datetime, timedelta
from functools import cached_property
from pathlib import Path
from typing import Union, Optional, Iterator, Collection, Any

from construct.lib.containers import ListContainer, Container

from .constants import EMPTY_SAVE_SLOT, MAP_ZONE_MAP, SEED_RESULT_MAP
from .constructs import Gamedata, Savefile, Plot, Header
from .diff import pseudo_json_diff, unified_byte_line_diff
from .utils import to_hex_and_str, pseudo_json, colored, cached_classproperty, unique_path, without_unknowns

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
        row_keys = {'quests', 'quests_b'}
        found_difference = False
        for key, own_raw in self.raw_items():
            if (keys and key not in keys) or ((other_raw := other.raw(key)) == own_raw):
                continue
            if not found_difference:
                found_difference = True
                print(f'--- {self}\n+++ {other}')

            own_val = self[key]
            if isinstance(self, GameData) and key in ('slots', 'header'):
                if key == 'slots':
                    for own, other_slot in zip(self.slots, other.slots):
                        own.diff(other_slot, max_len=max_len, byte_diff=byte_diff, keys=keys, per_line=per_line)
                elif key == 'header':
                    h_keys = set(keys).difference({'header'}) if keys else None
                    self.header.diff(other.header, max_len=max_len, byte_diff=byte_diff, keys=h_keys, per_line=per_line)
            elif not byte_diff and own_val != own_raw and not isinstance(own_val, (float, int, str)):
                print(colored(f'@@ {key} @@', 6))
                pseudo_json_diff(own_val, other[key], key in row_keys, key)
            elif max_len and isinstance(own_val, bytes) and len(own_raw) > max_len:
                unified_byte_line_diff(own_raw, other_raw, lineterm=key, struct=repr, per_line=per_line)
                # unified_byte_diff(own_raw, other_raw, lineterm=key, struct=repr, per_line=per_line)
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

    def _pprint(self, key: str, val, sort_keys: bool = True, unknowns: bool = False):
        if isinstance(val, dict):
            val = pseudo_json(val if unknowns else without_unknowns(val), sort_keys=sort_keys)
        print(f'{colored(key, 14)}: {val}')

    def pprint(
        self,
        unknowns: bool = False,
        keys: Collection[str] = None,
        binary: bool = False,
        sort_keys: bool = True,
        **kwargs,
    ):
        last_was_view = False
        for key in self._offsets_and_sizes:
            if (keys and key not in keys) or (not unknowns and key.startswith('_unk')):
                continue

            if binary:
                print(colored('\n{}  {}  {}'.format('=' * 30, key, '=' * 30), 14))
                self.view(key, **kwargs)
            else:
                val = self[key]
                if isinstance(val, bytes):
                    print(colored('\n{}  {}  {}'.format('=' * 30, key, '=' * 30), 14))
                    self.view(key, **kwargs)
                    last_was_view = True
                else:
                    if last_was_view:
                        print()
                    self._pprint(key, val, sort_keys=sort_keys, unknowns=unknowns)
                    last_was_view = False

    def find_number(self, value: Union[int, float], unknowns_only: bool = True):
        formats = {
            'b': ('int8', 1), 'h': ('int16', 2), 'i': ('int32', 4), 'q': ('int64', 8),
            'B': ('uint8', 1), 'H': ('uint16', 2), 'I': ('unit32', 4), 'Q': ('uint64', 8),
            'e': ('float16', 2), 'f': ('float32', 4), 'd': ('float64', 8),
        }
        for endian in '<>':
            for f, (name, width) in formats.items():
                try:
                    byte_val = struct.pack(f'{endian}{f}', value)
                except struct.error:
                    pass
                else:
                    # log.debug(f'Searching for {byte_val=}')
                    print(f'Searching for {byte_val=}')
                    for key, data in self.raw_items():
                        if byte_val in data:
                        # if (not unknowns_only or key.startswith('_unk')) and byte_val in data:
                            # log.info(f'Found {value=} in {key=} as {name} with {byte_val=}')
                            print(f'Found {value=} in {key=} as {name} with {byte_val=}')


class GameData(Constructed, construct=Gamedata):
    """Represents the full GAMEDATA file, including all save slots."""

    def __init__(self, data: bytes, path: Path = None):
        super().__init__(data)
        self._path = path
        self.header = GameDataHeader(self._parsed.header, self)
        self.slots = [SaveFile(slot, i, self) for i, slot in enumerate(self._parsed.slots, 1)]

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
        path = Path(path).expanduser() if path else self._path
        if not path:
            raise ValueError(f'A path is required to save {self}')

        data = self._construct.build(self._build())  # Prevent creating an empty file if an exception is raised

        if backup and path.exists():
            bkp_path = unique_path(path.parent, path.name, '.bkp')
            log.info(f'Creating backup: {bkp_path.as_posix()}')
            shutil.copy(path, bkp_path)

        log.info(f'Saving {path.as_posix()}')
        with Path(path).expanduser().open('wb') as f:
            f.write(data)

    def __repr__(self) -> str:
        return '<GameData[\n{}]>'.format(''.join(map('    {!r}\n'.format, self.slots)))

    @property
    def ok(self) -> bool:
        return all(f.ok for f in self.slots)

    def __getitem__(self, slot_or_key: Union[int, str]) -> Union['SaveFile', Any]:
        """
        Slots are 0-indexed.  Slots 0-2 (saves 1-3) are the 3 that are visible in-game.  I assume slots 3-6 are where
        "deleted" saves are stored by ending D.

        :param slot_or_key: A slot index or key for a sub-construct
        :return: A :class:`SaveFile` for the given slot, or the specified sub-construct
        """
        if isinstance(slot_or_key, int):
            return self.slots[slot_or_key]
        else:
            return _clean(self._parsed[slot_or_key])

    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(f'{self.__class__.__name__} has no attribute {key}') from e

    def __setitem__(self, slot: int, value: 'SaveFile'):
        """
        Overwrite a save slot with a different :class:`SaveFile`.  If the save file originated from a :class:`GameData`
        object (i.e., if its :attr:`SaveFile._parent` attribute was set), then a deep copy of the :class:`SaveFile` will
        be stored in this one.  That means that any subsequent changes to the original :class:`SaveFile` will not be
        reflected when saving this game data, so a new reference to the slot must be obtained to make further changes.

        :param slot: The slot to overwrite
        :param value: The :class:`SaveFile` to be used in the specified slot
        """
        if not 0 <= slot <= 6:
            raise ValueError(f'Invalid slot index={slot!r}')
        if not isinstance(value, SaveFile):
            raise TypeError(f'Can only set SaveFile slot values - type={type(value).__name__} is not supported')
        if value._parent:
            value = value.copy()
        value._parent = self
        self._parsed.slots[slot] = {'data': value._data, 'value': value._parsed}
        self.slots[slot] = value
        value._num = slot + 1

    def __delitem__(self, slot: int):
        if not isinstance(slot, int):
            raise TypeError(f'Can only delete SaveFile slot values - index type={type(slot).__name__} is not supported')
        self[slot] = SaveFile.empty()

    def __iter__(self) -> Iterator['SaveFile']:
        """Iterate over the first 3 :class:`SaveFile`s"""
        yield from self.slots[:3]


class GameDataHeader(Constructed, construct=Header):
    def __init__(self, data: Union[Container, bytes], parent: GameData = None):
        self._parent = parent
        if isinstance(data, bytes):
            super().__init__(data)
        else:
            super().__init__(data['data'], data['value'])  # raw bytes data / parsed value from RawCopy

    # def __repr__(self) -> str:
    #     return f'<GameDataHeader[]>'


class SaveFile(Constructed, construct=Savefile):
    """Represents one save slot."""

    def __init__(self, slot: Union[Container, bytes], num: int, parent: GameData = None):
        self._parent = parent
        if isinstance(slot, bytes):
            super().__init__(slot)  # Loaded directly from file
        else:
            super().__init__(slot['data'], slot['value'])  # raw bytes data / parsed value from RawCopy
        self._num = num

    def __repr__(self) -> str:
        time = self.save_time.isoformat(' ') if isinstance(self.save_time, datetime) else 'N/A'
        return f'<SaveFile#{self._num}[{time}][{self.play_time}][{self._name}, Lv.{self.level + 1} @ {self.location}]>'

    @property
    def ok(self) -> bool:
        return self._parsed.corruptness == 200

    @cached_property
    def _name(self) -> str:
        return self.character if self.name.lower() in self.character.lower() else f'{self.name} ({self.character})'

    @cached_property
    def play_time(self) -> str:
        hours, seconds = divmod(int(self._parsed.total_play_time), 3600)
        minutes, seconds = divmod(seconds, 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

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

    def _pprint(self, key: str, val, sort_keys: bool = True, unknowns: bool = False):
        if key == 'garden':
            print(f'{colored(key, 14)}:')
            self.garden.show(prefix='    ')
        else:
            if key in {'quests', 'quests_b'}:
                a = 'started={started}, stages={stages}, done={done}'.format
                b = 'started={started}, done={done}'.format
                val = {k: a(**v) if 'stages' in v else b(**v) for k, v in without_unknowns(val).items()}
            super()._pprint(key, val, sort_keys, unknowns=unknowns)

    def update_quest(self, name: str, started: bool, done: bool, **kwargs):
        self._parsed['quests'][name] = {'started': started, 'done': done, **kwargs}

    def save(self, path: Union[str, Path]):
        """
        Save this save file/slot to a separate file.

        :param path: Location where the file should be written
        :raises: :class:`ValueError` if the specified path already exists.
        """
        path = Path(path).expanduser()
        if path.exists() and path.is_dir():
            path = path.joinpath(f'{self._name} - Lv{self.level} - {self.location} - {int(self.total_play_time)}.sav')
        if path.exists():
            raise ValueError(f'Invalid path={path.as_posix()} - it already exists')
        elif not path.parent.exists():
            path.parent.mkdir(parents=True)

        data = self._construct.build(self._build())  # Prevent creating an empty file if an exception is raised
        log.info(f'Saving {path.as_posix()}')
        with Path(path).expanduser().open('wb') as f:
            f.write(data)

    @classmethod
    def load(cls, path: Union[str, Path]) -> 'SaveFile':
        path = Path(path).expanduser()
        log.debug(f'Loading save slot from path={path.as_posix()}')
        with path.open('rb') as f:
            return cls(f.read(), -1)

    def copy(self) -> 'SaveFile':
        """Create a deep copy of this :class:`SaveFile` with no :class:`GameData` parent."""
        return self.__class__({'data': self._data, 'value': deepcopy(self._parsed)}, self._num)

    @classmethod
    def empty(cls) -> 'SaveFile':
        """Creates an empty :class:`SaveFile`"""
        return cls(gzip.decompress(b64decode(EMPTY_SAVE_SLOT)), -1)


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

    def update(
        self,
        dt: datetime = None,
        hours: int = None,
        fertilizer: Union[str, int] = None,
        water: int = None,
        plots: Collection[int] = None,
        **kwargs
    ):
        if dt or hours:
            self.set_plant_times(dt, hours, plots=plots)
        if fertilizer or fertilizer == 0:
            self.set_fertilizer(fertilizer, plots=plots, **kwargs)
        if water:
            self.set_water(water, plots=plots)

    def set_plant_times(self, dt: datetime = None, hours: int = None, plots: Collection[int] = None):
        """
        Sets the plant time for all seeds in this garden.  Does not modify plots where a seed has not been planted.

        :param dt: The specific time to set as the time that all seeds were planted.  Mutually exclusive with ``hours``.
        :param hours: Number of hours earlier than the current time to set as the time that all seeds were planted.
          Mutually exclusive with ``dt``.
        :param plots: Specific plots for which the plant time should be set (default: all)
        """
        if (dt and hours) or (not dt and not hours):
            raise ValueError('set_plant_times() requires ONE of dt or hours')
        dt = dt or (datetime.now() - timedelta(hours=hours)).replace(microsecond=0)
        for i, plot in enumerate(self):
            if (not plots or i in plots) and plot._parsed.seed != 255:
                plot._parsed.time = dt

    def set_fertilizer(
        self,
        fertilizer: Union[str, int],
        only_planted: bool = False,
        only_unfertilized: bool = False,
        plots: Collection[int] = None,
    ):
        """
        Sets the fertilizer used in all garden plots, regardless of whether a seed has been planted in that plot.

        :param fertilizer: One of ['None', 'Speed Fertilizer', 'Flowering Fertilizer', 'Bounty Fertilizer'] or an
          integer between 0-3, inclusive.
        :param only_planted: Only set the specified fertilizer for plots have have a seed planted already (default: set
          for all plots)
        :param only_unfertilized: Only set the specified fertilizer for plots that have no fertilizer already in use
          (default: set for all plots)
        :param plots: Specific plots that should be fertilized (default: all)
        """
        for i, plot in enumerate(self):
            if (only_planted and plot._parsed.seed == 255) or (only_unfertilized and plot._parsed.fertilizer != 0):
                continue
            elif not plots or i in plots:
                plot._parsed.fertilizer = fertilizer

    def set_water(self, water: int, plots: Collection[int] = None):
        kwargs = {'first': water >= 1, 'second': water >= 2}
        for i, plot in enumerate(self):
            if plot._parsed.seed != 255 and (not plots or i in plots):
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
        if set(obj) == {'offset1', 'length', 'offset2', 'data', 'value'}:  # RawCopy
            return {'value': _build(obj.value)}
        return {key: _build(val) for key, val in obj.items() if key != '_io'}
    else:
        return obj


def _clean(obj):
    if isinstance(obj, ListContainer):
        return [_clean(li) for li in obj]
    elif isinstance(obj, Container):
        if set(obj) == {'offset1', 'length', 'offset2', 'data', 'value'}:  # RawCopy
            return _clean(obj.value)
        return {key: _clean(val) for key, val in obj.items() if key not in ('_io', '_flagsenum')}
    else:
        return obj
