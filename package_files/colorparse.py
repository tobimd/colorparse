#!/usr/bin/python3
import os
import sys
import re
import argparse


__version__ = '1.0.0'


class _Defaults:
    paint = {
        'print': True,
        'ret': True,
        'overflow': False,
        'sep': ' ',
        'end': '\n',
        'file': sys.stdout,
        'flush': False,
    }

    _color_list = {
        'rr': 'DARK_RED',
        'oo': 'DARK_ORANGE',
        'yy': 'DARK_YELLOW',
        'gg': 'DARK_GREEN',
        'cc': 'DARK_CYAN',
        'bb': 'DARK_BLUE',
        'pp': 'DARK_PURPLE',
        'mm': 'DARK_MAGENTA',
        'r':  'RED',
        'o':  'ORANGE',
        'y':  'YELLOW',
        'g':  'GREEN',
        'c':  'CYAN',
        'b':  'BLUE',
        'p':  'PURPLE',
        'm':  'MAGENTA',
        'R':  'STRONG_RED',
        'O':  'STRONG_ORANGE',
        'Y':  'STRONG_YELLOW',
        'G':  'STRONG_GREEN',
        'C':  'STRONG_CYAN',
        'B':  'STRONG_BLUE',
        'P':  'STRONG_PURPLE',
        'M':  'STRONG_MAGENTA',
        'k':  'BLACK',
        'aa': 'DARK_GRAY',
        'a':  'GRAY',
        'A':  'LIGHT_GRAY',
        'w':  'WHITE',
    }


class Color:
    @classmethod
    def __init__(cls):
        cls.ENDC = '\033[0m'  # ;: | :;

        cls.foreground = _Foreground(False)
        cls.background = _Background()
        cls._true_color(False)

    @classmethod
    def _true_color(cls, value):        
        # set global value for true color
        cls._true_color_active = value
        cls.foreground = _Foreground(value)


class _Foreground:
    def __init__(self, true_color):
	    # if the stdout does support rgb color escape sequences
        if true_color:
            self.DARK_RED        = '\033[38;2;130;0;0m'       # ;R
            self.DARK_ORANGE     = '\033[38;2;160;50;0m'      # ;O
            self.DARK_YELLOW     = '\033[38;2;150;120;0m'     # ;Y
            self.DARK_GREEN      = '\033[38;2;0;80;0m'        # ;G
            self.DARK_CYAN       = '\033[38;2;0;120;130m'     # ;C
            self.DARK_BLUE       = '\033[38;2;20;50;130m'     # ;B
            self.DARK_PURPLE     = '\033[38;2;90;0;150m'      # ;P
            self.DARK_MAGENTA    = '\033[38;2;130;0;100m'     # ;M

            self.RED             = '\033[38;2;180;0;0m'       # ;r
            self.ORANGE          = '\033[38;2;200;90;0m'      # ;o
            self.YELLOW          = '\033[38;2;190;170;0m'     # ;y
            self.GREEN           = '\033[38;2;0;150;0m'       # ;g
            self.CYAN            = '\033[38;2;0;190;200m'     # ;c
            self.BLUE            = '\033[38;2;0;70;255m'      # ;b
            self.PURPLE          = '\033[38;2;100;0;180m'     # ;p
            self.MAGENTA         = '\033[38;2;190;0;150m'     # ;m

            self.STRONG_RED      = '\033[38;2;255;0;0m'       # ;rr
            self.STRONG_ORANGE   = '\033[38;2;255;150;0m'     # ;oo
            self.STRONG_YELLOW   = '\033[38;2;255;255;0m'     # ;yy
            self.STRONG_GREEN    = '\033[38;2;0;255;0m'       # ;gg
            self.STRONG_CYAN     = '\033[38;2;0;255;255m'     # ;cc
            self.STRONG_BLUE     = '\033[38;2;0;20;255m'      # ;bb
            self.STRONG_PURPLE   = '\033[38;2;150;0;255m'     # ;pp
            self.STRONG_MAGENTA  = '\033[38;2;225;0;225m'     # ;mm

            self.BLACK           = '\033[38;2;0;0;0m'         # ;k
            self.DARK_GRAY       = '\033[38;2;70;70;70m'      # ;A
            self.GRAY            = '\033[38;2;130;130;130m'   # ;a
            self.LIGHT_GRAY      = '\033[38;2;185;185;185m'   # ;aa
            self.WHITE           = '\033[38;2;255;255;255m'   # ;w

	    # if the stdout does *not* support rgb color escape sequences
        else:
            self.DARK_RED        = '\033[38;5;88m'   # ;R
            self.DARK_ORANGE     = '\033[38;5;130m'  # ;O
            self.DARK_YELLOW     = '\033[38;5;142m'  # ;Y
            self.DARK_GREEN      = '\033[38;5;22m'   # ;G
            self.DARK_CYAN       = '\033[38;5;31m'   # ;C
            self.DARK_BLUE       = '\033[38;5;24m'   # ;B
            self.DARK_PURPLE     = '\033[38;5;54m'   # ;P
            self.DARK_MAGENTA    = '\033[38;5;90m'   # ;M

            self.RED             = '\033[38;5;124m'  # ;r
            self.ORANGE          = '\033[38;5;166m'  # ;o
            self.YELLOW          = '\033[38;5;184m'  # ;y
            self.GREEN           = '\033[38;5;34m'   # ;g
            self.CYAN            = '\033[38;5;39m'   # ;c
            self.BLUE            = '\033[38;5;27m'   # ;b
            self.PURPLE          = '\033[38;5;57m'   # ;p
            self.MAGENTA         = '\033[38;5;127m'  # ;m

            self.STRONG_RED      = '\033[38;5;196m'    # ;rr
            self.STRONG_ORANGE   = '\033[38;5;202m'  # ;oo
            self.STRONG_YELLOW   = '\033[38;5;226m'   # ;yy
            self.STRONG_GREEN    = '\033[38;5;82m'   # ;gg                
            self.STRONG_CYAN     = '\033[38;5;45m'   # ;cc
            self.STRONG_BLUE     = '\033[38;5;21m'   # ;bb
            self.STRONG_PURPLE   = '\033[38;5;93m'   # ;pp
            self.STRONG_MAGENTA  = '\033[38;5;200m'   # ;mm

            self.BLACK           = '\033[38;5;232m'    # ;k
            self.DARK_GRAY       = '\033[38;5;238m'  # ;A
            self.GRAY            = '\033[38;5;244m'  # ;a
            self.LIGHT_GRAY      = '\033[38;5;250m'  # ;aa
            self.WHITE           = '\033[38;5;256m'   # ;w


