"""
Structs that represent parts of NieR Replicant ver.1.22474487139... save files.

:author: Doug Skrypa
"""

from construct import Struct, Int8ul, Int32sl, Int32ul, Float64l, Float32l, PaddedString, Bytes
from construct import Enum, FlagsEnum, Sequence, BitStruct, Flag, BitsSwapped, ExprValidator, RawCopy

from ..constants import DOCUMENTS, KEY_ITEMS, MAPS, WORDS, CHARACTERS, PLANTS, FERTILIZER, SWORDS_1H, SWORDS_2H, SPEARS
from ..constants import RAW_MATERIALS, RECOVERY, FERTILIZERS, SEEDS, CULTIVATED, BAIT, FISH, ABILITIES
from ..constants import TUTORIALS, QUESTS, QUESTS_NEW_1, QUESTS_VIEWED, FISH_RECORDS
from .adapters import DateTime, Checksum, Weapon, Quests
from .utils import IntEnum, BitStructLE, BitFlagEnum, SparseBitFlagEnum, _struct_parts


Character = Enum(Int32ul, **{k: i for i, k in enumerate(CHARACTERS)})
Tutorials = SparseBitFlagEnum(0, TUTORIALS, '_tutorial_{}')

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

WordsLearned = SparseBitFlagEnum(0, WORDS, '_word_{}')

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

QuestViewedStates = SparseBitFlagEnum(11, QUESTS_VIEWED, flag_struct=ViewStateBit)  # 11
KeyItemViewedStates = SparseBitFlagEnum(10, KEY_ITEMS, flag_struct=ViewStateBit)  # 10
# MapViewedStates = BitStructLE(([], MAPS), (1, 7), ViewStateBit)  # 4
# MapViewedStates = BitStructLE(([], KEY_ITEM_MAPS), (1, 6), ViewStateBit)  # 3

RecoveryViewedStates = BitStructLE(RECOVERY.values(), (18, 2, 1, 6), ViewStateBit)  # 5
CultivationViewedStates = BitStructLE(([], FERTILIZERS, SEEDS, CULTIVATED), (1, 2, 5, 5), ViewStateBit)  # 7
FishingViewedStates = BitStructLE(([], BAIT, FISH), (5, 7, 2), ViewStateBit)  # 4
RawMaterialsViewedStates = BitStructLE(([], *RAW_MATERIALS.values()), (3, 3, 4, 5, 4, 1, 5, 1, 3, 0), ViewStateBit)  # 16
# endregion

