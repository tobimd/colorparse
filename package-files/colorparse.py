#!/usr/bin/python3
import os
import sys
import re
import argparse

from functools import partial

__version__ = "2.0.0"


# Default values
class _Config:
    paint = {
        'print': True,
        'ret': True,
        'overflow': False,
        'sep': ' ',
        'end': '\033[0m\n',
        'file': sys.stdout,
        'flush': False,
    }

    flags = {
        'ignore_special': False,
        'always_finish_colors': True,
        'true_color': False,
        'always_try_rgb_codes': True,
        'auto_fix_bad_rgb': True,
        'color_defs_were_changed': False
    }

    data = {
        'regex': r"((?:(?P<sqb>\[(?=[^\]\(\)\\]*?\]))\s*|(?P<par>\((?=[^\)\[\]\\]*?\)))\s*)|/)?(?:\\)?((?P<fg>;)|(?P<bg>:))(;|:|(?(fg)(?P<fgc>rr|oo|yy|gg|cc|bb|pp|mm|aa|r|o|y|g|c|b|p|m|a|k|w|R|O|Y|G|C|B|P|M|A)|(?(bg)(?P<bgc>rr|oo|yy|gg|cc|bb|pp|mm|aa|r|o|y|g|c|b|p|m|a|k|w|R|O|Y|G|C|B|P|M|A)))|(?P<eq>=)|(?P<hs>#))(?(eq)(?P<rgb>\d{0,3},?\d{0,3},?\d{0,3})|(?(hs)(?P<hex>[0-9a-fA-F]{0,6})))(?(sqb)(?:\s*\])|(?(par)(?:\s*\))|/?))"
    }


