#!/usr/bin/python3
import os
import sys
import re


__version__ = '0.0.0'


class Defaults:
    paint = {
        'out': True,
        'overflow': False,
        'sep': ' ',
        'end': {True: '\033[0m\n', False: ';:'},
        'file': sys.stdout,
        'flush': False,
    }

    _custom_codes = r''

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
        cls.ENDC = '\033[0m'  # ;;

        cls.foreground = _Foreground(False)
        cls.background = _Background()
        cls.true_color(False)

    @classmethod
    def true_color(cls, value=None):
        if value is None:
            return cls._true_color_active
        
        # set global value for true color
        cls._true_color_active = value
        cls.foreground = _Foreground(value)

    @classmethod
    def define_color(cls, code, value):
        pass


class _Foreground:
    def __init__(self, true_color):
	    # if the stdout does support rgb color escape sequences
        if true_color:
            self.DARK_RED        = '\033[38;2;80;0;0m'        # ;R
            self.DARK_ORANGE     = '\033[38;2;80;40;0m'       # ;O
            self.DARK_YELLOW     = '\033[38;2;87;74;0m'       # ;Y
            self.DARK_GREEN      = '\033[38;2;0;80;0m'        # ;G
            self.DARK_CYAN       = '\033[38;2;0;80;110m'      # ;C
            self.DARK_BLUE       = '\033[38;2;0;30;100m'      # ;B
            self.DARK_PURPLE     = '\033[38;2;0;30;100m'      # ;P
            self.DARK_MAGENTA    = '\033[38;2;50;0;70m'       # ;M

            self.RED             = '\033[38;2;150;0;0m'       # ;r
            self.ORANGE          = '\033[38;2;170;70;0m'      # ;o
            self.YELLOW          = '\033[38;2;150;130;0m'     # ;y
            self.GREEN           = '\033[38;2;0;150;0m'       # ;g
            self.CYAN            = '\033[38;2;0;190;200m'     # ;c
            self.BLUE            = '\033[38;2;0;40;180m'      # ;b
            self.CYAN            = '\033[38;2;0;190;200m'     # ;p
            self.MAGENTA         = '\033[38;2;140;0;180m'     # ;m

            self.STRONG_RED      = '\033[38;2;255;0;0m'       # ;rr
            self.STRONG_ORANGE   = '\033[38;2;255;100;0m'     # ;oo
            self.STRONG_YELLOW   = '\033[38;2;255;255;0m'     # ;yy
            self.STRONG_GREEN    = '\033[38;2;80;255;15m'     # ;gg
            self.STRONG_CYAN     = '\033[38;2;0;255;255m'     # ;cc
            self.STRONG_BLUE     = '\033[38;2;0;20;255m'      # ;bb
            self.STRONG_CYAN     = '\033[38;2;0;255;255m'     # ;pp
            self.STRONG_MAGENTA  = '\033[38;2;200;0;255m'     # ;mm

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
            self.DARK_BLUE       = '\033[38;5;17m'   # ;B
            self.DARK_PURPLE     = '\033[38;5;53m'   # ;P
            self.DARK_MAGENTA    = '\033[38;5;90m'   # ;M

            self.RED             = '\033[38;5;124m'  # ;r
            self.ORANGE          = '\033[38;5;166m'  # ;o
            self.YELLOW          = '\033[38;5;184m'  # ;y
            self.GREEN           = '\033[38;5;34m'   # ;g
            self.CYAN            = '\033[38;5;39m'   # ;c
            self.BLUE            = '\033[38;5;27m'   # ;b
            self.PURPLE          = '\033[38;5;55m'   # ;p
            self.MAGENTA         = '\033[38;5;127m'  # ;m

            self.STRONG_RED      = '\033[38;5;196m'  # ;rr
            self.STRONG_ORANGE   = '\033[38;5;202m'  # ;oo
            self.STRONG_YELLOW   = '\033[38;5;226m'  # ;yy
            self.STRONG_GREEN    = '\033[38;5;46m'   # ;gg                
            self.STRONG_CYAN     = '\033[38;5;51m'   # ;cc
            self.STRONG_BLUE     = '\033[38;5;21m'   # ;bb
            self.STRONG_PURPLE   = '\033[38;5;57m'   # ;pp
            self.STRONG_MAGENTA  = '\033[38;5;13m'  # ;mm

            self.BLACK           = '\033[38;5;0m'    # ;k
            self.DARK_GRAY       = '\033[38;5;238m'  # ;A
            self.GRAY            = '\033[38;5;244m'  # ;a
            self.LIGHT_GRAY      = '\033[38;5;250m'  # ;aa
            self.WHITE           = '\033[38;5;15m'   # ;w


