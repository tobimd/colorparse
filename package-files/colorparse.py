#!/usr/bin/python3
import argparse
import os
import re
import sys
from enum import Flag, auto
from functools import partial

__version__ = "2.0.0"


# Class used to keep enum values
class Color(Flag):
    FOREGROUND = auto()
    BACKGROUND = auto()
    BOTH = FOREGROUND | BACKGROUND


# Default values
class _Config:
    paint = {
        "print": True,
        "ret": True,
        "overflow": False,
        "sep": " ",
        "end": "\033[0m\n",
        "file": sys.stdout,
        "flush": False,
    }

    flags = {
        "ignore_special": False,
        "always_finish_colors": True,
        "true_color": False,
        "should_update_color_maps": False,
        "ignore_idle_use_warning": False,
    }

    data = {
        "regex": (
            r"((?:(?P<sqb>\[(?=[^\]\(\)\\]*?\]))\s*|(?P<par>\((?=[^\)"
            + r"\[\]\\]*?\)))\s*)|\/)?(?:\\)?((?P<fg>;)|(?P<bg>:))(;|:"
            + r"|(?(fg)(?P<fgc>rr|oo|yy|gg|cc|bb|pp|mm|aa|r|o|y|g|c|b|"
            + r"p|m|a|k|w|R|O|Y|G|C|B|P|M|A)|(?(bg)(?P<bgc>rr|oo|yy|gg"
            + r"|cc|bb|pp|mm|aa|r|o|y|g|c|b|p|m|a|k|w|R|O|Y|G|C|B|P|M|"
            + r"A)))|[\+\-](?P<st>[biusdrh])|(?P<eq>=)|(?P<hs>#)|\!)(?"
            + r"(eq)(?P<rgb>\d{0,3},?\d{0,3},?\d{0,3})|(?(hs)(?P<hex>["
            + r"0-9a-fA-F]{0,6})))(?(sqb)(?:\s*\])|(?(par)(?:\s*\))|\/"
            + r"?))"
        )
    }