# Color definitions
class _Color:
    _ENDC = '\033[0m'

    class _Foreground:

        # COLOR NAME       # CODE  # ANSI COLOR      # TRUE COLOR
        DARK_RED          = ('rr', '\033[38;5;88m',  '\033[38;2;130;0;0m')       # ;rr
        DARK_ORANGE       = ('oo', '\033[38;5;130m', '\033[38;2;160;50;0m')      # ;oo
        DARK_YELLOW       = ('yy', '\033[38;5;142m', '\033[38;2;150;120;0m')     # ;yy
        DARK_GREEN        = ('gg', '\033[38;5;22m',  '\033[38;2;0;80;0m')        # ;gg
        DARK_CYAN         = ('cc', '\033[38;5;31m',  '\033[38;2;0;120;130m')     # ;cc
        DARK_BLUE         = ('bb', '\033[38;5;24m',  '\033[38;2;20;50;130m')     # ;bb
        DARK_PURPLE       = ('pp', '\033[38;5;54m',  '\033[38;2;90;0;150m')      # ;pp
        DARK_MAGENTA      = ('mm', '\033[38;5;90m',  '\033[38;2;130;0;100m')     # ;mm

        RED               = ('r',  '\033[38;5;124m', '\033[38;2;180;0;0m')       # ;r
        ORANGE            = ('o',  '\033[38;5;166m', '\033[38;2;200;90;0m')      # ;o
        YELLOW            = ('y',  '\033[38;5;184m', '\033[38;2;190;170;0m')     # ;y
        GREEN             = ('g',  '\033[38;5;34m',  '\033[38;2;0;150;0m')       # ;g
        CYAN              = ('c',  '\033[38;5;39m',  '\033[38;2;0;190;200m')     # ;c
        BLUE              = ('b',  '\033[38;5;27m',  '\033[38;2;0;70;255m')      # ;b
        PURPLE            = ('p',  '\033[38;5;57m',  '\033[38;2;100;0;180m')     # ;p
        MAGENTA           = ('m',  '\033[38;5;127m', '\033[38;2;190;0;150m')     # ;m

        STRONG_RED        = ('R',  '\033[38;5;196m', '\033[38;2;255;0;0m')       # ;R
        STRONG_ORANGE     = ('O',  '\033[38;5;202m', '\033[38;2;255;150;0m')     # ;O
        STRONG_YELLOW     = ('Y',  '\033[38;5;226m', '\033[38;2;255;255;0m')     # ;Y
        STRONG_GREEN      = ('G',  '\033[38;5;82m',  '\033[38;2;0;255;0m')       # ;G
        STRONG_CYAN       = ('C',  '\033[38;5;45m',  '\033[38;2;0;255;255m')     # ;C
        STRONG_BLUE       = ('B',  '\033[38;5;21m',  '\033[38;2;0;20;255m')      # ;B
        STRONG_PURPLE     = ('P',  '\033[38;5;93m',  '\033[38;2;150;0;255m')     # ;P
        STRONG_MAGENTA    = ('M',  '\033[38;5;200m', '\033[38;2;225;0;225m')     # ;M

        BLACK             = ('k',  '\033[38;5;232m', '\033[38;2;0;0;0m')         # ;k
        DARK_GRAY         = ('A',  '\033[38;5;238m', '\033[38;2;70;70;70m')      # ;aa
        GRAY              = ('a',  '\033[38;5;244m', '\033[38;2;130;130;130m')   # ;a
        LIGHT_GRAY        = ('aa', '\033[38;5;250m', '\033[38;2;185;185;185m')   # ;A
        WHITE             = ('w',  '\033[1;37m',     '\033[38;2;255;255;255m')   # ;w

        maps = {
            'R': 'STRONG_RED',
            'O': 'STRONG_ORANGE',
            'Y': 'STRONG_YELLOW',
            'G': 'STRONG_GREEN',
            'C': 'STRONG_CYAN',
            'B': 'STRONG_BLUE',
            'P': 'STRONG_PURPLE',
            'M': 'STRONG_MAGENTA',
            'r': 'RED',
            'o': 'ORANGE',
            'y': 'YELLOW',
            'g': 'GREEN',
            'c': 'CYAN',
            'b': 'BLUE',
            'p': 'PURPLE',
            'm': 'MAGENTA',
            'rr': 'DARK_RED',
            'oo': 'DARK_ORANGE',
            'yy': 'DARK_YELLOW',
            'gg': 'DARK_GREEN',
            'cc': 'DARK_CYAN',
            'bb': 'DARK_BLUE',
            'pp': 'DARK_PURPLE',
            'mm': 'DARK_MAGENTA',
            'k': 'BLACK',
            'A': 'LIGHT_GRAY',
            'a': 'GRAY',
            'aa': 'DARK_GRAY',
            'w': 'WHITE'
        }

    class _Background:

        DARK_RED          = ('rr', '\033[48;5;88m',  '\033[48;2;130;0;0m')      # :rr
        DARK_ORANGE       = ('oo', '\033[48;5;130m', '\033[48;2;160;50;0m')     # :oo
        DARK_YELLOW       = ('yy', '\033[48;5;142m', '\033[48;2;150;120;0m')    # :yy
        DARK_GREEN        = ('gg', '\033[48;5;22m',  '\033[48;2;0;80;0m')       # :gg
        DARK_CYAN         = ('cc', '\033[48;5;31m',  '\033[48;2;0;120;130m')    # :cc
        DARK_BLUE         = ('bb', '\033[48;5;19m',  '\033[48;2;20;50;130m')    # :bb
        DARK_PURPLE       = ('pp', '\033[48;5;54m',  '\033[48;2;90;0;150m')     # :pp
        DARK_MAGENTA      = ('mm', '\033[48;5;127m', '\033[48;2;130;0;100m')    # :mm

        RED               = ('r',  '\033[48;5;124m', '\033[48;2;180;0;0m')      # :r
        ORANGE            = ('o',  '\033[48;5;166m', '\033[48;2;200;90;0m')     # :o
        YELLOW            = ('y',  '\033[48;5;184m', '\033[48;2;190;170;0m')    # :y
        GREEN             = ('g',  '\033[48;5;34m',  '\033[48;2;0;150;0m')      # :g
        CYAN              = ('c',  '\033[48;5;45m',  '\033[48;2;0;190;200m')    # :c
        BLUE              = ('b',  '\033[48;5;27m',  '\033[48;2;0;70;255m')     # :b
        PURPLE            = ('p',  '\033[48;5;93m',  '\033[48;2;100;0;180m')    # :p
        MAGENTA           = ('m',  '\033[48;5;165m', '\033[48;2;190;0;150m')    # :m

        STRONG_RED        = ('R',  '\033[48;5;196m', '\033[48;2;255;0;0m')      # :R
        STRONG_ORANGE     = ('O',  '\033[48;5;202m', '\033[48;2;255;150;0m')    # :O
        STRONG_YELLOW     = ('Y',  '\033[48;5;226m', '\033[48;2;255;255;0m')    # :Y
        STRONG_GREEN      = ('G',  '\033[48;5;82m',  '\033[48;2;0;255;0m')      # :G
        STRONG_CYAN       = ('C',  '\033[48;5;45m',  '\033[48;2;0;255;255m')    # :C
        STRONG_BLUE       = ('B',  '\033[48;5;21m',  '\033[48;2;0;20;255m')     # :B
        STRONG_PURPLE     = ('P',  '\033[48;5;128m', '\033[48;2;150;0;255m')    # :P
        STRONG_MAGENTA    = ('M',  '\033[48;5;200m', '\033[48;2;225;0;225m')    # :M

        BLACK             = ('k',  '\033[48;5;232m', '\033[48;2;0;0;0m')        # :k
        DARK_GRAY         = ('A',  '\033[48;5;238m', '\033[48;2;70;70;70m')     # :aa
        GRAY              = ('a',  '\033[48;5;244m', '\033[48;2;130;130;130m')  # :a
        LIGHT_GRAY        = ('aa', '\033[48;5;250m', '\033[48;2;185;185;185m')  # :A
        WHITE             = ('w',  '\033[48;5;255m', '\033[48;2;255;255;255m')  # :w

        maps = {
            'R': 'STRONG_RED',
            'O': 'STRONG_ORANGE',
            'Y': 'STRONG_YELLOW',
            'G': 'STRONG_GREEN',
            'C': 'STRONG_CYAN',
            'B': 'STRONG_BLUE',
            'P': 'STRONG_PURPLE',
            'M': 'STRONG_MAGENTA',
            'r': 'RED',
            'o': 'ORANGE',
            'y': 'YELLOW',
            'g': 'GREEN',
            'c': 'CYAN',
            'b': 'BLUE',
            'p': 'PURPLE',
            'm': 'MAGENTA',
            'rr': 'DARK_RED',
            'oo': 'DARK_ORANGE',
            'yy': 'DARK_YELLOW',
            'gg': 'DARK_GREEN',
            'cc': 'DARK_CYAN',
            'bb': 'DARK_BLUE',
            'pp': 'DARK_PURPLE',
            'mm': 'DARK_MAGENTA',
            'k': 'BLACK',
            'A': 'LIGHT_GRAY',
            'a': 'GRAY',
            'aa': 'DARK_GRAY',
            'w': 'WHITE',
        }

