import re
import sys
from ._datatypes import *
from ._constants import *
from ._util import _readonly_attrs
from ._internal import _redo_command_regex

__all__ = ["Command", "Container", "OptionContainer", "PrintContainer", "PaintContainer", "FlagContainer", "_commands", "_command_map", "colors", "styles", "foreground", "background", "start", "stop"]  # fmt: skip


class Command(_Object):
    ...


class Container(_Object):
    """Base container class."""

    def add(self, command: Command, attribute_name: str = ...):
        ...

    def remove(self, command: Command):
        ...

    def register(self, value: str, code: str, name: str = ...):
        # fmt: off

        # Check argument types (must be str)
        _name = name if name not in [..., None] else ""
        if [type(value), type(code), type(_name)] != [str, str, str]:
            _tn = _Object._typenameof

            if type(value) != str:
                raise TypeError(f"expected argument 'value' to be str, not {_tn(value)}")            
            if type(code) != str:
                raise TypeError(f"expected argument 'code' to be str, not {_tn(code)}")            
            if type(_name) != str:
                raise TypeError(f"expected argument 'name' to be str, not {_tn(_name)}")            

        variantchars = [";", ":", "+", "-"]
        variant0chars = [";", "+"]
        color_groupchars = [";", ":"]

        # Check if value argument is valid: starts with ; : + or - &&  len(value) > 1
        if value[0] not in variantchars or len(value) < 2:
            raise ValueError("'value' argument must be a valid command.")

        # Check if label & name are valid
        if re.match(_PAT_ACCEPTED_NAME_CHARS, value[1:]) is None:
            raise ValueError("command labels must only include alphanumeric characters (including underscore) and can't start with a number")

        if name not in [..., None] and re.match(_PAT_ACCEPTED_NAME_CHARS, name) is None:
            raise ValueError("attribute names must only include alphanumeric characters (including underscore) and can't start with a number")
        # fmt: on

        cmd_group = COLOR if value[0] in color_groupchars else STYLE
        cmd_variant = VAR_0 if value[0] in variant0chars else VAR_1
        cmd_label = value[1:]

        # Remove mapping if name exists for other command
        if name in _command_map[cmd_group][cmd_variant].values():
            labelkey = _commands[cmd_group][cmd_variant][name].label

            _command_map[cmd_group][cmd_variant].pop(labelkey)
            _commands[cmd_group][cmd_variant].pop(name)

        # Add new command to data dictionaries
        _command_map[cmd_group][cmd_variant][cmd_label] = name
        _commands[cmd_group][cmd_variant][name] = Command(
            cmd_group, cmd_variant, cmd_label, code
        )

        # Redo global regex
        _redo_command_regex()


class OptionContainer(_Object):
    """Base option class for configurations."""


class PrintContainer(OptionContainer):
    """Contains options/default values for function 'print'.

    Attributes
    ----------
    - overflow : (``bool``)
        When True, allow unfinished commands to overflow onto
        other strings or values. Defaults to False.

    - sep : (``str``)
        Inserted between each ``value``. Defaults to ' '.

    - end : (``str``)
        Added after the last ``value``. Defaults to 'ESC[0m\\n'.

    - file : (``SupportsWrite[str]``)
        A file-like object (stream). Defaults to sys.stdout.

    - flush : (``bool``)
        Whether to forcibly flush the stream or not. Defaults to
        False.

    """

    def __init__(self):
        self.overflow = False
        self.sep = " "
        self.end = "\033[0m\n"
        self.file = sys.stdout
        self.flush = False


class PaintContainer(OptionContainer):
    """Contains options/default values for function 'paint'.

    Attributes
    ----------
    - overflow : (``bool``)
        When True, allow unfinished commands to overflow onto
        other strings or values. Defaults to False.

    - sep : (``str``)
        Inserted between each ``value``. Defaults to ' '.

    """

    def __init__(self) -> None:
        self.overflow = False
        self.sep = " "
        self.end = "\033[0m"


