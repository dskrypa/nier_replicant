"""
Structs that represent parts of NieR Replicant ver.1.22474487139... save files.

:author: Doug Skrypa
"""

from construct import Struct, Int8ul, Int32sl, Int32ul, Float64l, Float32l, PaddedString, Bytes
from construct import Enum, FlagsEnum, Sequence, BitStruct, Flag, BitsSwapped, ExprValidator, RawCopy

from ..constants import DOCUMENTS, KEY_ITEMS, MAPS, WORDS, CHARACTERS, PLANTS, FERTILIZER, SWORDS_1H, SWORDS_2H, SPEARS
from ..constants import RAW_MATERIALS, RECOVERY, FERTILIZERS, SEEDS, CULTIVATED, BAIT, FISH, ABILITIES
from ..constants import TUTORIALS, QUESTS, QUESTS_NEW_1, QUEST_NEW_MARKERS, FISH_RECORDS
from .adapters import DateTime, Checksum, Weapon, Quests
from .utils import IntEnum, _struct_parts

__all__ = ['Savefile', 'Gamedata', 'Plot']

Character = Enum(Int32ul, **{k: i for i, k in enumerate(CHARACTERS)})
Tutorials = BitsSwapped(BitStruct(*((n if n else f'_tutorial_{i}') / Flag for i, n in enumerate(TUTORIALS))))

# region Garden
Plot = Struct(
    seed=IntEnum(Int32ul, **({k: i for i, k in enumerate(PLANTS)} | {'None': 255})),
    fertilizer=IntEnum(Int32ul, **{k: i for i, k in enumerate(FERTILIZER)}),
    water=FlagsEnum(Int32ul, first=1, second=2),
    direction=IntEnum(Float32l, East=0, North=90, West=180, South=270),
    time=DateTime,  # 7
    _pad=Bytes(1),
)
Garden = Sequence(RawCopy(Plot)[5], RawCopy(Plot)[5], RawCopy(Plot)[5])
# endregion

# region Inventory
Recovery = Struct(*_struct_parts(RECOVERY.values(), (18, 2, 1, 0)))
Cultivation = Struct(*_struct_parts((FERTILIZERS, SEEDS, CULTIVATED), (2, 5, 0)))
Fishing = Struct(*_struct_parts((BAIT, FISH), (7, 0)))
RawMaterials = Struct(*_struct_parts(RAW_MATERIALS.values(), (3, 4, 5, 4, 1, 5, 1, 3, 0)))

KeyItems = Struct(*(v / Int8ul for v in KEY_ITEMS))
Documents = Struct(*(v / Int8ul for v in DOCUMENTS))
Maps = Struct(*(v / Int8ul for v in MAPS))
# endregion

# region Weapons, Abilities, Words
Ability = Enum(Int32ul, **{k: i for i, k in enumerate(ABILITIES)})
WeaponState = Enum(Int8ul, **{'Level 1': 0, 'Level 2': 1, 'Level 3': 2, 'Level 4': 3, 'Not Owned': 255})
WordEquipped = Enum(Int8ul, **({k: i for i, k in enumerate(WORDS)} | {'None': 255}))

WordsLearned = BitsSwapped(BitStruct(*((n if n else f'_word_{i}') / Flag for i, n in enumerate(WORDS))))

Weapons = Struct(*_struct_parts((SWORDS_1H, SWORDS_2H, SPEARS), (3, 10, 0), WeaponState))  # noqa
WeaponWords = Struct(*_struct_parts((SWORDS_1H, SWORDS_2H, SPEARS), (3, 10, 0), WordEquipped))  # noqa
AbilityWords = Struct(*(a / WordEquipped for a in ABILITIES[1:]))
# endregion

# region Fishing Records
FishRecordState = Enum(Int8ul, new=1, viewed=0)
FishRecordStates = Struct(*(f / FishRecordState for f in FISH_RECORDS))
FishRecordSizesCm = Struct(*(f / Float64l for f in FISH_RECORDS))
FishRecordWeightsG = Struct(*(f / Float64l for f in FISH_RECORDS))
# endregion

# region New / Viewed
ViewStateBit = Enum(Flag, new=True, viewed=False)

QuestViewedStates = BitStruct(*((n if n else f'_quest_{i}') / ViewStateBit for i, n in enumerate(QUEST_NEW_MARKERS)))
# endregion

