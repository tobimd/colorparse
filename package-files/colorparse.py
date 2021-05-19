#!/usr/bin/python3
import os
import sys
import re
import argparse

from functools import partial


__version__ = "2.0.0"


# Default values
class _Options:
    _paint = {
        'print': True,
        'ret': True,
        'overflow': False,
        'sep': ' ',
        'end': '\033[0m\n',
        'file': sys.stdout,
        'flush': False,
    }

    _ignore_special = False
    _finish_colors_at_end = True
    _true_color_active = False


# Color definitions
class _Color:
    class _Foreground:

        # COLOR NAME       # CODE  # ANSI COLOR      # TRUE COLOR
        DARK_RED          = ('R',  '\033[38;5;88m',  '\033[38;2;130;0;0m')       # ;R
        DARK_ORANGE       = ('O',  '\033[38;5;130m', '\033[38;2;160;50;0m')      # ;O
        DARK_YELLOW       = ('Y',  '\033[38;5;142m', '\033[38;2;150;120;0m')     # ;Y
        DARK_GREEN        = ('G',  '\033[38;5;22m',  '\033[38;2;0;80;0m')        # ;G
        DARK_CYAN         = ('C',  '\033[38;5;31m',  '\033[38;2;0;120;130m')     # ;C
        DARK_BLUE         = ('B',  '\033[38;5;24m',  '\033[38;2;20;50;130m')     # ;B
        DARK_PURPLE       = ('P',  '\033[38;5;54m',  '\033[38;2;90;0;150m')      # ;P
        DARK_MAGENTA      = ('M',  '\033[38;5;90m',  '\033[38;2;130;0;100m')     # ;M

        RED               = ('r',  '\033[38;5;124m', '\033[38;2;180;0;0m')       # ;r
        ORANGE            = ('o',  '\033[38;5;166m', '\033[38;2;200;90;0m')      # ;o
        YELLOW            = ('y',  '\033[38;5;184m', '\033[38;2;190;170;0m')     # ;y
        GREEN             = ('g',  '\033[38;5;34m',  '\033[38;2;0;150;0m')       # ;g
        CYAN              = ('c',  '\033[38;5;39m',  '\033[38;2;0;190;200m')     # ;c
        BLUE              = ('b',  '\033[38;5;27m',  '\033[38;2;0;70;255m')      # ;b
        PURPLE            = ('p',  '\033[38;5;57m',  '\033[38;2;100;0;180m')     # ;p
        MAGENTA           = ('m',  '\033[38;5;127m', '\033[38;2;190;0;150m')     # ;m

        STRONG_RED        = ('rr', '\033[38;5;196m', '\033[38;2;255;0;0m')       # ;rr
        STRONG_ORANGE     = ('oo', '\033[38;5;202m', '\033[38;2;255;150;0m')     # ;oo
        STRONG_YELLOW     = ('yy', '\033[38;5;226m', '\033[38;2;255;255;0m')     # ;yy
        STRONG_GREEN      = ('gg', '\033[38;5;82m',  '\033[38;2;0;255;0m')       # ;gg
        STRONG_CYAN       = ('cc', '\033[38;5;45m',  '\033[38;2;0;255;255m')     # ;cc
        STRONG_BLUE       = ('bb', '\033[38;5;21m',  '\033[38;2;0;20;255m')      # ;bb
        STRONG_PURPLE     = ('pp', '\033[38;5;93m',  '\033[38;2;150;0;255m')     # ;pp
        STRONG_MAGENTA    = ('mm', '\033[38;5;200m', '\033[38;2;225;0;225m')     # ;mm

        BLACK             = ('k',  '\033[38;5;232m', '\033[38;2;0;0;0m')         # ;k
        DARK_GRAY         = ('A',  '\033[38;5;238m', '\033[38;2;70;70;70m')      # ;A
        GRAY              = ('a',  '\033[38;5;244m', '\033[38;2;130;130;130m')   # ;a
        LIGHT_GRAY        = ('aa', '\033[38;5;250m', '\033[38;2;185;185;185m')   # ;aa
        WHITE             = ('w',  '\033[1;37m',     '\033[38;2;255;255;255m')   # ;w

    class _Background:
        DARK_RED          = ('R',  '\033[48;5;88m')   # :R
        DARK_ORANGE       = ('O',  '\033[48;5;130m')  # :O
        DARK_YELLOW       = ('Y',  '\033[48;5;142m')  # :Y
        DARK_GREEN        = ('G',  '\033[48;5;22m')   # :G
        DARK_CYAN         = ('C',  '\033[48;5;31m')   # :C
        DARK_BLUE         = ('B',  '\033[48;5;19m')   # :B
        DARK_PURPLE       = ('P',  '\033[48;5;54m')   # :P
        DARK_MAGENTA      = ('M',  '\033[48;5;127m')  # :M

        RED               = ('r',  '\033[48;5;124m')  # :r
        ORANGE            = ('o',  '\033[48;5;166m')  # :o
        YELLOW            = ('y',  '\033[48;5;184m')  # :y
        GREEN             = ('g',  '\033[48;5;34m')   # :g
        CYAN              = ('c',  '\033[48;5;45m')   # :c
        BLUE              = ('b',  '\033[48;5;27m')   # :b
        PURPLE            = ('p',  '\033[48;5;93m')   # :p
        MAGENTA           = ('m',  '\033[48;5;165m')  # :m

        STRONG_RED        = ('rr', '\033[48;5;196m')  # :rr
        STRONG_ORANGE     = ('oo', '\033[48;5;202m')  # :oo
        STRONG_YELLOW     = ('yy', '\033[48;5;226m')  # :yy
        STRONG_GREEN      = ('gg', '\033[48;5;82m')   # :gg
        STRONG_CYAN       = ('cc', '\033[48;5;45m')   # :cc
        STRONG_BLUE       = ('bb', '\033[48;5;21m')   # :bb
        STRONG_PURPLE     = ('pp', '\033[48;5;128m')  # :pp
        STRONG_MAGENTA    = ('mm', '\033[48;5;200m')  # :mm

        BLACK             = ('k',  '\033[48;5;232m')  # :k
        DARK_GRAY         = ('A',  '\033[48;5;238m')  # :A
        GRAY              = ('a',  '\033[48;5;244m')  # :a
        LIGHT_GRAY        = ('aa', '\033[48;5;250m')  # :aa
        WHITE             = ('w',  '\033[48;5;255m')  # :w