# Color definitions
class _Color:
    ENDC = "\033[0m"

    class Foreground:

        # COLOR NAME       # CODE  # ANSI COLOR      # TRUE COLOR
        DARK_RED = ("rr", "\033[38;5;88m", "\033[38;2;130;0;0m")
        DARK_ORANGE = ("oo", "\033[38;5;130m", "\033[38;2;160;50;0m")
        DARK_YELLOW = ("yy", "\033[38;5;142m", "\033[38;2;150;120;0m")
        DARK_GREEN = ("gg", "\033[38;5;22m", "\033[38;2;0;80;0m")
        DARK_CYAN = ("cc", "\033[38;5;31m", "\033[38;2;0;120;130m")
        DARK_BLUE = ("bb", "\033[38;5;24m", "\033[38;2;20;50;130m")
        DARK_PURPLE = ("pp", "\033[38;5;54m", "\033[38;2;90;0;150m")
        DARK_MAGENTA = ("mm", "\033[38;5;90m", "\033[38;2;130;0;100m")

        RED = ("r", "\033[38;5;124m", "\033[38;2;180;0;0m")
        ORANGE = ("o", "\033[38;5;166m", "\033[38;2;200;90;0m")
        YELLOW = ("y", "\033[38;5;184m", "\033[38;2;190;170;0m")
        GREEN = ("g", "\033[38;5;34m", "\033[38;2;0;150;0m")
        CYAN = ("c", "\033[38;5;39m", "\033[38;2;0;190;200m")
        BLUE = ("b", "\033[38;5;27m", "\033[38;2;0;70;255m")
        PURPLE = ("p", "\033[38;5;57m", "\033[38;2;100;0;180m")
        MAGENTA = ("m", "\033[38;5;127m", "\033[38;2;190;0;150m")

        STRONG_RED = ("R", "\033[38;5;196m", "\033[38;2;255;0;0m")
        STRONG_ORANGE = ("O", "\033[38;5;202m", "\033[38;2;255;150;0m")
        STRONG_YELLOW = ("Y", "\033[38;5;226m", "\033[38;2;255;255;0m")
        STRONG_GREEN = ("G", "\033[38;5;82m", "\033[38;2;0;255;0m")
        STRONG_CYAN = ("C", "\033[38;5;45m", "\033[38;2;0;255;255m")
        STRONG_BLUE = ("B", "\033[38;5;21m", "\033[38;2;0;20;255m")
        STRONG_PURPLE = ("P", "\033[38;5;93m", "\033[38;2;150;0;255m")
        STRONG_MAGENTA = ("M", "\033[38;5;200m", "\033[38;2;225;0;225m")

        BLACK = ("k", "\033[38;5;232m", "\033[38;2;0;0;0m")
        DARK_GRAY = ("A", "\033[38;5;238m", "\033[38;2;70;70;70m")
        GRAY = ("a", "\033[38;5;244m", "\033[38;2;130;130;130m")
        LIGHT_GRAY = ("aa", "\033[38;5;250m", "\033[38;2;185;185;185m")
        WHITE = ("w", "\033[1;37m", "\033[38;2;255;255;255m")

        maps = {
            "R": "STRONG_RED",
            "O": "STRONG_ORANGE",
            "Y": "STRONG_YELLOW",
            "G": "STRONG_GREEN",
            "C": "STRONG_CYAN",
            "B": "STRONG_BLUE",
            "P": "STRONG_PURPLE",
            "M": "STRONG_MAGENTA",
            "r": "RED",
            "o": "ORANGE",
            "y": "YELLOW",
            "g": "GREEN",
            "c": "CYAN",
            "b": "BLUE",
            "p": "PURPLE",
            "m": "MAGENTA",
            "rr": "DARK_RED",
            "oo": "DARK_ORANGE",
            "yy": "DARK_YELLOW",
            "gg": "DARK_GREEN",
            "cc": "DARK_CYAN",
            "bb": "DARK_BLUE",
            "pp": "DARK_PURPLE",
            "mm": "DARK_MAGENTA",
            "k": "BLACK",
            "A": "LIGHT_GRAY",
            "a": "GRAY",
            "aa": "DARK_GRAY",
            "w": "WHITE",
        }

    class Background:

        DARK_RED = ("rr", "\033[48;5;88m", "\033[48;2;130;0;0m")
        DARK_ORANGE = ("oo", "\033[48;5;130m", "\033[48;2;160;50;0m")
        DARK_YELLOW = ("yy", "\033[48;5;142m", "\033[48;2;150;120;0m")
        DARK_GREEN = ("gg", "\033[48;5;22m", "\033[48;2;0;80;0m")
        DARK_CYAN = ("cc", "\033[48;5;31m", "\033[48;2;0;120;130m")
        DARK_BLUE = ("bb", "\033[48;5;19m", "\033[48;2;20;50;130m")
        DARK_PURPLE = ("pp", "\033[48;5;54m", "\033[48;2;90;0;150m")
        DARK_MAGENTA = ("mm", "\033[48;5;127m", "\033[48;2;130;0;100m")

        RED = ("r", "\033[48;5;124m", "\033[48;2;180;0;0m")
        ORANGE = ("o", "\033[48;5;166m", "\033[48;2;200;90;0m")
        YELLOW = ("y", "\033[48;5;184m", "\033[48;2;190;170;0m")
        GREEN = ("g", "\033[48;5;34m", "\033[48;2;0;150;0m")
        CYAN = ("c", "\033[48;5;45m", "\033[48;2;0;190;200m")
        BLUE = ("b", "\033[48;5;27m", "\033[48;2;0;70;255m")
        PURPLE = ("p", "\033[48;5;93m", "\033[48;2;100;0;180m")
        MAGENTA = ("m", "\033[48;5;165m", "\033[48;2;190;0;150m")

        STRONG_RED = ("R", "\033[48;5;196m", "\033[48;2;255;0;0m")
        STRONG_ORANGE = ("O", "\033[48;5;202m", "\033[48;2;255;150;0m")
        STRONG_YELLOW = ("Y", "\033[48;5;226m", "\033[48;2;255;255;0m")
        STRONG_GREEN = ("G", "\033[48;5;82m", "\033[48;2;0;255;0m")
        STRONG_CYAN = ("C", "\033[48;5;45m", "\033[48;2;0;255;255m")
        STRONG_BLUE = ("B", "\033[48;5;21m", "\033[48;2;0;20;255m")
        STRONG_PURPLE = ("P", "\033[48;5;128m", "\033[48;2;150;0;255m")
        STRONG_MAGENTA = ("M", "\033[48;5;200m", "\033[48;2;225;0;225m")

        BLACK = ("k", "\033[48;5;232m", "\033[48;2;0;0;0m")
        DARK_GRAY = ("A", "\033[48;5;238m", "\033[48;2;70;70;70m")
        GRAY = ("a", "\033[48;5;244m", "\033[48;2;130;130;130m")
        LIGHT_GRAY = ("aa", "\033[48;5;250m", "\033[48;2;185;185;185m")
        WHITE = ("w", "\033[48;5;255m", "\033[48;2;255;255;255m")

        maps = {
            "R": "STRONG_RED",
            "O": "STRONG_ORANGE",
            "Y": "STRONG_YELLOW",
            "G": "STRONG_GREEN",
            "C": "STRONG_CYAN",
            "B": "STRONG_BLUE",
            "P": "STRONG_PURPLE",
            "M": "STRONG_MAGENTA",
            "r": "RED",
            "o": "ORANGE",
            "y": "YELLOW",
            "g": "GREEN",
            "c": "CYAN",
            "b": "BLUE",
            "p": "PURPLE",
            "m": "MAGENTA",
            "rr": "DARK_RED",
            "oo": "DARK_ORANGE",
            "yy": "DARK_YELLOW",
            "gg": "DARK_GREEN",
            "cc": "DARK_CYAN",
            "bb": "DARK_BLUE",
            "pp": "DARK_PURPLE",
            "mm": "DARK_MAGENTA",
            "k": "BLACK",
            "A": "LIGHT_GRAY",
            "a": "GRAY",
            "aa": "DARK_GRAY",
            "w": "WHITE",
        }

    class Style:
        BOLD = ("b", "\033[1m", "\033[22m")
        ITALIC = ("i", "\033[3m", "\033[23m")
        UNDERLINE = ("u", "\033[4m", "\033[24m")
        STRIKE = ("s", "\033[9m", "\033[29m")
        DIM = ("d", "\033[2m", "\033[22m")
        REVERSE = ("r", "\033[7m", "\033[27m")
        HIDE = ("h", "\033[8m", "\033[28m")

        maps = {
            "b": "BOLD",
            "i": "ITALIC",
            "u": "UNDERLINE",
            "s": "STRIKE",
            "d": "DIM",
            "r": "REVERSE",
            "h": "HIDE",
        }