class _Background:
    def __init__(self):
        self.DARK_RED        = '\033[48;5;88m'   # :R
        self.DARK_ORANGE     = '\033[48;5;130m'  # :O
        self.DARK_YELLOW     = '\033[48;5;142m'  # :Y
        self.DARK_GREEN      = '\033[48;5;22m'   # :G
        self.DARK_CYAN       = '\033[48;5;31m'   # :C
        self.DARK_BLUE       = '\033[48;5;19m'    # :B
        self.DARK_PURPLE     = '\033[48;5;54m'   # :P
        self.DARK_MAGENTA    = '\033[48;5;127m'  # :M

        self.RED             = '\033[48;5;124m'  # :r
        self.ORANGE          = '\033[48;5;166m'  # :o
        self.YELLOW          = '\033[48;5;184m'  # :y
        self.GREEN           = '\033[48;5;34m'   # :g
        self.CYAN            = '\033[48;5;45m'   # :c
        self.BLUE            = '\033[48;5;27m'   # :b
        self.PURPLE          = '\033[48;5;93m'   # :p
        self.MAGENTA         = '\033[48;5;165m'  # :m

        self.STRONG_RED      = '\033[48;5;196m'    # :rr
        self.STRONG_ORANGE   = '\033[48;5;202m'  # :oo
        self.STRONG_YELLOW   = '\033[48;5;226m'   # :yy
        self.STRONG_GREEN    = '\033[48;5;82m'   # :gg
        self.STRONG_CYAN     = '\033[48;5;45m'   # :cc
        self.STRONG_BLUE     = '\033[48;5;21m'   # :bb
        self.STRONG_PURPLE   = '\033[48;5;128m'   # :pp
        self.STRONG_MAGENTA  = '\033[48;5;200m'   # :mm

        self.BLACK           = '\033[48;5;232m'    # :k
        self.DARK_GRAY       = '\033[48;5;238m'  # :A
        self.GRAY            = '\033[48;5;244m'  # :a
        self.LIGHT_GRAY      = '\033[48;5;250m'  # :aa
        self.WHITE           = '\033[48;5;255m'   # :w


def _clamp(number):
    if number == '':
        number = 0

    if type(number) == str:
        number = int(number)

    if number < 0:
        number = 0
    
    if number > 255:
        number = 255
    
    return str(number)


def _hex_to_rgb(string):
    r = int(string[:2], 16)
    g = int(string[2:4], 16)
    b = int(string[4:], 16)

    return map(_clamp, (r, g, b))