# Exception class for printing custom errors
class ColorparseException(Exception):
    pass


# Each time there is a change in the color codes, reconstruct regex
def _construct_regex():
    global regex

    # Order each attribute by the size of the code (biggest to smallest)
    def sort(l):
        return sorted(l, key=lambda c: len(c[0]), reverse=True)

    # Get each color attribute of the class `x` in a list
    def get_colors(x):
        return [getattr(x, c) for c in dir(x) if not c.startswith('__')]

    # Get all current attributes in both _Foreground and _Background classes
    fg_colors = sort(get_colors(_Color._Foreground))
    bg_colors = sort(get_colors(_Color._Background))

    #


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
    r = int(string[:2], 16)
    g = int(string[2:4], 16)
    b = int(string[4:], 16)

    return map(_rgb_clamp, (r, g, b))


# Replace special characters if "-I" or "--ignore-special" flag is set
def _try_ignore_special(string):
    if not _Options._ignore_special:
        return string

    chars = 'nabfrvt'

    def repl(matchobj):
        special = { c: rf'\{c}' for c in chars}

        match = matchobj[0]

        double = match[:-2] + special[match[-1]]
        single = match[1:]

        return double if len(match) % 2 == 0 else single

    return re.sub(rf'\\+[{chars}]', repl, string)


# prints a pre made list of color codes
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

    if _Options._true_color_active:
        paint(extra_string, print=True)


# changes default values defined in the class _Defaults
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
        getattr(_Options, fn)[k] = v


# Parses arguments from the terminal
def _arg_parser():
    # initiate argument parser
    parser = argparse.ArgumentParser(prog='colorparse')

    # arguments
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
                        default=_Defaults.paint['sep'])

    parser.add_argument('-e', '--end',
                        help='specify what string to use at the end of the\
                              printed string (default is \'\\n\')',
                        default=_Defaults.paint['end'])

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
                        const=_Defaults.paint['file'],
                        default=_Defaults.paint['file'])

    # return the arguments to "_main"
    return parser, parser.parse_args()


def _main():
    # get arguments
    parser, args = _arg_parser()

    # Set base values
    _Options._true_color_active = args.true_color
    _Options._ignore_special = args.ignore_special

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