# Exception class for printing custom errors
class ColorparseError(Exception):
    """Base class for exceptions in this module"""

    pass


# Each time there is a change in the color codes, reconstruct regex
def _construct_regex():
    # Usual parts of the regex:
    str_enc = (
        r"((?:(?P<sqb>\[(?=[^\]\(\)\\]*?\]))\s*|(?P<par>\((?=[^\)\[\]\\]*?\)"
        + r"))\s*)|\/)?"
    )
    str_codes = r"(?:\\)?((?P<fg>;)|(?P<bg>:))(;|:|"

    # Here would go: codes(fg_colors, bg_colors)

    end_codes = (
        r"|[\+\-](?P<st>[biusdrh])|(?P<eq>=)|(?P<hs>#)|\!)(?(eq)(?P<rgb>"
        + r"\d{0,3},?\d{0,3},?\d{0,3})|(?(hs)(?P<hex>[0-9a-fA-F]{0,6})))"
    )
    end_enc = r"(?(sqb)(?:\s*\])|(?(par)(?:\s*\))|\/?))"

    # Get both color codes and sort them by length in reverse
    # (longest to smallest)
    fg = sorted(_Color.Foreground.maps.keys(), key=len, reverse=True)
    bg = sorted(_Color.Background.maps.keys(), key=len, reverse=True)

    # The changing part of the regex, depending on color code definitions
    codes = rf"(?(fg)(?:{'|'.join(fg)})|(?(bg)(?:{'|'.join(bg)})))"

    # Join all the regex, and replace the old one
    _Config.data["regex"] = f"{str_enc}{str_codes}{codes}{end_codes}{end_enc}"


# Stick number between the ranges of 0 to 255
def _rgb_clamp(num):
    if type(num) == str:
        num = int(num) if num != "" else 0

    return str(max(0, min(255, num)))


# Transform hex color to rgb color
def _hex_to_rgb(string):
    string = string + "0" * (6 - len(string))

    r = int(string[:2], 16)
    g = int(string[2:4], 16)
    b = int(string[4:], 16)

    return map(_rgb_clamp, (r, g, b))


# Clean string to return rgb values from comma separated input
def _str_to_rgb(string):
    r, g, b = (string + "," * (2 - string.count(","))).split(",")

    return map(_rgb_clamp, (r, g, b))


# Remove extra code components (e.g. brackets)
def _strip(code):
    return re.sub(r"\[|\]|\(|\)| ", "", code)


# Replace special characters if "-I" or "--ignore-special" flag is set
def _try_ignore_special(string):
    if not _Config.flags["ignore_special"]:
        return string

    chars = "nabfrvt"

    def repl(matchobj):
        special = {c: rf"\{c}" for c in chars}

        match = matchobj[0]

        double = match[:-2] + special[match[-1]]
        single = match[1:]

        return double if len(match) % 2 == 0 else single

    return re.sub(rf"\\+[{chars}]", repl, string)


