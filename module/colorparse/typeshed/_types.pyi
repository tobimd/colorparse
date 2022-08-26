from typing import Union, overload
from ._datatypes import *
from _typeshed import Incomplete

class Container(_Object):
    @overload
    def get(self, *, by_label: str = ...) -> None: ...
    @overload
    def get(self, *, by_code: str = ...) -> None: ...
    @overload
    def get(self, *, by_attribute_name: str = ...) -> None: ...

class OptionContainer(_Object): ...

class PrintContainer(OptionContainer):
    overflow: bool
    sep: str
    end: str
    file: SupportsWrite
    flush: bool
    def __init__(self) -> None: ...

class PaintContainer(OptionContainer):
    overflow: bool
    sep: str
    end: str
    def __init__(self) -> None: ...

class FlagContainer(OptionContainer):
    ignore_special: bool
    always_finish_colors: bool
    true_color: bool
    ignore_idle_use_warning: bool
    def __init__(self) -> None: ...

class Command(_Object):
    group: _ReadOnly
    variant: _ReadOnly
    label: _ReadOnly
    code: _ReadOnly
    def __init__(
        self,
        group: Union[COLOR, STYLE],
        variant: Union[VAR_0, VAR_1],
        label: str,
        code: str,
    ) -> None: ...
    def __str__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...
    def __add__(self, other) -> "Command": ...
