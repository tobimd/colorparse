from enum import Enum, auto
from typing import Literal, Protocol, TypeVar

# fmt: off
_T_contra = TypeVar("_T_contra", contravariant=True)
_T = TypeVar("_T")
__all__ = ["_T", "SupportsWrite", "_Object", "callable_property", "GroupType", "VariantType", "COLOR", "STYLE", "VAR_0", "VAR_1", "FOREGROUND", "FG", "BACKGROUND", "BG", "START", "STOP"]


class SupportsWrite(Protocol[_T_contra]):
    def write(self, __s: _T_contra): ...  


class _Object:
    def _typename(self) -> str:
        return str(self.__class__)[8 : - 2]

    def _kwdata(self) -> list[str]:
        return [ f"{k}={ascii(getattr(self, k))}" for k in dir(self) if not k.startswith("_") ]

    @classmethod
    def _typenameof(cls, obj: object) -> str:
        return str(obj.__class__)[8 : - 2]

    @classmethod
    def _kwdataof(self, obj: object) -> list[str]:
        return [ f"{k}={ascii(getattr(obj, k))}" for k in dir(obj) if not k.startswith("_") ]

    def __repr__(self) -> str:
        return f"<{self._typename()} {' '.join(self._kwdata())}>"
# fmt: on


class callable_property(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

        super().__init__(fget, fset, fdel, doc)

    def __get__(self, instance, owner, /):
        value = super().__get__(instance, owner)
        if len(value) > 1:
            return value[0](*(value[1:]))
        return value[0]()

    def __set__(self, instance, value, /):
        raise AttributeError("can't set attribute")


# fmt: off
class GroupType(Enum):
    COLOR = auto()
    STYLE = auto()
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

COLOR:Literal[GroupType.COLOR]= GroupType.COLOR
"""Command's group is of type COLOR."""
STYLE:Literal[GroupType.STYLE]= GroupType.STYLE
"""Command's group is of type STYLE."""


class VariantType(Enum):
    VAR_0 = auto()
    VAR_1 = auto()
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

VAR_0:Literal[VariantType.VAR_0]= VariantType.VAR_0
"""Command's variant is of type 0."""
FOREGROUND:Literal[VariantType.VAR_0]= VAR_0
"""Command's variant is of type 0. Equal to START variant."""
FG:Literal[VariantType.VAR_0]= VAR_0
"""Command's variant is of type 0. Shorthand for FOREGROUND variant."""
START:Literal[VariantType.VAR_0]= VAR_0
"""Command's variant is of type 0. Equal to FOREGROUND variant."""

VAR_1:Literal[VariantType.VAR_1]= VariantType.VAR_1
"""Command's variant is of type 1."""
BACKGROUND:Literal[VariantType.VAR_1]= VAR_1
"""Command's variant is of type 1. Equal to STOP variant."""
BG:Literal[VariantType.VAR_1]= VAR_1
"""Command's variant is of type 1. Shorthand for BACKGROUND variant."""
STOP:Literal[VariantType.VAR_1]= VAR_1
"""Command's variant is of type 1. Equal to BACKGROUND variant."""

# fmt: on