# Replace individual matches of each code into the ansi escape sequence
def _color_repl(match) -> str:

    # Get the correct attribute of a class
    def get_attr(color_class, match, index):
        return getattr(color_class, color_class.maps[match])[index]

    # Update the 'maps' attribute of the given class
    def update_maps(color_class):
        maps = dict()

        for color_name in dir(color_class):
            if not color_name.startswith("__") and not color_name == "maps":
                maps[getattr(color_class, color_name)[0]] = color_name

        color_class.maps = maps

    gm = match[0]  # Global match (0th match)

    # If color code was escaped, return without the backslash
    if "\\" in gm:
        return gm.replace("\\", "")

    # If the code is of type "end color", return ENDC
    if ";:" in gm or ":;" in gm:
        return _Color.ENDC

    # If it's a special rgb color code
    if "#" in gm or "=" in gm:
        if not _Config.flags["true_color"]:
            return gm

        elif "#" in gm:
            r, g, b = _hex_to_rgb(match["hex"])

        else:
            r, g, b = _str_to_rgb(match["rgb"])

        if ";" in gm:
            t = "38"
        else:
            t = "48"

        return f"\033[{t};2;{r};{g};{b}m"

    # If it's a special style code
    if "+" in gm or "-" in gm:
        index = 1 if "+" in gm else 2

        return get_attr(_Color.Style, match["st"], index)

    # Check if color definitions were changed, to update
    # the 'maps' attribute of both color types
    if _Config.flags["should_update_color_maps"]:
        update_maps(_Color.Foreground)
        update_maps(_Color.Background)

        _Config.flags["should_update_color_maps"] = False

    index = 2 if _Config.flags["true_color"] else 1

    # If it's a background-type color code
    if ":" in gm:
        return get_attr(_Color.Background, match["bgc"], index)

    # If it's foreground-type color code
    if ";" in gm:
        return get_attr(_Color.Foreground, match["fgc"], index)

    return gm


# Search and replace matched color codes
def _match_color_codes(string: str):
    # Before actually replacing each code by an ansi color,
    # search and fix special codes (i.e. ';;' and '::')

    # Return int to check if color code is type ';:', ';;', etc.
    # or otherwise
    def end_type(code):
        if ";:" in code or ":;" in code:
            return 0
        elif ";;" in code:
            return 1
        elif "::" in code:
            return 2
        elif "!" in code:
            return 3
        else:
            return -1

    # Similarly, check if color code is either forground, background
    # or neither
    def color_type(code):
        if "+" in code or "-" in code:
            return 0
        elif ";" in code and end_type(code) < 0:
            return 1
        elif ":" in code and end_type(code) < 0:
            return 2
        else:
            return -1

    # Do not match backslashes
    match_iter = re.finditer(_Config.data["regex"], string)
    matches = [m for m in match_iter if "\\" not in m[0]]

    prev_fg = None
    prev_bg = None

    prev_st = None
    curr_st = None

    bd = ["b", "d"]

    # Iterate through all matches and fix both the case of having
    # either ';;' and '::', and the case where the special styling codes
    # are used (with ';+' or ';-')
    for index, match in enumerate(matches):
        code = match[0]

        prev_st = curr_st if curr_st is not None else prev_st
        curr_st = match if color_type(code) == 0 else None

        prev_fg = match if color_type(code) == 1 else prev_fg
        prev_bg = match if color_type(code) == 2 else prev_bg

        # Check if the case of ";+b ... ;-d" happened or the reverse case
        # with with ";+d ... ;-b" happened
        curr_st_check = (
            curr_st is not None and "-" in curr_st[0] and curr_st["st"] in bd
        )

        prev_st_check = (
            prev_st is not None and "+" in prev_st[0] and prev_st["st"] in bd
        )

        # If ';;' or '::' are found, fix this case
        if end_type(code) > -1:
            # If it's just ending both colors, remember to reset the variables
            if end_type(code) == 0:

                if prev_st is not None:
                    string = string.replace(code, f"[;:]{prev_st[0]}", 1)
                    matches.insert(index + 1, prev_st)

                prev_fg = None
                prev_bg = None

            # If ending foreground color
            if end_type(code) == 1:
                matches[index] = ["[;:]"]

                if prev_bg is None and prev_st is None:
                    string = string.replace(code, "[;:]", 1)

                if prev_bg is not None:
                    repl = "[;:]" if prev_st is None else code

                    string = string.replace(code, f"{repl}{prev_bg[0]}", 1)
                    matches.insert(index + 1, prev_bg)

                if prev_st is not None:
                    string = string.replace(code, f"[;:]{prev_st[0]}", 1)
                    matches.insert(index + 1, prev_st)

                prev_fg = None

            # Else, ending the background color
            elif end_type(code) == 2:
                matches[index] = ["[;:]"]

                if prev_fg is None and prev_st is None:
                    string = string.replace(code, "[;:]", 1)

                if prev_fg is not None:
                    repl = "[;:]" if prev_st is None else code

                    string = string.replace(code, f"{repl}{prev_fg[0]}", 1)
                    matches.insert(index + 1, prev_fg)

                if prev_st is not None:
                    string = string.replace(code, f"[;:]{prev_st[0]}", 1)
                    matches.insert(index + 1, prev_st)

                prev_bg = None

            # Otherwise, it's the '!' to end all colors and styles
            else:
                string = string.replace(code, "[;:]", 1)

                prev_fg = None
                prev_bg = None
                prev_st = None

        elif curr_st_check and prev_st_check and curr_st["st"] != prev_st["st"]:
            string = string.replace(
                code, (f"[;-{curr_st['st']}]" + f"[;+{prev_st['st']}]")
            )
            curr_st = prev_st

    # Replace color codes with the respective ansi escape sequences
    return re.sub(_Config.data["regex"], _color_repl, string)