# region Save File
Savefile = Struct(
    # region Character Info
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
    # endregion

    recovery=Recovery,              # 34
    _unk7=Bytes(7),                 # zeros
    cultivation=Cultivation,        # 50
    _unk8=Bytes(10),                # zeros
    fishing=Fishing,                # 25
    _unk9=Bytes(5),                 # zeros
    raw_materials=RawMaterials,     # 125
    key_items=KeyItems,             # 80
    _unk10=Bytes(176),              # zeros
    documents=Documents,            # 24
    _unk11=Bytes(168),              # zeros
    maps=Maps,                      # 24

    _unk12a1=Bytes(40),
    _unk12a2=Bytes(32),
    _unk12a3=Bytes(32),
    _unk12a4=Bytes(32),

    recovery_viewed_states=RecoveryViewedStates,  # 5
    cultivation_viewed_states=CultivationViewedStates,  # 7
    fishing_viewed_states=FishingViewedStates,  # 4
    raw_materials_viewed_states=RawMaterialsViewedStates,  # 16
    key_item_viewed_states=KeyItemViewedStates,  # 10
    _unk12b=Bytes(86),

    # _unk12b1=Bytes(48),
    # map_viewed_states=MapViewedStates,
    # _unk12b2=Bytes(35),
    # _unk12a + ...
    # 0x0A8: ff -> fe on moon key viewed (key item)
    # 0x0E2 (226): c7 -> c5 on shadowlord's castle map viewed

    total_play_time=Float64l,
    _unk13=Bytes(4),  # zeros
    weapons=Weapons,  # 51
    _unk14a=Bytes(1),
    _maybe_weapon_viewed_states=Bytes(32),  # 0x1b: 8e -> 0e after viewing Labyrinth's Song (new->viewed)

    _unk14b=Bytes(23),  # likely related to main story mission progress
    _unk14c=Bytes(137),  # zeros in new game; content in old game
    _unk14d=Bytes(32),  # likely related to main story mission progress

    quests=Quests(512, QUESTS),

    # _unk15a1=Bytes(256),  # zeros in new game; content in old game
    _unk15a1a1=Bytes(100),
    _unk15a1a2=Bytes(100),

    sheep_kill_count=Int8ul,  # May be larger byte width
    _unk15a1b=Bytes(55),

    # _maybe_mission_objective=Bytes(4),
    _maybe_mission_objective=Int32ul,
    _unk15a2b=Bytes(20),

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

    # _unk17a1=Bytes(68),  # Seems to contain Tutorial new/viewed
    # 0x00D: 33 -> 13 on Tutorial "Weapon Quick Switching" New -> viewed
    _unk17a1a=Bytes(4),  # zeros
    _maybe_tutorial_viewed_states=Bytes(16),
    _unk17a1b=Bytes(48),

    fishing_record_sizes=FishRecordSizesCm,  # 120; value / 2.54 => inches
    _unk17a2=Bytes(72),
    fishing_record_weights=FishRecordWeightsG,  # 120; value * .00220462 => lbs
    _unk17a3=Bytes(32),
    garden=Garden,  # 360
    _unk17b1a=Bytes(168),
    _unk17b1b=Bytes(21),
    fishing_record_states=FishRecordStates,  # 15
    _unk17b2a=Bytes(99),  # Last block in checksum; zeros
    _unk17b2b=Bytes(29),  # Outside of checksum; content
    quests_b=Quests(32, QUESTS_NEW_1),

    # _unk18a1=Bytes(240),  # May contain main story mission progress?
    # 0xE5:0xE6 seem to change after fighting shades, but also with mission progress...
    _unk18a1a=Bytes(96),
    _unk18a1b=Bytes(136),
    _unk18a1c=Bytes(8),
    _unk18a2=Bytes(240),  # zeros
    _unk18a3=Bytes(40),
    _unk18a4a=Bytes(68),  # zeros
    _unk18a4b=Bytes(4),  # Content during Kaine play; maybe bit flags
    _unk18a4c=Bytes(616),  # zeros
    _unk18a4d=Bytes(32),  # Content during Kaine play; maybe bit flags
    _unk18a5=Bytes(86),
    save_time=DateTime,  # 7
    _unk18b0=Int8ul,  # Seems to increment by 1 when saving the next day; may be uint16; can't be int32
    _unk18b1=Bytes(199),
    _unk18b2=Bytes(32771),  # zeros
    checksum=Checksum(37456, 3104),  # 4
    _end=Bytes(12),  # zeros
)
# endregion

# region Header
# Header size: 33,120
Header = Struct(
    _unk1=Bytes(4),                     # 1st byte is always 0x6E (110; ascii: 'n'), the rest are 0s
    endings=BitFlagEnum(4, 'ABCDE'),
    d_name=PaddedString(32, 'utf-8'),   # The name deleted during ending D; cannot re-use for new game afterwards
    _unk3=Bytes(16),                    # Changes between young->old and no ending -> ending
    _unk4=Bytes(24),                    # zeros
    # _unk5=Bytes(344),                   # Changes between endings; maybe between main story missions?
    _unk5a=Bytes(28),
    _unk5b=Bytes(24),
    _unk5c=Bytes(28),
    _unk5d=Bytes(84),
    _unk5e=Bytes(48),
    _unk5f=Bytes(128),
    _unk5g=Bytes(4),
    _unk6=Bytes(32684),                 # zeros
    checksum=Checksum(33108, 424),      # The read count may not be correct; 424 = stop before large block of zeros
    _end=Bytes(8),                      # zeros
)
# endregion

# I suspect the ending D "deletion" of saves just moves them into a slot outside of the initial array of 3
Gamedata = Struct(header=RawCopy(Header), slots=RawCopy(Savefile)[7])

# Savefile.sizeof() => 37,472
# * 3 = 112,416
# * 4 = 149,888

# Initially upon completing ending D, the most recently used save slot is copied to slot 7 (index 6); 4-6 are unused.
# Slots 1-3 are not actually wiped out, but header.d_name seems to tell the game to prevent those from being offered as
# an option to load.

# Slot indices 0-2: NieR
# Slot indices 3-5: Kaine
# Slot index 6: Saved ending D NieR

# The endings badges on save slots may be stored in header, not the save slot