class FlagContainer(OptionContainer):
    """Contains options/default values for flags in general.

    Attributes
    ----------
    - ignore_special : (``bool``)
        Un-escape special characters. Defaults to False.

    - always_finish_colors : (``bool``)
        Prevent commands from escaping program bounds or
        terminal. Defaults to True.

    - true_color : (``bool``)
        Use of RGB values for the ANSI escape sequences. Allows
        customized color commands and a more accurate color set.
        Defaults to False.

    - ignore_idle_use_warning : (``bool``)
        Print a warning when this module is used inside a Python
        IDLE environment (colors and styles don't work). Defaults
        to False.

    """

    def __init__(self) -> None:
        self.ignore_special = False
        self.always_finish_colors = True
        self.true_color = False
        self.ignore_idle_use_warning = False


class Command(_Object):
    def __init__(self, group: GroupType, variant: VariantType, label: str, code: str):
        self._group = group
        self._variant = variant
        self._label = label
        self._code = code

    @property
    def group(self):
        return self._group

    @property
    def variant(self):
        return self._variant

    @property
    def label(self):
        return self._label

    @property
    def code(self):
        return self._code

    def __str__(self) -> str:
        return self._code

    def __hash__(self) -> int:
        return hash(self._group, self._variant, self._label, self._code)

    def __eq__(self, other) -> bool:
        return (
            (self._group == other.group and self._variant == other.variant and self._label == other.label and self._code == other.code)  # fmt: skip
            if isinstance(other, Command)
            else False
        )

    def __add__(self, other):
        if isinstance(other, Command):
            return Command(None, None, None, self._code + other.code)
        elif type(other) is str:
            return Command(None, None, None, self._code + other)
        else:
            raise TypeError(f"unsupported operant type(s) for +: '{self._typename()}' and '{_Object._typenameof(other)}'")  # fmt: skip