# Function helper, returns a list of the input color types
def _get_color_types(color_type):
    # Get the corresponding color classes
    color_classes = [None, None]

    if Color.FOREGROUND in color_type:
        color_classes[0] = _Color.Foreground

    if Color.BACKGROUND in color_type:
        color_classes[1] = _Color.Background

    if not any(color_classes):
        raise ValueError("Expected a color type")

    return color_classes


def register(
    color_type, color_code, color_value="", true_color_value="", code_name=None, **flags
):
    ignore_repeats = flags.get("ignore_repeats", False)
    silent = flags.get("silent", False)

    color_classes = _get_color_types(color_type)

    exists = lambda c, x: c in x.maps.keys()
    # Check if the color code is already taken or it uses bad characters
    is_repeated = [
        None if color_classes[0] is None else exists(color_code, color_classes[0]),
        None if color_classes[1] is None else exists(color_code, color_classes[1]),
    ]

    # If missing both classes from 'color_type'
    if not any(color_classes):
        if not silent:
            print(
                "At least one color class must be given to register the " + "color code"
            )
        return False

    # If found existing color code
    if any(is_repeated) and not ignore_repeats:
        if not silent:
            print(
                f'Can\'t register code "{str(color_code)}" because it '
                + "is already defined."
            )
        return False

    # If the new code has characters that may break functionallity
    if re.fullmatch(r"\w+", color_code) is None:
        if not silent:
            print("Only alphanumeric characters are allowed to be used in " + "codes.")
        return False

    # If at least one is repeated, then use that as name
    if any(is_repeated):
        attr_name = (
            color_classes[0].maps[color_code]
            if is_repeated[0]
            else color_classes[1].maps[color_code]
        )

    # Otherwise, use "USER_<code>"
    else:
        attr_name = (
            f"USER_{color_code.upper()}" if code_name is None else code_name.upper()
        )

    # Add new color codes
    attr_value = (color_code, color_value, true_color_value)

    if color_classes[0] is not None:
        setattr(color_classes[0], attr_name, attr_value)
        color_classes[0].maps[color_code] = attr_name

    if color_classes[1] is not None:
        setattr(color_classes[1], attr_name, attr_value)
        color_classes[1].maps[color_code] = attr_name

    # Set flag to update color maps
    _Config.flags["should_update_color_maps"] = True


def remove(color_type, color_code=None, code_name=None, **flags):
    ignore_missing = flags.get("ignore_missing_color", False)
    silent = flags.get("silent", False)

    color_classes = _get_color_types(color_type)

    code_exists = lambda c, x: c in x.maps.keys()
    name_exists = lambda n, x: n in x.maps.values()

    # If missing both classes from 'color_type'
    if not any(color_classes):
        if not silent:
            print(
                "At least one color class must be given to register the " + "color code"
            )
        return False

    # If neither the color_code nor code_name are given
    if color_code is None and code_name is None:
        if not silent:
            print(
                "At least one part of the code must be given to remove it "
                + "(either the code or the name)."
            )
        return False

    # If the given attributes do not exist for the classes
    if not ignore_missing:
        for cclass in color_classes:
            if color_class is not None:
                exists = code_name is None and code_exists(color_code, cclass)
    # Set flag to update color maps
    _Config.flags["should_update_color_maps"] = True


