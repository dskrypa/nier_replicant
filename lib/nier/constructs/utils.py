"""
Utils for Nier Replicant save file constructs

:author: Doug Skrypa
"""

import math
from typing import Sequence

from construct import Int8ul, Bytes, Enum, Adapter, EnumIntegerString, BitsSwapped, BitStruct, Flag

__all__ = ['EnumIntStr', 'IntEnum', 'BitStructLE', '_struct_parts', 'BitFlagEnum', 'SparseBitFlagEnum']


def _struct_parts(sections, unknowns, struct=Int8ul):
    for i, (unknown, section) in enumerate(zip(unknowns, sections)):
        yield from (v / struct for v in section)
        if unknown:
            yield f'_unk{i}' / Bytes(unknown)


def _expanded_parts(sections, unknowns, struct):
    for group, (unknown, section) in enumerate(zip(unknowns, sections)):
        yield from (v / struct for v in section)
        if unknown:
            for i in range(unknown):
                yield f'_unk_{group}_{i}' / struct  # noqa


def BitStructLE(sections, unknowns, struct, expand: bool = False):
    if expand:
        return BitsSwapped(BitStruct(*_expanded_parts(sections, unknowns, struct)))
    else:
        return BitsSwapped(BitStruct(*_struct_parts(sections, unknowns, struct)))


def BitFlagEnum(byte_width: int, labels: Sequence[str] = (), **kw_labels):
    bits = byte_width * 8
    rev_labels = {i: val for i, val in enumerate(labels)} | {v: k for k, v in kw_labels.items()}
    return BitsSwapped(BitStruct(*(rev_labels.get(i, f'_unk_{i}') / Flag for i in range(bits))))


def SparseBitFlagEnum(byte_width: int, labels: Sequence[str], empty_fmt: str = '_unk_{}', flag_struct=Flag):
    if byte_width == 0:
        byte_width = math.ceil(len(labels) / 8)
    bits = byte_width * 8
    if len(labels) > bits:
        raise ValueError(f'{byte_width=} does not contain enough {bits=} to fit {len(labels)} labels')
    label_names = [n if n else empty_fmt.format(i) for i, n in enumerate(labels)]
    if len(labels) < bits:
        label_names.extend(empty_fmt.format(i) for i in range(len(labels), bits))
    return BitsSwapped(BitStruct(*(label / flag_struct for label in label_names)))  # noqa


class EnumIntStr(EnumIntegerString):
    def __eq__(self, other):
        if isinstance(other, (float, int)):
            return self.intvalue == other  # noqa
        return super().__eq__(other)

    def __ne__(self, other):
        if isinstance(other, (float, int)):
            return self.intvalue != other  # noqa
        return super().__ne__(other)

    def __hash__(self):
        return str.__hash__(self)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.new({self.intvalue}, {str.__repr__(self)})'  # noqa

    @classmethod
    def new(cls, intvalue, stringvalue):
        # Had to override because original is a staticmethod instead of a classmethod
        ret = cls(stringvalue)
        ret.intvalue = intvalue
        return ret


class IntEnum(Enum):  # noqa
    """Overrides encmapping & decmapping attrs to use more permissive :class:`EnumIntStr`"""
    def __init__(self, subcon, *merge, **mapping):
        Adapter.__init__(self, subcon)
        for enum in merge:
            for enumentry in enum:
                mapping[enumentry.name] = enumentry.value
        self.encmapping = {EnumIntStr.new(v, k): v for k, v in mapping.items()}
        self.decmapping = {v: EnumIntStr.new(v, k) for k, v in mapping.items()}
        self.ksymapping = {v: k for k, v in mapping.items()}
