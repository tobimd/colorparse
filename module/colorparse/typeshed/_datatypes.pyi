from _typeshed import Incomplete
from email.headerregistry import Group
from enum import Enum
from typing import Literal, Protocol, TypeVar
from weakref import WeakKeyDictionary

# fmt: off
_T_contra = TypeVar('_T_contra', contravariant=True)
_T = TypeVar('_T')
__all__ = ["_T", "SupportsWrite", "_Object", "_ReadOnly", "GroupType", "VariantType", "COLOR", "STYLE", "VAR_0", "VAR_1", "FOREGROUND", "FG", "START", "BACKGROUND", "BG", "STOP"]

class SupportsWrite(Protocol[_T_contra]):
    def write(self, __s: _T_contra): ...

class _Object:
    def _typename(self) -> str: ...
    def _kwdata(self) -> list[str]: ...
    @classmethod
    def _typename(cls, obj: object) -> str: ...
    @classmethod
    def _kwdata(self, obj: object) -> list[str]: ...
    def __repr__(self) -> str: ...

class _ReadOnly:
    weakrefs: WeakKeyDictionary
    def __init__(self) -> None: ...
    def __get__(self, ins, own = ...) -> _T: ...
    def __set__(self, ins, value:_T) -> None: ...

class GroupType(Enum):
    COLOR: Incomplete
    STYLE: Incomplete

COLOR: Literal[GroupType.COLOR]
STYLE: Literal[GroupType.STYLE]

class VariantType(Enum):
    VAR_0: Incomplete
    VAR_1: Incomplete

VAR_0: Literal[VariantType.VAR_0]
FOREGROUND: Literal[VariantType.VAR_0]
FG: Literal[VariantType.VAR_0]
START: Literal[VariantType.VAR_0]
VAR_1: Literal[VariantType.VAR_1]
BACKGROUND: Literal[VariantType.VAR_1]
BG: Literal[VariantType.VAR_1]
STOP: Literal[VariantType.VAR_1]
# fmt: on