class _Background:
    def __init__(self):
        self.DARK_RED        = '\033[48;5;52m'   # :R
        self.DARK_ORANGE     = '\033[48;5;94m'   # :O
        self.DARK_YELLOW     = '\033[48;5;142m'  # :Y
        self.DARK_GREEN      = '\033[48;5;22m'   # :G
        self.DARK_CYAN       = '\033[48;5;31m'   # :C
        self.DARK_BLUE       = '\033[48;5;4m'    # :B
        self.DARK_PURPLE     = '\033[48;5;31m'   # :P
        self.DARK_MAGENTA    = '\033[48;5;54m'   # :M

        self.RED             = '\033[48;5;124m'  # :r
        self.ORANGE          = '\033[48;5;130m'  # :o
        self.YELLOW          = '\033[48;5;184m'  # :y
        self.GREEN           = '\033[48;5;34m'   # :g
        self.CYAN            = '\033[48;5;45m'   # :c
        self.BLUE            = '\033[48;5;27m'   # :b
        self.PURPLE          = '\033[48;5;45m'   # :p
        self.MAGENTA         = '\033[48;5;127m'  # :m

        self.STRONG_RED      = '\033[48;5;196m'  # :rr
        self.STRONG_ORANGE   = '\033[48;5;202m'  # :oo
        self.STRONG_YELLOW   = '\033[48;5;190m'  # :yy
        self.STRONG_GREEN    = '\033[48;5;46m'   # :gg
        self.STRONG_CYAN     = '\033[48;5;14m'   # :cc
        self.STRONG_BLUE     = '\033[48;5;21m'   # :bb
        self.STRONG_PURPLE   = '\033[48;5;14m'   # :pp
        self.STRONG_MAGENTA  = '\033[48;5;201m'  # :mm

        self.BLACK           = '\033[48;5;0m'    # :k
        self.DARK_GRAY       = '\033[48;5;238m'  # :A
        self.GRAY            = '\033[48;5;244m'  # :a
        self.LIGHT_GRAY      = '\033[48;5;250m'  # :aa
        self.WHITE           = '\033[48;5;15m'   # :w


def _clamp(number):
    if number == '':
        number = 0

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
    # get the string of the matched color code and remove unwanted characters
    string = re.sub(r'\[|\]|\(|\)|/| ', '', matchobj[0])

    # if matched string is ':;' or ';:', then return ENDC (end color)
    if string == ':;' or string == ';:':
        return Color.ENDC

    col_type, col_val = string[0], string[1:]

    # custom color code
    if '#' in col_val or '=' in col_val:
        mode, val = col_val[0], col_val[1:]

        r, g, b = (map(_clamp, val.split(',')) if mode == '='
                   else _hex_to_rgb(val + '0' * (6 - len(val))))

        return f'\033[38;2;{r};{g};{b}m'

    # foreground color code
    elif col_type == ';':
        return getattr(Color.foreground, Defaults._color_list[col_val])

    # background color code
    else:
        return getattr(Color.background, Defaults._color_list[col_val])


def _color_format(string):
    # a failed attempt to make this a less convoluted regex
    pre = r'((\[(?=[^/\)]+\]))\s*|(\((?=[^/\]]+\)))\s*|/)?((?:(;)|(:))'
    color = r'(;|:|[ROYGCBPMkAw]|([roygcbpma])\8?'
    rgb = r'|(?(5)(= ?\d{0,3}\s?,\s?\d{0,3}\s?,\s?\d{0,3}'
    hex_rgb = r'|# ?[0-9A-Fa-f]{0,6})|\5)'
    cstm = Defaults._custom_codes
    suffix = r'))(/|(?(2)\s*\]|(?(3)\s*\))))?'

    # set regex to use (with true color, use custom color codes)
    if Color._true_color_active:
        regex = f'{pre}{color}{rgb}{hex_rgb}{cstm}{suffix}'
        endc_regex = f'{pre}{color}{rgb}{hex_rgb}{suffix}'

    else:
        regex = f'{pre}{color}{suffix}'
        endc_regex = f'{pre}{color}|;|:{suffix}'

    while ';;' in string or '::' in string: 
        codes = re.finditer(endc_regex, string)
        saved = []
        for matchobj in codes:
            code = matchobj[0]

            if ';;' not in code and '::' not in code:
                saved.append(matchobj)

            else:
                inv_code = '::' if ';;' in code else ';;'

                for mo in saved[::-1]:
                    if inv_code[0] in mo[0]:
                        
                        string = string.replace(code, '[;:]' + mo[0], 1)
                        saved = []
                    
                if len(saved) > 0:
                    string = string.replace(code, '[;:]', 1)
                    continue

    return re.sub(regex, _color_repl, string)