def _color_repl(matchobj):
    # if it was escaped, then return without the backslash
    if '\\' in matchobj[0]:
        return matchobj[0].replace('\\', '')

    # get the string of the matched color code and remove unwanted characters
    string = re.sub(r'\[|\]|\(|\)|/| ', '', matchobj[0])

    # if matched string is ':;' or ';:', then return ENDC (end color)
    if string == ':;' or string == ';:':
        return Color.ENDC

    col_type, col_val = string[0], string[1:]

    # custom color code
    if '#' in col_val or '=' in col_val:
        mode, val = col_val[0], col_val[1:]

        fix = ((val + ',' * (2 - val.count(','))).split(',') if mode == '='
                else _hex_to_rgb(val + '0' * (6 - len(val))))
        r, g, b = map(_clamp, fix)

        return f'\033[38;2;{r};{g};{b}m'

    # foreground color code
    elif col_type == ';':
        return getattr(Color.foreground, _Defaults._color_list[col_val])

    # background color code
    else:
        return getattr(Color.background, _Defaults._color_list[col_val])


def _color_format(string):
    # a failed attempt to make this a less convoluted regex
    start = r'((\[(?=[^/\)]+\]))\s*|(\((?=[^/\]]+\)))\s*|/)?('
    prefix = r'\\?(?:(;)|(:))'
    color = r'(;|:|[ROYGCBPMkAw]|([roygcbpma])\8?'
    rgb = r'|(?(5)(= ?\d{0,3}(?:\s?,\s?\d{0,3})?(?:\s?,\s?\d{0,3})?'
    hex_rgb = r'|# ?[0-9A-Fa-f]{0,6})|\5)'
    suffix = r'))(/|(?(2)\s*\]|(?(3)\s*\))))?'

    # set regex to use (with true color, use custom color codes)
    if Color._true_color_active:
        regex = f'{start}{prefix}{color}{rgb}{hex_rgb}{suffix}'

    else:
        regex = f'{start}{prefix}{color}{suffix}'
    
    # search for ';;'|'::' and replace them with end color + prev color
    all_matches = list(re.finditer(regex, string))
    for i, mo in enumerate(all_matches):
        if (';;' in mo[0] or '::' in mo[0]) and '\\' not in mo[0]:
            code = mo[0]
            inv = ':' if ';;' in code else ';'
            found = False

            for _mo in all_matches[i - 1::-1]:
                if ';:' in _mo[0] or ':;' in _mo[0]:
                    continue

                is_color = (re.search(r'(?<!\\)' + inv + r'(\w|#|=)', _mo[0]) 
                            is not None)
                if is_color:
                    string = string.replace(code, '[;:]' + _mo[0], 1)
                    found = True
                    all_matches.insert(i + 1, _mo)

            if not found:
                string = string.replace(code, '[;:]', 1)

            all_matches[i] = ['[;:]']

    return re.sub(regex, _color_repl, string)


def _fix_special(matchobj):
    special = {'n': '\n', 'a': '\a', 'b': '\b', 
               'f': '\f', 'r': '\r', 'v': '\v',
               't': '\t',}

    string = matchobj[0]
    
    # Windows does not escape characters before user input
    if sys.platform[:3] == 'win':
        is_not_escaped = len(string) % 2 != 0

    # Linux, or at least urxvt terminal, does
    else:
        is_not_escaped = len(string) % 2 == 0


    if is_not_escaped:
        return string[:-2] + special[string[-1]]

    return string[1:]


def paint(*strings, **options):
    """paint(strings, ..., print=True, ret=True, overflow=False, sep=' ',
             end='\n', file=sys.stdout, flush=false) -> string

    Returns a string that will have color codes converted to real ANSI
    color escape sequences (if 'print' is False, then the string won't be
    printed and the arguments 'end', 'file' and 'flush' won't be considered
    whatever their values may be. The returned and/or printed string will
    always end all color codes.

    The overflow argument will allow any unfinished color to pass through
    to the other strings if it's value is True. By default it's False, which
    means that all the color will be finished at the end of each string.

    """
    endc = '\033[0m'

    # get the options' arguments
    _print = options.get('print', _Defaults.paint['print'])
    _ret = options.get('ret', _Defaults.paint['ret'])
    _overflow = options.get('overflow', _Defaults.paint['overflow'])
    _sep = options.get('sep', _Defaults.paint['sep'])
    _end = options.get('end', _Defaults.paint['end'])
    _file = options.get('file', _Defaults.paint['file'])
    _flush = options.get('flush', _Defaults.paint['flush'])

    # if overflow is true, then color the strings as one
    if _overflow:
        result = _color_format(_sep.join(strings)) + endc
    
    # else, colors one by one and the join them
    else:        
        result = (endc + _sep).join(map(_color_format, strings)) + endc

    # if out is True, then print
    if _print:
        print(result, end=_end, file=_file, flush=_flush)
    
    if _ret:
        return result


