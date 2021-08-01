"""
Structs that represent parts of NieR Replicant ver.1.22474487139... save files.

Credit for decoding most of the struct fields goes to https://github.com/Acurisu
Most constants and original structs were translated to Python from
https://github.com/Acurisu/NieR-Replicant-ver.1.22474487139/blob/main/Editor/src/Nier.ts

Newly decoded fields in this module include time (for a given save + for each garden plot) and garden plots.

:author: Doug Skrypa
"""

import logging
from datetime import datetime
from io import BytesIO
from typing import Optional

from construct import Struct, Int8ul, Int32sl, Int32ul, Float64l, Float32l, PaddedString, Bytes, Int16ul
from construct import Enum, FlagsEnum, Sequence, Adapter, BitStruct, Flag, BitsSwapped, ExprValidator, Subconstruct
from construct import ValidationError, RawCopy, singleton, Bit

from .constants import DOCUMENTS, KEY_ITEMS, MAPS, WORDS, CHARACTERS, PLANTS, FERTILIZER, SWORDS_1H, SWORDS_2H, SPEARS
from .constants import RAW_MATERIALS, RECOVERY, FERTILIZERS, SEEDS, CULTIVATED, BAIT, FISH, ABILITIES
from .constants import TUTORIALS, QUESTS, QUESTS_NEW_1

log = logging.getLogger(__name__)
__all__ = ['Savefile', 'Gamedata', 'Plot']


# region Helpers

@singleton
class DateTime(Adapter):  # noqa
    _base_struct = Struct(year=Int16ul, month=Int8ul, day=Int8ul, hour=Int8ul, minute=Int8ul, second=Int8ul)

    def __init__(self):
        super().__init__(self._base_struct)

    def _decode(self, obj, context, path) -> Optional[datetime]:
        del obj['_io']
        return datetime(**obj) if obj.year else None

    def _encode(self, obj: Optional[datetime], context, path):
        fields = (sc.name for sc in self.subcon.subcons)
        return {f: 0 for f in fields} if obj is None else {f: getattr(obj, f) for f in fields}


@singleton
class Checksum(Subconstruct):  # noqa
    def __init__(self):
        super().__init__(Int32ul)

    @classmethod
    def _get_checksum(cls, stream: BytesIO):
        pos = stream.tell()
        stream.seek(pos - Savefile.sizeof() + 16)
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
        return SPEARS[index - 40]

    def _encode(self, name: Optional[str], context, path) -> int:
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


def _struct_parts(sections, unknowns, struct=Int8ul):
    for i, (unknown, section) in enumerate(zip(unknowns, sections)):
        yield from (v / struct for v in section)
        if unknown:
            yield f'_unk{i}' / Bytes(unknown)


# endregion

# region Save Slot Fields

Character = Enum(Int32ul, **{k: i for i, k in enumerate(CHARACTERS)})
Ability = Enum(Int32ul, **{k: i for i, k in enumerate(ABILITIES)})
Tutorials = BitsSwapped(BitStruct(*((n if n else f'_tutorial_{i}') / Flag for i, n in enumerate(TUTORIALS))))
WordsLearned = BitsSwapped(BitStruct(*((n if n else f'_word_{i}') / Flag for i, n in enumerate(WORDS))))
WordEquipped = Enum(Int8ul, **({k: i for i, k in enumerate(WORDS)} | {'None': 255}))
WeaponState = Enum(Int8ul, **{'Level 1': 0, 'Level 2': 1, 'Level 3': 2, 'Level 4': 3, 'Not Owned': 255})

KeyItems = Struct(*(v / Int8ul for v in KEY_ITEMS))
Documents = Struct(*(v / Int8ul for v in DOCUMENTS))
Maps = Struct(*(v / Int8ul for v in MAPS))

Plot = Struct(
    seed=Enum(Int8ul, **({k: i for i, k in enumerate(PLANTS)} | {'None': 255})),
    _unk0=Bytes(3),
    fertilizer=Enum(Int8ul, **{k: i for i, k in enumerate(FERTILIZER)}),
    _unk1=Bytes(3),
    water=FlagsEnum(Int8ul, first=1, second=2),
    _unk2=Bytes(3),
    direction=Enum(Float32l, East=0, North=90, West=180, South=270),
    time=DateTime,
    _unk3=Bytes(1),
)
Garden = Sequence(RawCopy(Plot)[5], RawCopy(Plot)[5], RawCopy(Plot)[5])