# Prints a pre made list of color codes
def codes():
    """Prints a list of all the color codes available.
    It also displays what the colors look as
    background type and foreground type.
    """

    help_string = """  > [;+b]color list[;-b]:

 [background] [foreground] [code]   [name]
   "(;w):(;a)<code>(;:)"   "(;w);(;a)<code>(;:)"\n
   [:rr]        [;:]     [;rr]red     [;:]     [;w]rr[;:]   (DARK_RED)
   [:oo]        [;:]     [;oo]orange  [;:]     [;w]oo[;:]   (DARK_ORANGE)
   [:yy]        [;:]     [;yy]yellow  [;:]     [;w]yy[;:]   (DARK_YELLOW)
   [:gg]        [;:]     [;gg]green   [;:]     [;w]gg[;:]   (DARK_GREEN)
   [:cc]        [;:]     [;cc]cyan    [;:]     [;w]cc[;:]   (DARK_CYAN)
   [:bb]        [;:]     [;bb]blue    [;:]     [;w]bb[;:]   (DARK_BLUE)
   [:pp]        [;:]     [;pp]purple  [;:]     [;w]pp[;:]   (DARK_PURPLE)
   [:mm]        [;:]     [;mm]magenta [;:]     [;w]mm[;:]   (DARK_MAGENTA)\n
   [:r ]        [;:]     [;r ]red     [;:]     [;w]r [;:]   (RED)
   [:o ]        [;:]     [;o ]orange  [;:]     [;w]o [;:]   (ORANGE)
   [:y ]        [;:]     [;y ]yellow  [;:]     [;w]y [;:]   (YELLOW)
   [:g ]        [;:]     [;g ]green   [;:]     [;w]g [;:]   (GREEN)
   [:c ]        [;:]     [;c ]cyan    [;:]     [;w]c [;:]   (CYAN)
   [:b ]        [;:]     [;b ]blue    [;:]     [;w]b [;:]   (BLUE)
   [:p ]        [;:]     [;p ]purple  [;:]     [;w]p [;:]   (PURPLE)
   [:m ]        [;:]     [;m ]magenta [;:]     [;w]m [;:]   (MAGENTA)\n
   [:R ]        [;:]     [;R ]red     [;:]     [;w]R [;:]   (STRONG_RED)
   [:O ]        [;:]     [;O ]orange  [;:]     [;w]O [;:]   (STRONG_ORANGE)
   [:Y ]        [;:]     [;Y ]yellow  [;:]     [;w]Y [;:]   (STRONG_YELLOW)
   [:G ]        [;:]     [;G ]green   [;:]     [;w]G [;:]   (STRONG_GREEN)
   [:C ]        [;:]     [;C ]cyan    [;:]     [;w]C [;:]   (STRONG_CYAN)
   [:B ]        [;:]     [;B ]blue    [;:]     [;w]B [;:]   (STRONG_BLUE)
   [:P ]        [;:]     [;P ]purple  [;:]     [;w]P [;:]   (STRONG_PURPLE)
   [:M ]        [;:]     [;M ]magenta [;:]     [;w]M [;:]   (STRONG_MAGENTA)\n
   [:k ]        [;:]    [;k ]black     [;:]    [;w]k [;:]   (BLACK)
   [:aa]        [;:]    [;aa]dark gray [;:]    [;w]aa[;:]   (DARK_GRAY)
   [:a ]        [;:]    [;a ]gray      [;:]    [;w]a [;:]   (GRAY)
   [:A ]        [;:]    [;A ]light gray[;:]    [;w]A [;:]   (LIGHT_GRAY)
   [:w ]        [;:]    [;w ]white     [;:]    [;w]w [;:]   (WHITE)

  > [;+b]starting a style[;-b]:   "(;w);+(;a)<code>(;:)" or "(;w):+(;a)<code>(;:)"
  >   [;+b]ending a style[;-b]:   "(;w);-(;a)<code>(;:)" or "(;w):-(;a)<code>(;:)"\n
              [style]      [code] [name]\n
               [;+b]bold[;-b]          [;w]b[;:]    (BOLD)
               [;+i]italic[;-i]        [;w]i[;:]    (ITALIC)
               [;+u]underline[;-u]     [;w]u[;:]    (UNDERLINE)
               [;+s]strike[;-s]        [;w]s[;:]    (STRIKE)
               [;+d]dim[;-d]           [;w]d[;:]    (DIM)
               [;+r]reverse[;-r]       [;w]r[;:]    (REVERSE)
               [;+h]hide[;-h]          [;w]h[;:]    (HIDE)\n
  > [;+b]color ending[;-b]:\n
        end color         [;w]\;: | \:;[;:] (ENDC)
        end fg color         [;w]\;;[;:]
        end bg color         [;w]\::[;:]
        end color & style    [;w]\;![;:]
"""

    extra_string = """  > [;+b]custom colors[;-b]:

 [format type]   [code]   [name]         [description]

      rgb          [;w]=[;:]      (RGB)           Up to 3 values
                                          from 0 to 255,
                                          comma separated

      hex          [;w]#[;:]      (HEXADECIMAL)   Up to 6 values
                                          from 0 to f
    """

    paint(help_string, print=True)

    if _Config.flags["true_color"]:
        paint(extra_string, print=True)