def codes():
    """Prints a list of all the color codes available. It shows the
    background, foreground, code and the name of each code.

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

    if Color._true_color_active:
        paint(extra_string, print=True)


def change_defaults(fn, **kwargs):
    """change_defaults(fn, key=value, ...)
    change_defaults(fn, **kwargs)

    Used to set default values permanently for the rest of the program.

    """

    if callable(fn):
        fn = fn.__name__

    for k, v in kwargs.items():
        getattr(_Defaults, fn)[k] = v


def true_color(value=None):
    """true_color(value=None)

    If set to True, the color set will change to rgb ANSI color escape
    sequences, which may not work on some terminals. If no value is given,
    then returns the current state of true color (if it's set to True or not).

    """

    if value is None:
        return Color._true_color_active
    
    Color._true_color(value)


def _arg_parser():
    # initiate argument parser
    parser = argparse.ArgumentParser(prog='colorparse')

    # arguments 
    parser.add_argument('string', 
                        help='a string that may contain color codes',
                        nargs='*',
                        default='')

    parser.add_argument('-i', '--input-file',
                        help='specify an input file or files to recieve the\
                              color coded strings from. If the file doesn\'t\
                              exist an error will be raised.',
                        nargs='*',
                        type=argparse.FileType('r'),
                        default=[])

    parser.add_argument('-o', '--output-file',
                        help='specify an output file to send the resulting\
                              formatted string. If the file exists, it will\
                              be appended to the end of said file.',
                        nargs='?',
                        type=argparse.FileType('a'),
                        default=_Defaults.paint['file'])

    parser.add_argument('-O', '--overflow',
                        help='make color codes overflow to other strings if\
                              the previous one has not ended the color code.',
                        action='store_true')

    parser.add_argument('-s', '--sep',
                        help='specify what to use to separate string\
                              arguments.',
                        default=_Defaults.paint['sep'])

    parser.add_argument('-e', '--end',
                        help='specify what to use at the end of the resulting\
                              formatted string',
                        default=_Defaults.paint['end'])

    parser.add_argument('-t', '--true-color',
                        help='use of rgb values for the color escape\
                              sequences, allowing customized foreground color\
                              codes and having the color set be more accurate\
                              (warning: having this option won\'t work on all\
                              terminals as they do not all have true color).',
                        action='store_true')

    parser.add_argument('-r', '--read-special',
                        help='tell the parser to read special characters read\
                              from the terminal. This doesn\'t apply to input\
                              files, as the parser will always read special\
                              characters from those.',
                        action='store_true')


    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--codes',
                        help='show the available color codes and exit.',
                        action='store_true')

    group.add_argument('-v', '--version',
                        help='show the current version of this module and\
                              exit.',
                        action='version', version=f'%(prog)s {__version__}')

    # return the arguments to "_main"
    return parser, parser.parse_args()


Color()


def _main():
    # get the arguments
    parser, args = _arg_parser()
    
    # set true color to the argument's value
    true_color(args.true_color)

    # if used '-c' or '--codes', the call 'codes' and exit
    if args.codes:
        codes()
        parser.exit()
    
    # if no arguments are given, print usage and exit
    if args.string == '' and len(args.input_file) == 0:
        parser.print_usage()
        parser.exit()        
    
    # use partial to add each string as argument, instead of the whole tuple 
    from functools import partial

    #fix escaped and non-escaped special characters in "sep" and "end"
    if args.read_special and args.sep != _Defaults.paint['sep']:
        args.sep = re.sub(r'\\+[nrtvabf]', _fix_special, args.sep)

    if args.read_special and args.end != _Defaults.paint['end']:
        args.end = re.sub(r'\\+[nrtvabf]', _fix_special, args.end)

    _paint = partial(paint, print=True, overflow=args.overflow,
                     sep=args.sep, end=args.end, file=args.output_file)
    
    # fix escaped and non-escaped special characters in "string"
    strings = list(args.string)
    for string in strings:
        if args.read_special:
            string = re.sub(r'\\+[nrtvabf]', _fix_special, string)

        _paint = partial(_paint, string)

    # read values from input file if there is one
    for f in args.input_file:
        _paint = partial(_paint, f.read())        

    # print the result string
    _paint()


if __name__ == '__main__':
    _main()

else:
    if sys.platform[:3] == 'win':
        os.system('color')
