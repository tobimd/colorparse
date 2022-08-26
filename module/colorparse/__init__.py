#!/usr/bin/python3
# 2022-present tobimd <tobimd@users.noreply.github.com>

"""
    The colorparse module and script will allow the user to add color and styles to text using "commands".
    
    These are short commands that facilitate the process of setting up text effects when printing, because it avoids things like:
    >>> print(Color.DARK_RED + "Hello")

    And instead uses commands like ";rr" for the color dark red:
    >>> print(";rrHello") # prints "Hello"
    
    Note: If needed, the first format can still be used, though a bit "wordy".

    Methods:
    ----
        - `register_command(name:str, command:str, value:str)`
        - `configuration(tag:str|object, **values)`
        - `show_commands()`
        - `print(*value, overflow:bool|None, sep:str|None, end:str|None, file:SupportsWrite[str]|None, flush:bool|None)`
        - `paint(*value, overflow:bool|None, sep:str|None, end:str|None)`
        - `clean(input_string:str) -> str`

    Variables:
    ----
        - `colors`: Container for all registered colors.
        - `styles`: Container for all registered styles.
        - `options`: Stores program-wide configuration for default values and data.
        - `RESET`: Literal string for the ANSI escape sequence 'ESC[0m' (resets colors and styles).
        - `__version__`: This package's version.

    Use Python's builtin function `help` to get more info on each one.
"""
from .typeshed import *
from ._constants import *
from ._datatypes import *
from ._containers import *
from ._util import *