# Changes default values and other options
def options(fn, **kwargs):
    """This function is meant to be used at the
    beggining of the program, to set permanent default
    values. This way, it helps to avoid having to
    constantly set the same arguments that would
    otherwise be omitted. The 'kwargs' argument
    recieves one or more key/value pairs for the
    function 'fn'.

    It was designed to help both for future functions
    that may be added and to make lines of code
    shorter.

    Arguments            Descriptions
    -----------------    -----------------------------
    fn                   Either the name or the
                         function itself, from which
                         the changes for default
                         values will be applied.

    kwargs               Key - value pairs for each
                         default argument to set.
    """

    if callable(fn):
        fn = fn.__name__

    for k, v in kwargs.items():
        getattr(_Config, fn)[k] = v


# It's meant to work just like the built-in function "print"
def paint(*value, **options):
    """Returns a string that will have color codes
    converted to ANSI escape sequences.

    Having 'print' as 'False', makes the arguments
    'end', 'file' and 'flush' to not be considered
    whatever their values may be, because those are
    only used when printing.

    When there is more than one string and the
    argument 'overflow' is 'True', any unfinished
    color will pass through to other strings.
    Otherwise, colors will be finished at the end of
    each string.

    It's worth noting that regardless of the value
    this argument has, the function will always finish
    all color codes at the end of the last string (the
    same as adding a ';:').

    Arguments            Descriptions
    -----------------    -----------------------------
    value                One or more values to be
                         parsed.

    print=True           If true, the obtained string
                         will be printed.

    ret=True             If true, the obtained string
                         will be returned.

    overflow=False       If true, allow unfinished
                         colors to overflow onto other
                         strings.

    sep=' '	         Inserted between the given
                         strings.

    end='\\n'	         Appended after the last
                         string (when it's printed)

    file=sys.stdout	 A file-like object (stream).

    flush=False 	 Whether to forcibly flush the
                         stream (when the strings are
                         printed) or not.
    """
    ec = _Color.ENDC
    value = list(value)

    # Get the options' arguments
    _print = options.get("print", _Config.paint["print"])
    _ret = options.get("ret", _Config.paint["ret"])
    _overflow = options.get("overflow", _Config.paint["overflow"])
    _sep = _match_color_codes(options.get("sep", _Config.paint["sep"]))
    _end = _match_color_codes(options.get("end", _Config.paint["end"]))
    _file = options.get("file", _Config.paint["file"])
    _flush = options.get("flush", _Config.paint["flush"])

    FC = ec if _Config.flags["always_finish_colors"] else ""

    # If overflow is true, then color the strings as one
    if _overflow:
        result = _match_color_codes(_sep.join(map(str, value)))

        if _print:
            print(result, end=(_end + FC), file=_file, flush=_flush)

    # Else, color one by one and the join them
    else:
        result = (ec + _sep).join(map(_match_color_codes, map(str, value)))

        if _print:
            print(result, end=(ec + _end + FC), file=_file, flush=_flush)

    # Return the result
    if _ret:
        return result + FC