# Exception class for printing custom errors
class ColorparseException(Exception):
    pass


# Each time there is a change in the color codes, reconstruct regex
def _construct_regex():
    # Usual parts of the regex:
    init_enc = r"((?:(?P<sqb>\[(?=[^\]\(\)\\]*?\]))\s*|(?P<par>\((?=[^\)\[\]\\]*?\)))\s*)|/)?"
    init_codes = r"(?:\\)?((?P<fg>;)|(?P<bg>:))(;|:|"

    # Here would go: codes(fg_colors, bg_colors)

    end_codes = r"|(?P<eq>=)|(?P<hs>#))(?(eq)(?P<rgb>\d{0,3},?\d{0,3},?\d{0,3})|(?(hs)(?P<hex>[0-9a-fA-F]{0,6})))"
    end_enc = r"(?(sqb)(?:\s*\])|(?(par)(?:\s*\))|/?))"

    # The changing part of the regex, depending on color code definitions
    codes = lambda f, b: rf"(?(fg)(?:{'|'.join(f)})|(?(bg)(?:{'|'.join(b)})))"

    # Get each color code (from each attribute) of the class `x` in a list
    def get_colors(x):
        return [getattr(x, c)[0] for c in dir(x) if not c.startswith('__')]

    # Get both color codes and sort them by length in reverse (longest to smallest)
    fg_colors = sorted(get_colors(_Color._Foreground), key=len, reverse=True)
    bg_colors = sorted(get_colors(_Color._Background), key=len, reverse=True)

    # Join all the regex, and replace the old one
    _Config.data['regex'] = f"{init_enc}{init_codes}{codes(fg_colors, bg_colors)}{end_codes}{end_enc}"


# Keep number between min and max
def _clamp(num, n_min, n_max):
    return max(n_min, min(n_max, num))


# Stick number between the ranges of 0 to 255
def _rgb_clamp(num):
    if type(num) == str:
        num = int(num) if num != '' else 0

    return str(max(0, min(255, num)))