Recovery = Struct(*_struct_parts(RECOVERY.values(), (18, 2, 1, 0)))
Cultivation = Struct(*_struct_parts((FERTILIZERS, SEEDS, CULTIVATED), (2, 5, 0)))
Fishing = Struct(*_struct_parts((BAIT, FISH), (7, 0)))
RawMaterials = Struct(*_struct_parts(RAW_MATERIALS.values(), (3, 4, 5, 4, 1, 5, 1, 3, 0)))
Weapons = Struct(*_struct_parts((SWORDS_1H, SWORDS_2H, SPEARS), (3, 10, 0), WeaponState))  # noqa
WeaponWords = Struct(*_struct_parts((SWORDS_1H, SWORDS_2H, SPEARS), (3, 10, 0), WordEquipped))  # noqa
AbilityWords = Struct(*(a / WordEquipped for a in ABILITIES[1:]))

# endregion


Savefile = Struct(
    corruptness=ExprValidator(Int32ul, lambda val, ctx: val == 200),
    map=PaddedString(32, 'utf-8'),
    spawn=Int32ul,
    character=Character,
    name=PaddedString(32, 'utf-8'),
    health=Int32sl, health_kaine=Int32sl, health_emil=Int32sl,
    magic=Float32l, magic_kaine=Float32l, magic_emil=Float32l,
    level=Int32sl,  # Level index, not actual integer level - add one for level displayed in-game
    level_kaine=Int32sl, level_emil=Int32sl,  # _unk3=Bytes(8),  # Unconfirmed, but they seem to match Nier's
    xp=Int32sl,
    _unk4=Bytes(12),
    order_kaine=Int32ul, order_emil=Int32ul,
    active_weapon=Weapon, selected_sword_1h=Weapon, selected_sword_2h=Weapon, selected_spear=Weapon,
    _unk5=Bytes(8),
    left_bumper=Ability, right_bumper=Ability, left_trigger=Ability, right_trigger=Ability,
    _unk6=Bytes(12),
    money=Int32sl,
    recovery=Recovery,
    _unk7=Bytes(7),  # zeros
    cultivation=Cultivation,
    _unk8=Bytes(10),  # zeros
    fishing=Fishing,
    _unk9=Bytes(5),  # zeros
    raw_materials=RawMaterials,
    key_items=KeyItems,
    _unk10=Bytes(176),  # zeros
    documents=Documents,
    _unk11=Bytes(168),  # zeros
    maps=Maps,
    _unk12=Bytes(264),  # :40=zeros; 40:84=content; 84:104=zeros; 104:108=content; 108:128=zeros; 128:=mostly 0xFF
    total_play_time=Float64l,
    _unk13=Bytes(4),  # zeros
    weapons=Weapons,
    _unk14=Bytes(225),
    quests=Quests(512, QUESTS),
    _unk15=Bytes(312),
    words=WordsLearned,
    _unk16a=Bytes(16),
    ability_words_a=AbilityWords,
    weapon_words_a=WeaponWords,
    _unk16b=Bytes(13),
    ability_words_b=AbilityWords,
    weapon_words_b=WeaponWords,
    _unk16c=Bytes(17),
    tutorials=Tutorials,  # 12
    _unk17a=Bytes(412),
    garden=Garden,  # 360
    _unk17b=Bytes(332),
    quests_b=Quests(32, QUESTS_NEW_1),
    _unk18a1=Bytes(240),
    _unk18a2=Bytes(240),  # zeros
    _unk18a3=Bytes(40),
    _unk18a4=Bytes(720),  # zeros
    _unk18a5=Bytes(86),
    save_time=DateTime,
    _unk18b1=Bytes(200),
    _unk18b2=Bytes(32771),  # zeros
    checksum=Checksum,
    _unk19=Bytes(12),  # zeros
)

"""
Change: Tutorial "Weapon Quick Switching" New -> viewed
@@ -1,7 +1,7 @@ _unk17a
  0x008: c100012e  |  �...  |  b'\xc1\x00\x01.'
- 0x00C: d833f6ff  |  �3��  |  b'\xd83\xf6\xff'
+ 0x00C: d813f6ff  |  �.��  |  b'\xd8\x13\xf6\xff'
  0x010: ffffffff  |  ����  |  b'\xff\xff\xff\xff'
"""

Gamedata = Struct(_unk=Bytes(33120), slots=RawCopy(Savefile)[3], _unk2=Bytes(149888))