# Parses arguments from the terminal
def _arg_parser():
    su = "\033[4m"  # Set text with underline
    eu = "\033[24m"  # End underline

    sb = "\033[1m"  # Set text in bold
    eb = "\033[22m"  # End bold style

    si = "\033[3m"  # Set text in italic
    ei = "\033[23m"  # End italic style

    nl = f"{si}"  # Add new line

    # Initiate argument parser
    parser = argparse.ArgumentParser(
        prog="colorparse",
        add_help=False,
        usage=f"colorparse [{su}options{eu}]\n\
       colorparse [{su}options{eu}] [{su}string{eu} ...] [{sb}-o{eb} {su}output file{eu}]\n\
       colorparse [{su}options{eu}] [{su}string{eu} ...] [{sb}-p{eb} {su}position{eu}] [{sb}-i{eb} {su}input file{eu} ...] [{sb}-o{eb} {su}output file{eu}]",
    )

    # Arguments
    parser.add_argument(
        "string", help="one or more input strings.", nargs="*", default=[]
    )

    parser.add_argument(
        "-h",
        "--help",
        help=f"show this help message and exit.",
        action="help",
        default=argparse.SUPPRESS,
    )

    parser.add_argument(
        "-c",
        "--codes",
        help=f"show the available color codes and exit.",
        action="store_true",
    )

    parser.add_argument(
        "-v",
        "--version",
        help=f"show the current version of this module and\
                              exit.",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-t",
        "--true-color",
        help=f"use of RGB values for the ANSI escape sequences.\
                              Allowes customized foreground color codes and a\
                              more accurate color set. {su}Note{eu}: having this\
                              option won't work on all terminals as they do\
                              not all support true color (24-bit colors).",
        action="store_true",
    )

    parser.add_argument(
        "-s",
        "--sep",
        help=f"specify what string to use, to separate string\
                              arguments (default is ' ').",
        default=_Config.paint["sep"],
        metavar=f"{su}string{eu}",
    )

    parser.add_argument(
        "-e",
        "--end",
        help=f"specify what string to use at the end of the\
                              printed string (default is '\\n' followed by\
                              color & style ending with \"{si};!{ei}\").",
        default=_Config.paint["end"],
        metavar=f"{su}string{eu}",
    )

    parser.add_argument(
        "-O",
        "--overflow",
        help=f"make colors overflow to other strings if a color\
                              code is not finished.",
        action="store_true",
    )

    parser.add_argument(
        "-C",
        "--dont-finish-colors",
        help=f'do not finish colors at the end of the last\
                              string. Normally, everytime the\
                              "{su}paint{eu}" function is used, all colors\
                              and styles are finished at the end to avoid\
                              making the effects seap to the rest of the\
                              program or terminal. This option will disable\
                              that.',
        action="store_true",
    )

    parser.add_argument(
        "-I",
        "--ignore-special",
        help=f"tell the parser to ignore special characters\
                              like (new line, tab, etc.).",
        action="store_true",
    )

    parser.add_argument(
        "-S",
        "--strip",
        help=f"specify which leading and trailing\
                              characters to remove from input file(s)\
                              (by default removes whitespace if the flag is\
                              used).",
        nargs="?",
        const=None,
        default="",
        metavar=f"{su}chars{eu}",
    )

    parser.add_argument(
        "-p",
        "--position",
        help=f"insert all strings at the given index in the\
                              list of input files.",
        nargs=1,
        default=0,
        type=int,
        metavar=f"{su}position{eu}",
    )

    parser.add_argument(
        "-i",
        "--input-file",
        help=f"specify one or more files to read the color\
                              coded strings from. If a file doesn't exist, an\
                              error will be raised. It must be used after any \
                              {su}string{eu} argument.",
        nargs="+",
        type=argparse.FileType("r"),
        default=[],
        metavar=f"{su}input file{eu}",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        help=f"specify an output file to append the resulting\
                              string (default is sys.stdout).",
        nargs=1,
        type=argparse.FileType("a"),
        default=_Config.paint["file"],
        metavar=f"{su}output file{eu}",
    )

    parser.add_argument(
        "-W",
        "--ignore-idle-warning",
        help=f"do not print a warning when using this\
                               module inside Python IDLE.",
        action="store_true",
    )

    # Return the arguments to "_main"
    return parser, parser.parse_args()


def _main():
    # Get arguments
    parser, args = _arg_parser()

    # Set base values
    _Config.flags["true_color"] = args.true_color
    _Config.flags["ignore_special"] = args.ignore_special
    _Config.flags["ignore_idle_use_warning"] = args.ignore_idle_warning

    all_strings = []
    n_strings = len(args.string)
    n_files = len(args.input_file)

    # Check if this module is being used inside Python IDLE
    strip_formatting = (
        "idlelib.run" in sys.modules and not _Config.flags["ignore_idle_use_warning"]
    )
    if strip_formatting:
        print(" Warning: ansi color escape codes do not work inside Python IDLE!\n")

    # Exit if 'codes' option is used, or there is no input
    if args.codes:
        codes()
        sys.exit(0)

    if n_strings == 0 and n_files == 0:
        if strip_formatting:
            print(
                " colorparse [options]\n colorparse [options] [subtring "
                + "...] [-o output file]\n colorparse [options] [string "
                + "...] [-p position] [-i input file ...] [-o output file"
                + "]"
            )
        else:
            parser.print_usage()
        sys.exit(0)

    # Clean special characters if value is set
    args.sep = _try_ignore_special(args.sep)
    args.end = _try_ignore_special(args.end)
    args.strip = _try_ignore_special(args.strip)

    # Add input files first.
    for f in args.input_file:
        string = _try_ignore_special(f.read().strip(args.strip))
        all_strings.append(string)

    for s in args.string[::-1]:
        all_strings.insert(args.position, _try_ignore_special(s))

    # Add arguments to _paint
    _paint = partial(
        paint,
        print=True,
        overflow=args.overflow,
        sep=args.sep,
        end=args.end,
        file=args.output_file,
    )
    for v in all_strings:
        _paint = partial(_paint, v)

    # Print
    _paint()


if __name__ == "__main__":
    _main()


if sys.platform[:3] == "win":
    os.system("color")
