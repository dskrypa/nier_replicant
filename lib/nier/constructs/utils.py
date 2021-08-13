"""
Utils for Nier Replicant save file constructs

:author: Doug Skrypa
"""

from construct import Int8ul, Bytes, Enum, Adapter, EnumIntegerString

__all__ = ['EnumIntStr', 'IntEnum', '_struct_parts']


def _struct_parts(sections, unknowns, struct=Int8ul):
    for i, (unknown, section) in enumerate(zip(unknowns, sections)):
        yield from (v / struct for v in section)
        if unknown:
            yield f'_unk{i}' / Bytes(unknown)


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