# fmt: off
_commands = {
    COLOR: {
        VAR_0: {
            "DARK_RED": Command(COLOR, FG, "rr", "\033[38;5;88m"),
            "DARK_ORANGE": Command(COLOR, FG, "oo", "\033[38;5;130m"),
            "DARK_YELLOW": Command(COLOR, FG, "yy", "\033[38;5;142m"),
            "DARK_GREEN": Command(COLOR, FG, "gg", "\033[38;5;22m"),
            "DARK_CYAN": Command(COLOR, FG, "cc", "\033[38;5;31m"),
            "DARK_BLUE": Command(COLOR, FG, "bb", "\033[38;5;24m"),
            "DARK_PURPLE": Command(COLOR, FG, "pp", "\033[38;5;54m"),
            "DARK_MAGENTA": Command(COLOR, FG, "mm", "\033[38;5;90m"),
            "RED": Command(COLOR, FG, "r", "\033[38;5;124m"),
            "ORANGE": Command(COLOR, FG, "o", "\033[38;5;166m"),
            "YELLOW": Command(COLOR, FG, "y", "\033[38;5;184m"),
            "GREEN": Command(COLOR, FG, "g", "\033[38;5;34m"),
            "CYAN": Command(COLOR, FG, "c", "\033[38;5;39m"),
            "BLUE": Command(COLOR, FG, "b", "\033[38;5;27m"),
            "PURPLE": Command(COLOR, FG, "p", "\033[38;5;57m"),
            "MAGENTA": Command(COLOR, FG, "m", "\033[38;5;127m"),
            "STRONG_RED": Command(COLOR, FG, "R", "\033[38;5;196m"),
            "STRONG_ORANGE": Command(COLOR, FG, "O", "\033[38;5;202m"),
            "STRONG_YELLOW": Command(COLOR, FG, "Y", "\033[38;5;226m"),
            "STRONG_GREEN": Command(COLOR, FG, "G", "\033[38;5;82m"),
            "STRONG_CYAN": Command(COLOR, FG, "C", "\033[38;5;45m"),
            "STRONG_BLUE": Command(COLOR, FG, "B", "\033[38;5;21m"),
            "STRONG_PURPLE": Command(COLOR, FG, "P", "\033[38;5;93m"),
            "STRONG_MAGENTA": Command(COLOR, FG, "M", "\033[38;5;200m"),
            "BLACK": Command(COLOR, FG, "k", "\033[38;5;232m"),
            "DARK_GRAY": Command(COLOR, FG, "aa", "\033[38;5;238m"),
            "GRAY": Command(COLOR, FG, "a", "\033[38;5;244m"),
            "LIGHT_GRAY": Command(COLOR, FG, "A", "\033[38;5;250m"),
            "WHITE": Command(COLOR, FG, "w", "\033[1;37m")
        },
        VAR_1: {
            "DARK_RED": Command(COLOR, BG, "rr", "\033[48;5;88m"),
            "DARK_ORANGE": Command(COLOR, BG, "oo", "\033[48;5;130m"),
            "DARK_YELLOW": Command(COLOR, BG, "yy", "\033[48;5;142m"),
            "DARK_GREEN": Command(COLOR, BG, "gg", "\033[48;5;22m"),
            "DARK_CYAN": Command(COLOR, BG, "cc", "\033[48;5;31m"),
            "DARK_BLUE": Command(COLOR, BG, "bb", "\033[48;5;19m"),
            "DARK_PURPLE": Command(COLOR, BG, "pp", "\033[48;5;54m"),
            "DARK_MAGENTA": Command(COLOR, BG, "mm", "\033[48;5;127m"),
            "RED": Command(COLOR, BG, "r", "\033[48;5;124m"),
            "ORANGE": Command(COLOR, BG, "o", "\033[48;5;166m"),
            "YELLOW": Command(COLOR, BG, "y", "\033[48;5;184m"),
            "GREEN": Command(COLOR, BG, "g", "\033[48;5;34m"),
            "CYAN": Command(COLOR, BG, "c", "\033[48;5;45m"),
            "BLUE": Command(COLOR, BG, "b", "\033[48;5;27m"),
            "PURPLE": Command(COLOR, BG, "p", "\033[48;5;93m"),
            "MAGENTA": Command(COLOR, BG, "m", "\033[48;5;165m"),
            "STRONG_RED": Command(COLOR, BG, "R", "\033[48;5;196m"),
            "STRONG_ORANGE": Command(COLOR, BG, "O", "\033[48;5;202m"),
            "STRONG_YELLOW": Command(COLOR, BG, "Y", "\033[48;5;226m"),
            "STRONG_GREEN": Command(COLOR, BG, "G", "\033[48;5;82m"),
            "STRONG_CYAN": Command(COLOR, BG, "C", "\033[48;5;45m"),
            "STRONG_BLUE": Command(COLOR, BG, "B", "\033[48;5;21m"),
            "STRONG_PURPLE": Command(COLOR, BG, "P", "\033[48;5;128m"),
            "STRONG_MAGENTA": Command(COLOR, BG, "M", "\033[48;5;200m"),
            "BLACK": Command(COLOR, BG, "k", "\033[48;5;232m"),
            "DARK_GRAY": Command(COLOR, BG, "aa", "\033[48;5;238m"),
            "GRAY": Command(COLOR, BG, "a", "\033[48;5;244m"),
            "LIGHT_GRAY": Command(COLOR, BG, "A", "\033[48;5;250m"),
            "WHITE": Command(COLOR, BG, "w", "\033[48;5;255m")
        }
    },
    STYLE: {
        VAR_0: {
            "BOLD": Command(STYLE, START, "b", "\033[1m"),
            "ITALIC": Command(STYLE, START, "i", "\033[3m"),
            "UNDERLINE": Command(STYLE, START, "u", "\033[4m"),
            "STRIKE": Command(STYLE, START, "s", "\033[9m"),
            "DIM": Command(STYLE, START, "d", "\033[2m"),
            "REVERSE": Command(STYLE, START, "r", "\033[7m"),
            "HIDE": Command(STYLE, START, "h", "\033[8m")
        },
        VAR_1: {
            "BOLD": Command(STYLE, STOP, "b", "\033[22m"),
            "ITALIC": Command(STYLE, STOP, "i", "\033[23m"),
            "UNDERLINE": Command(STYLE, STOP, "u", "\033[24m"),
            "STRIKE": Command(STYLE, STOP, "s", "\033[29m"),
            "DIM": Command(STYLE, STOP, "d", "\033[22m"),
            "REVERSE": Command(STYLE, STOP, "r", "\033[27m"),
            "HIDE": Command(STYLE, STOP, "h", "\033[28m")
        }
    }
}