# region Save File
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

    recovery=Recovery,  # 34
    _unk7=Bytes(7),  # zeros

    cultivation=Cultivation,  # 50
    _unk8=Bytes(10),  # zeros

    fishing=Fishing,  # 25
    _unk9=Bytes(5),  # zeros

    raw_materials=RawMaterials,  # 125
    key_items=KeyItems,  # 80
    _unk10=Bytes(176),  # zeros

    documents=Documents,  # 24
    _unk11=Bytes(168),  # zeros

    maps=Maps,  # 24

    _unk12=Bytes(264),  # :40=zeros; 40:84=content; 84:104=zeros; 104:108=content; 108:128=zeros; 128:=mostly 0xFF

    # _unk12a=Bytes(137),
    # _unk12z=Bytes(38),


    # 0x08A (138): df -> 9f on recovery item new->viewed (strength capsule) [1 << 6]
    # 0x08A: 9f -> 1f on recovery item new->viewed (magic drop) [1 << 7]

    # 0x08B: 7f -> 6f on spirit capsule viewed [1 << 4]

    # 0x08D: ff -> fd on speed fertilizer viewed

    # 0x092: ff -> f7 on freesia viewed (1<<3)
    # 0x092: f7 -> e7 on red moonflower viewed (1<<4)

    # 0x093: ff -> fb on white moonflower viewed

    # 0x094: ff -> df on lugworm viewed
    # 0x096: df -> cf on blue marlin viewed

    # 0x098: ef -> e7 on aquatic plant viewed
    # 0x0A7: ff -> 7f on deer antler viewed

    # 0x0A8: ff -> fe on moon key viewed (key item)
    # 0x0E2 (226): c7 -> c5 on shadowlord's castle map viewed

    total_play_time=Float64l,
    _unk13=Bytes(4),  # zeros
    weapons=Weapons,  # 51

    _unk14=Bytes(225),  # Definitely contains something related to main story mission progress
    # 0x1b: 8e -> 0e after viewing Labyrinth's Song (new->viewed)

    quests=Quests(512, QUESTS),
    _unk15a=Bytes(280),  # Definitely contains something related to main story mission progress
    quest_viewed_states=QuestViewedStates,  # 11
    _unk15b=Bytes(21),
    words=WordsLearned,  # 16
    _unk16a=Bytes(16),
    ability_words_a=AbilityWords,  # 10
    weapon_words_a=WeaponWords,  # 51
    _unk16b=Bytes(13),
    ability_words_b=AbilityWords,  # 10
    weapon_words_b=WeaponWords,  # 51
    _unk16c=Bytes(17),
    tutorials=Tutorials,  # 12  # Whether a given tutorial has been unlocked

    _unk17a1=Bytes(68),  # Seems to contain Tutorial new/viewed
    # 0x00D: 33 -> 13 on Tutorial "Weapon Quick Switching" New -> viewed

    fishing_record_sizes=FishRecordSizesCm,  # 120; value / 2.54 => inches
    _unk17a2=Bytes(72),
    fishing_record_weights=FishRecordWeightsG,  # 120; value * .00220462 => lbs
    _unk17a3=Bytes(32),
    garden=Garden,  # 360
    _unk17b1=Bytes(189),
    fishing_record_states=FishRecordStates,  # 15
    _unk17b2=Bytes(128),
    quests_b=Quests(32, QUESTS_NEW_1),

    _unk18a1=Bytes(240),  # May contain main story mission progress?
    # 0xE5:0xE6 seem to change after fighting shades, but also with mission progress...

    _unk18a2=Bytes(240),  # zeros
    _unk18a3=Bytes(40),
    _unk18a4=Bytes(720),  # zeros
    _unk18a5=Bytes(86),
    save_time=DateTime,  # 7
    _unk18b1=Bytes(200),  # Something here changes when saving on a different day
    _unk18b2=Bytes(32771),  # zeros
    checksum=Checksum,  # 4
    _unk19=Bytes(12),  # zeros
)
# endregion

Header = Struct(
    _unk=Bytes(33120),
)

# I suspect the ending D "deletion" of saves just moves them into a slot outside of the initial array of 3
# Gamedata = Struct(_unk=Bytes(33120), slots=RawCopy(Savefile)[7])
Gamedata = Struct(header=RawCopy(Header), slots=RawCopy(Savefile)[7])

# Savefile.sizeof() => 37472
# * 3 = 112416
# * 4 = 149888