# Transform hex color to rgb color
def _hex_to_rgb(string):
    string = string + '0'*(6 - len(string))

    r = int(string[:2], 16)
    g = int(string[2:4], 16)
    b = int(string[4:], 16)

    if _Config.flags['auto_fix_bad_rgb']:
        return map(_rgb_clamp, (r, g, b))

    else:
        return (r, g, b)

# Clean string to return rgb values from comma separated input
def _str_to_rgb(string):
    r, g, b = (string + ','*(2 - string.count(','))).split(',')

    if _Config.flags['auto_fix_bad_rgb']:
        return map(_rgb_clamp, (r, g, b))

    else:
        return (r, g, b)


# Remove extra code components (e.g. brackets)
def _strip(code):
    return re.sub(r'\[|\]|\(|\)| ', '', code)


# Replace special characters if "-I" or "--ignore-special" flag is set
def _try_ignore_special(string):
    if not _Config.flags['ignore_special']:
        return string

    chars = 'nabfrvt'

    def repl(matchobj):
        special = { c: rf'\{c}' for c in chars}

        match = matchobj[0]

        double = match[:-2] + special[match[-1]]
        single = match[1:]

        return double if len(match) % 2 == 0 else single

    return re.sub(rf'\\+[{chars}]', repl, string)


# Replace individual matches of each code into the ansi escape sequence
def _color_repl(match):
    gm = match[0] # Global match (0th match)

    # If color code was escaped, return without the backslash
    if '\\' in gm: return gm.replace('\\', '')

    # If the code is of type "end color", return ENDC
    if ';:' in gm or ':;' in gm: return _Color._ENDC

    # If it's a special rgb color code
    if '#' in gm or '=' in gm:
        if not _Config.flags['true_color']:
            return gm

        elif '#' in gm:
            r, g, b = _hex_to_rgb(match['hex'])

        else:
            r, g, b = _str_to_rgb(match['rgb'])

        if ';' in gm: t = "38"
        else: t = "48"

        return f"\033[{t};2;{r};{g};{b}m"


    def update_maps(color_class):
        maps = dict()

        for color_name in dir(color_class):
            if not color_name.startswith('__') and not color_name == "maps":
                maps[getattr(color_class, color_name)[0]] = color_name

        color_class.maps = maps

    # Check if color definitions were changed, to update
    # the 'maps' attribute of both color types
    if _Config.flags['color_defs_were_changed']:
        update_maps(_Color._Foreground)
        update_maps(_Color._Background)

        _Config.flags['color_defs_were_changed'] = False

    index = 2 if _Config.flags['true_color'] else 1

    # If it's a background-type color code
    if ':' in gm:
        return getattr(_Color._Background, _Color._Background.maps[match['bgc']])[index]

    # If it's foreground-type color code
    if ';' in gm:
        return getattr(_Color._Foreground, _Color._Foreground.maps[match['fgc']])[index]

    return gm


# Search and replace matched color codes
def _match_color_codes(string):
    # Before actually replacing each code by an ansi color,
    # search and fix special codes (i.e. ';;' and '::')

    # Return int to check if color code is type ';:', ';;', etc.
    # or otherwise
    def end_type(code):
        if ';:' in code or ':;' in code:
            return 0
        elif ';;' in code:
            return 1
        elif '::' in code:
            return 2
        else:
            return -1

    # Similarly, check if color code is either forground, background
    # or neither
    def color_type(code):
        if ';' in code and end_type(code) < 0:
            return 1
        elif ':' in code and end_type(code) < 0:
            return 2
        else:
            return -1

    # Do not match backslashes
    matches = [m for m in re.finditer(_Config.data['regex'], string) if '\\' not in m[0]]

    prev_fg = None
    prev_bg = None

    # Iterate through all matches
    for index, match in enumerate(matches):
        code = match[0]

        curr_fg = code if color_type(code) == 1 else prev_fg
        curr_bg = code if color_type(code) == 2 else prev_bg

        prev_fg = curr_fg
        prev_bg = curr_bg

        # If ';;' or '::' are found
        if end_type(code) > 0:

            # If ending foreground color
            if end_type(code) == 1:
                matches[index] = ["[;:]"]

                if curr_bg is not None:
                    string = string.replace(code, f"[;:]{curr_bg}", 1)
                    matches.insert(index+1, [curr_bg])

                else:
                    string = string.replace(code, "[;:]", 1)

                prev_fg = None
                curr_fg = None

            # Else, ending the background color
            else:
                matches[index] = ["[;:]"]

                if curr_fg is not None:
                    string = string.replace(code, f"[;:]{curr_fg}", 1)
                    matches.insert(index+1, [curr_fg])

                else:
                    string = string.replace(code, "[;:]", 1)

                prev_bg = None
                curr_bg = None

    # Replace color codes with the respective ansi escape sequences
    return re.sub(_Config.data['regex'], _color_repl, string)