_command_map = {
    COLOR: {
        VAR_0: { "rr": "DARK_RED", "oo": "DARK_ORANGE", "yy": "DARK_YELLOW", "gg": "DARK_GREEN", "cc": "DARK_CYAN", "bb": "DARK_BLUE", "pp": "DARK_PURPLE", "mm": "DARK_MAGENTA", "r": "RED", "o": "ORANGE", "y": "YELLOW", "g": "GREEN", "c": "CYAN", "b": "BLUE", "p": "PURPLE", "m": "MAGENTA", "R": "STRONG_RED", "O": "STRONG_ORANGE", "Y": "STRONG_YELLOW", "G": "STRONG_GREEN", "C": "STRONG_CYAN", "B": "STRONG_BLUE", "P": "STRONG_PURPLE", "M": "STRONG_MAGENTA", "k": "BLACK", "aa": "DARK_GRAY", "a": "GRAY", "A": "LIGHT_GRAY", "w": "WHITE" },
        VAR_1: { "rr": "DARK_RED", "oo": "DARK_ORANGE", "yy": "DARK_YELLOW", "gg": "DARK_GREEN", "cc": "DARK_CYAN", "bb": "DARK_BLUE", "pp": "DARK_PURPLE", "mm": "DARK_MAGENTA", "r": "RED", "o": "ORANGE", "y": "YELLOW", "g": "GREEN", "c": "CYAN", "b": "BLUE", "p": "PURPLE", "m": "MAGENTA", "R": "STRONG_RED", "O": "STRONG_ORANGE", "Y": "STRONG_YELLOW", "G": "STRONG_GREEN", "C": "STRONG_CYAN", "B": "STRONG_BLUE", "P": "STRONG_PURPLE", "M": "STRONG_MAGENTA", "k": "BLACK", "aa": "DARK_GRAY", "a": "GRAY", "A": "LIGHT_GRAY", "w": "WHITE" }
    }, STYLE: {
        VAR_0: { "b": "BOLD", "i": "ITALIC", "u": "UNDERLINE", "s": "STRIKE", "d": "DIM", "r": "REVERSE", "h": "HIDE" },
        VAR_1: { "b": "BOLD", "i": "ITALIC", "u": "UNDERLINE", "s": "STRIKE", "d": "DIM", "r": "REVERSE", "h": "HIDE" }
    }
}

def _getcommand(g, v, n):
    return _commands[g][v][n]

colors = Container()
styles = Container()

foreground = Container()
background = Container()
start = Container()
stop = Container()
# fmt: on

_readonly_attrs(
    foreground,
    {n: (_getcommand, COLOR, VAR_0, n) for n in _commands[COLOR][VAR_0].keys()},
    {
        n: f"Command ';{l}' for foreground color: {n.lower().replace('_', ' ')}"
        for l, n in _command_map[COLOR][VAR_0].items()
    },
)
_readonly_attrs(
    background,
    {n: (_getcommand, COLOR, VAR_1, n) for n in _commands[COLOR][VAR_1].keys()},
    {
        n: f"Command ':{l}' for background color: {n.lower().replace('_', ' ')}"
        for l, n in _command_map[COLOR][VAR_1].items()
    },
)
_readonly_attrs(
    start,
    {n: (_getcommand, STYLE, VAR_0, n) for n in _commands[STYLE][VAR_0].keys()},
    {
        n: f"Command '+{l}' for start style: {n.lower().replace('_', ' ')}"
        for l, n in _command_map[STYLE][VAR_0].items()
    },
)
_readonly_attrs(
    stop,
    {n: (_getcommand, STYLE, VAR_1, n) for n in _commands[STYLE][VAR_1].keys()},
    {
        n: f"Command '-{l}' for stop style: {n.lower().replace('_', ' ')}"
        for l, n in _command_map[STYLE][VAR_1].items()
    },
)

_readonly_attrs(
    colors,
    {
        "foreground": foreground,
        "fg": foreground,
        "background": background,
        "bg": background,
    },
    {
        "foreground": "Container of all foreground colors.",
        "fg": "Shorthand for 'foreground' attribute. Container of all foreground colors.",
        "background": "Container of all background colors.",
        "bg": "Shorthand for 'background' attribute. Container of all background colors.",
    },
)
_readonly_attrs(
    styles,
    {"start": start, "stop": stop},
    {
        "start": "Container of all starting styles.",
        "stop": "Container of all stopping styles.",
    },
)