def paint(*strings, **options):

    # get the options' arguments
    _out = options.get('out', Defaults.paint['out'])
    _overflow = options.get('overflow', Defaults.paint['overflow'])
    _sep = options.get('sep', Defaults.paint['sep'])
    _end = options.get('end', Defaults.paint['end'][_out])
    _file = options.get('file', Defaults.paint['file'])
    _flush = options.get('flush', Defaults.paint['flush'])

    result = ''

    # if overflow is true, then color the strings as one
    if _overflow:
        result = _color_format(_sep.join(strings))
    
    # else, colors one by one and the join them
    else:
        formatted_strings = []

        for string in strings:
            formatted_strings.append(_color_format(string))
        
        result = _sep.join(formatted_strings)

    # if out is True, then print
    if _out:
        print(result, end=_end, file=_file, flush=_flush)

    return result


def codes():
    help_string = []

    for code in Defaults._color_list.keys():
        pass

    help_string = """The following are the color codes: 
\t  < colors >     < code >   < name >
\t- ";RDARK_RED;!":       ;R      (dark red)
\t- ";ODARK_ORANGE;!":    ;O      (dark orange)
\t- ";GDARK_GREEN;!":     ;G      (dark green)
\t- ";YDARK_YELLOW;!":    ;Y      (dark yellow)
\t- ";BDARK_BLUE;!":      ;B      (dark blue)
\t- ";MDARK_MAGENTA;!":   ;M      (dark magenta)
\t- ";CDARK_CYAN;!":      ;C      (dark cyan)

\t- ";rRED;!":            ;r      (red)
\t- ";oORANGE;!":         ;o      (orange)
\t- ";gGREEN;!":          ;g      (green)
\t- ";yYELLOW;!":         ;y      (yellow)
\t- ";bBLUE;!":           ;b      (blue)
\t- ";mMAGENTA;!":        ;m      (magenta)
\t- ";cCYAN;!":           ;c      (cyan)

\t- ";rrSTRONG_RED;!":     ;rr     (strong red)
\t- ";ooSTRONG_ORANGE;!":  ;oo     (strong orange)
\t- ";ggSTRONG_GREEN;!":   ;gg     (strong green)
\t- ";yySTRONG_YELLOW;!":  ;yy     (strong yellow)
\t- ";bbSTRONG_BLUE;!":    ;bb     (strong blue)
\t- ";mmSTRONG_MAGENTA;!": ;mm     (strong magenta)
\t- ";ccSTRONG_CYAN;!":    ;cc     (strong cyan)

\t- ";kBLACK;!":          ;k      (black)
\t- ";ADARK_GRAY;!":      ;A      (dark gray)
\t- ";aGRAY;!":           ;a      (gray)
\t- ";aaLIGHT_GRAY;!":     ;aa     (light gray)
\t- ";wWHITE;!":          ;w      (white)

\t- "ENDC":           ;!      (end color)"""

    extra_string = """
\t- "CUSTOM RGB":     ;=      (rgb)         [from 0 to 255, comma separated]
\t- "CUSTOM RGB%":    ;%      (rgb)         [from 0 to 1, comma separated]
\t- "CUSTOM HEX":     ;#      (hexadecimal) [from 000000 to ffffff]
    """

    paint(help_string, out=True)

    if Color._true_color_active:
        paint(extra_string, out=True)



Color()


if __name__ == '__main__':
    pass

else:
    if sys.platform[:3] == 'win':
        os.system('color')