# Prints a pre made list of color codes
def codes():
    """Prints a list of all the color codes available.
    It also displays what the colors look as
    background type and foreground type.
    """

    help_string = """
 [background] [foreground] [code]   [name]
   "(;w):(;a)<code>(;:)"   "(;w);(;a)<code>(;:)"\n
   [:rr]        [;:]     [;rr]red     [;:]     [;w]rr[;:]   (DARK_RED)
   [:oo]        [;:]     [;oo]orange  [;:]     [;w]oo[;:]   (DARK_ORANGE)
   [:yy]        [;:]     [;yy]yellow  [;:]     [;w]yy[;:]   (DARK_YELLOW)
   [:gg]        [;:]     [;gg]green   [;:]     [;w]gg[;:]   (DARK_GREEN)
   [:cc]        [;:]     [;cc]cyan    [;:]     [;w]cc[;:]   (DARK_CYAN)
   [:bb]        [;:]     [;bb]blue    [;:]     [;w]bb[;:]   (DARK_BLUE)
   [:pp]        [;:]     [;pp]purple  [;:]     [;w]pp[;:]   (DARK_PURPLE)
   [:mm]        [;:]     [;mm]magenta [;:]     [;w]mm[;:]   (DARK_MAGENTA)

   [:r ]        [;:]     [;r ]red     [;:]     [;w]r [;:]   (RED)
   [:o ]        [;:]     [;o ]orange  [;:]     [;w]o [;:]   (ORANGE)
   [:y ]        [;:]     [;y ]yellow  [;:]     [;w]y [;:]   (YELLOW)
   [:g ]        [;:]     [;g ]green   [;:]     [;w]g [;:]   (GREEN)
   [:c ]        [;:]     [;c ]cyan    [;:]     [;w]c [;:]   (CYAN)
   [:b ]        [;:]     [;b ]blue    [;:]     [;w]b [;:]   (BLUE)
   [:p ]        [;:]     [;p ]purple  [;:]     [;w]p [;:]   (PURPLE)
   [:m ]        [;:]     [;m ]magenta [;:]     [;w]m [;:]   (MAGENTA)

   [:R ]        [;:]     [;R ]red     [;:]     [;w]R [;:]   (STRONG_RED)
   [:O ]        [;:]     [;O ]orange  [;:]     [;w]O [;:]   (STRONG_ORANGE)
   [:Y ]        [;:]     [;Y ]yellow  [;:]     [;w]Y [;:]   (STRONG_YELLOW)
   [:G ]        [;:]     [;G ]green   [;:]     [;w]G [;:]   (STRONG_GREEN)
   [:C ]        [;:]     [;C ]cyan    [;:]     [;w]C [;:]   (STRONG_CYAN)
   [:B ]        [;:]     [;B ]blue    [;:]     [;w]B [;:]   (STRONG_BLUE)
   [:P ]        [;:]     [;P ]purple  [;:]     [;w]P [;:]   (STRONG_PURPLE)
   [:M ]        [;:]     [;M ]magenta [;:]     [;w]M [;:]   (STRONG_MAGENTA)

   [:k ]        [;:]    [;k ]black     [;:]    [;w]k [;:]   (BLACK)
   [:aa]        [;:]    [;aa]dark gray [;:]    [;w]aa[;:]   (DARK_GRAY)
   [:a ]        [;:]    [;a ]gray      [;:]    [;w]a [;:]   (GRAY)
   [:A ]        [;:]    [;A ]light gray[;:]    [;w]A [;:]   (LIGHT_GRAY)
   [:w ]        [;:]    [;w ]white     [;:]    [;w]w [;:]   (WHITE)


   color ending:

               end color  [;w]\;: | \:;[;:] (ENDC)
               end fg color  [;w]\;;[;:]
               end bg color  [;w]\::[;:]

"""

    extra_string = """   custom colors:

                 rgb         [;w]\;=[;:]    (RGB)
                 [from 0 to 255, comma separated]

                 hex         [;w]\;#[;:]    (HEXADECIMAL)
                 [from 000000 to ffffff]
    """

    paint(help_string, print=True)

    if _Config.flags['true_color']:
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
    ec = _Color._ENDC
    value = list(value)

    # Get the options' arguments
    _print = options.get('print', _Config.paint['print'])
    _ret = options.get('ret', _Config.paint['ret'])
    _overflow = options.get('overflow', _Config.paint['overflow'])
    _sep = _match_color_codes(options.get('sep', _Config.paint['sep']))
    _end = _match_color_codes(options.get('end', _Config.paint['end']))
    _file = options.get('file', _Config.paint['file'])
    _flush = options.get('flush', _Config.paint['flush'])

    # If overflow is true, then color the strings as one
    if _overflow:
        result = _match_color_codes(_sep.join(map(str, value)))

        if _print:
            print(result, end=(_end + ec), file=_file, flush=_flush)

    # Else, color one by one and the join them
    else:
        result = (ec + _sep).join(map(_match_color_codes, map(str, value)))

        if _print:
            print(result, end=(ec + _end + ec), file=_file, flush=_flush)

    # Return the result
    if _ret:
        return result + ec


