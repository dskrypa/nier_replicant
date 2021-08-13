"""
Construct adapters / sub-constructs for Nier Replicant save files.

:author: Doug Skrypa
"""

import logging
from datetime import datetime
from io import BytesIO
from typing import Optional, Union

from construct import Struct, Adapter, BitStruct, Flag, BitsSwapped, Subconstruct, ValidationError, singleton, Bit
from construct import Int8ul, Int32ul, Int16ul

from ..constants import SWORDS_1H, SWORDS_2H, SPEARS

log = logging.getLogger(__name__)
__all__ = ['DateTime', 'Checksum', 'Weapon', 'Quests']


@singleton
class DateTime(Adapter):  # noqa
    _base_struct = Struct(year=Int16ul, month=Int8ul, day=Int8ul, hour=Int8ul, minute=Int8ul, second=Int8ul)

    def __init__(self):
        super().__init__(self._base_struct)

    def _decode(self, obj, context, path) -> Union[datetime, None, dict[str, int]]:
        del obj['_io']
        try:
            return datetime(**obj) if obj.year else None
        except ValueError:
            return dict(obj)

    def _encode(self, obj: Union[datetime, None, dict[str, int]], context, path):
        if isinstance(obj, dict):
            return obj
        fields = (sc.name for sc in self.subcon.subcons)
        return {f: 0 for f in fields} if obj is None else {f: getattr(obj, f) for f in fields}


@singleton
class Checksum(Subconstruct):  # noqa
    def __init__(self):
        super().__init__(Int32ul)

    @classmethod
    def _get_checksum(cls, stream: BytesIO):
        pos = stream.tell()
        stream.seek(pos - 37472 + 16)  # Savefile.sizeof() => 37472
        checksum = sum(stream.read(3104))
        stream.seek(pos)
        return checksum

    def _parse(self, stream, context, path):
        checksum = self._get_checksum(stream)
        parsed = self.subcon._parsereport(stream, context, path)
        if parsed != checksum:
            raise ValidationError(f'Incorrect stored checksum={parsed} - calculated={checksum}')
        return parsed

    def _build(self, checksum, stream, context, path):
        return self.subcon._build(self._get_checksum(stream), stream, context, path)


@singleton
class Weapon(Adapter):  # noqa
    def __init__(self):
        super().__init__(Int32ul)

    def _decode(self, index: int, context, path) -> Optional[str]:
        if index < 20:
            return SWORDS_1H[index]
        elif index < 40:
            return SWORDS_2H[index - 20]
        try:
            return SPEARS[index - 40]
        except IndexError:
            if index == (1 << 32) - 1:
                return None
            else:
                log.error(f'Error decoding weapon with {index=} @ {path=}')
                raise

    def _encode(self, name: Optional[str], context, path) -> int:
        if name is None:
            return (1 << 32) - 1
        try:
            return SWORDS_1H.index(name)
        except ValueError:
            pass
        try:
            return SWORDS_2H.index(name) + 20
        except ValueError:
            pass
        return SPEARS.index(name) + 40


class Quests(Adapter):  # noqa
    def __init__(self, bits: int, quest_map: dict[str, tuple[int, int]]):
        super().__init__(self._prepare_struct(bits, quest_map))

    @classmethod
    def _prepare_struct(cls, bits: int, quest_map: dict[str, tuple[int, int]]):
        fields = []
        last = -1
        for i, (name, (start, end)) in enumerate(quest_map.items()):
            if pad := start - last - 1:
                fields.append(f'_unk_{i}' / Bit[pad])  # noqa

            if mid := end - start - 1:
                fields.append(name / Struct(started=Flag, _unk=Bit[mid], done=Flag))
            else:
                fields.append(name / Struct(started=Flag, done=Flag))
            last = end

        if remainder := bits - last - 1:
            fields.append(f'_unk_{len(quest_map)}' / Bit[remainder])  # noqa

        return BitsSwapped(BitStruct(*fields))

    def _decode(self, obj, context, path):
        try:
            a = obj.pop('Thieves in Training (1)')
        except KeyError:
            pass
        else:
            b = obj.pop('Thieves in Training (2)')
            obj['Thieves in Training'] = {
                'started': a['started'], '_unk': a['_unk'], '_a': a['done'], '_b': b['started'], 'done': b['done']
            }
        return obj

    def _encode(self, obj, context, path):
        try:
            quest = obj.pop('Thieves in Training')
        except KeyError:
            pass
        else:
            obj['Thieves in Training (1)'] = {'started': quest['started'], '_unk': quest['_unk'], 'done': quest['_a']}
            obj['Thieves in Training (2)'] = {'started': quest['_b'], 'done': quest['done']}
        return obj