# Parses arguments from the terminal
def _arg_parser():
    # Initiate argument parser
    parser = argparse.ArgumentParser(prog='colorparse')

    # Arguments
    parser.add_argument('string',
                        help='one or more input strings.',
                        nargs='*',
                        default=[])

    parser.add_argument('-c', '--codes',
                        help='show the available color codes and exit.',
                        action='store_true')

    parser.add_argument('-v', '--version',
                        help='show the current version of this module and\
                              exit.',
                        action='version', version=f'%(prog)s {__version__}')

    parser.add_argument('-t', '--true-color',
                        help='use of RGB values for the ANSI escape sequences.\
                              Allowes customized foreground color codes and a\
                              more accurate color set (warning: having this\
                              option won\'t work on all terminals as they do\
                              not all support true color).',
                        action='store_true')

    parser.add_argument('-s', '--sep',
                        help='specify what string to use, to separate string\
                              arguments (default is \' \').',
                        default=_Config.paint['sep'])

    parser.add_argument('-e', '--end',
                        help='specify what string to use at the end of the\
                              printed string (default is \'\\n\')',
                        default=_Config.paint['end'])

    parser.add_argument('-O', '--overflow',
                        help='make colors overflow to other strings if a color\
                              code is not finished.',
                        action='store_true')

    parser.add_argument('-I', '--ignore-special',
                        help='tell the parser to ignore special characters\
                              like (new line, tab, etc.).',
                        action='store_true')

    parser.add_argument('-S', '--strip',
                        help='specify which leading and trailing\
                              characters to remove from input file(s)\
                              (by default removes whitespace if the flag is\
                              used).',
                        nargs='?',
                        const=None,
                        default='')

    parser.add_argument('-p', '--position',
                        help='place all strings after the nth input file.',
                        nargs='?',
                        const=0,
                        default=0,
                        type=int)

    parser.add_argument('-i', '--input-file',
                        help='specify one or more files to read the color\
                              coded strings from. If a file doesn\'t exist, an\
                              error will be raised. It must be used after any \
                              string argument.',
                        nargs='*',
                        type=argparse.FileType('r'),
                        default=[])

    parser.add_argument('-o', '--output-file',
                        help='specify an output file to append the resulting\
                              string (default is sys.stdout).',
                        nargs='?',
                        type=argparse.FileType('a'),
                        const=_Config.paint['file'],
                        default=_Config.paint['file'])

    # Return the arguments to "_main"
    return parser, parser.parse_args()


def _main():
    # Get arguments
    parser, args = _arg_parser()

    # Set base values
    _Config.flags['true_color'] = args.true_color
    _Config.flags['ignore_special'] = args.ignore_special

    all_strings = []
    n_strings = len(args.string)
    n_files = len(args.input_file)

    # Exit if 'codes' option is used, or there is no input
    if args.codes:
        codes()
        sys.exit(0)

    if n_strings == 0 and n_files == 0:
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
    _paint = partial(paint, print=True, overflow=args.overflow,
                     sep=args.sep, end=args.end, file=args.output_file)
    for v in all_strings:
        _paint = partial(_paint, v)

    # Print
    _paint()


if __name__ == '__main__':
    _main()


if sys.platform[:3] == 'win':
        os.system('color')
