import os
import sys
import re
import platform


class Color:
    @classmethod
    def _true_color(cls, is_supported):
        """This function changes the values of all the base colors
        to the one your terminal supports. If 'value' is False,
        then the colors will turn to a more classic look being supported
        by all terminals. Otherwise, if it is True, then 'true color' is
        available and works, which means RGB values can be directly used
        in the color codes.

        """

        if is_supported:
            Color.DARK_RED        = '\033[38;2;80;0;0m'        # ;R
            Color.DARK_ORANGE     = '\033[38;2;80;40;0m'       # ;G
            Color.DARK_GREEN      = '\033[38;2;0;80;0m'        # ;G
            Color.DARK_YELLOW     = '\033[38;2;87;74;0m'       # ;Y
            Color.DARK_BLUE       = '\033[38;2;0;30;100m'      # ;B
            Color.DARK_MAGENTA    = '\033[38;2;50;0;70m'       # ;M
            Color.DARK_CYAN       = '\033[38;2;0;80;110m'      # ;C

            Color.RED             = '\033[38;2;150;0;0m'       # ;r
            Color.ORANGE          = '\033[38;2;170;70;0m'      # ;o
            Color.GREEN           = '\033[38;2;0;150;0m'       # ;g
            Color.YELLOW          = '\033[38;2;150;130;0m'     # ;y
            Color.BLUE            = '\033[38;2;0;40;180m'      # ;b
            Color.MAGENTA         = '\033[38;2;140;0;180m'     # ;m
            Color.CYAN            = '\033[38;2;0;190;200m'     # ;c

            Color.STRONG_RED      = '\033[38;2;255;0;0m'       # ;rr
            Color.STRONG_ORANGE   = '\033[38;2;255;100;0m'     # ;oo
            Color.STRONG_GREEN    = '\033[38;2;80;255;15m'     # ;gg
            Color.STRONG_YELLOW   = '\033[38;2;255;255;0m'     # ;yy
            Color.STRONG_BLUE     = '\033[38;2;0;20;255m'      # ;bb
            Color.STRONG_MAGENTA  = '\033[38;2;200;0;255m'     # ;mm
            Color.STRONG_CYAN     = '\033[38;2;0;255;255m'     # ;cc

            Color.BLACK           = '\033[38;2;0;0;0m'         # ;k
            Color.DARK_GRAY       = '\033[38;2;70;70;70m'      # ;A
            Color.GRAY            = '\033[38;2;130;130;130m'   # ;a
            Color.LIGHT_GRAY      = '\033[38;2;185;185;185m'   # ;aa
            Color.WHITE           = '\033[38;2;255;255;255m'   # ;w

            Color.ENDC            = '\033[0m'                  # ;!
            
            Color.true_color = True
        else:
            Color.DARK_RED        = '\033[38;5;88m'   # ;R
            Color.DARK_ORANGE     = '\033[38;5;130m'  # ;O
            Color.DARK_GREEN      = '\033[38;5;22m'   # ;G
            Color.DARK_YELLOW     = '\033[38;5;142m'  # ;Y
            Color.DARK_BLUE       = '\033[38;5;17m'   # ;B
            Color.DARK_MAGENTA    = '\033[38;5;55m'   # ;M
            Color.DARK_CYAN       = '\033[38;5;31m'   # ;C

            Color.RED             = '\033[38;5;124m'  # ;r
            Color.ORANGE          = '\033[38;5;166m'  # ;o
            Color.GREEN           = '\033[38;5;34m'   # ;g
            Color.YELLOW          = '\033[38;5;184m'  # ;y
            Color.BLUE            = '\033[38;5;27m'   # ;b
            Color.MAGENTA         = '\033[38;5;127m'  # ;m
            Color.CYAN            = '\033[38;5;39m'   # ;c

            Color.STRONG_RED      = '\033[38;5;196m'  # ;rr
            Color.STRONG_ORANGE   = '\033[38;5;202m'  # ;oo
            Color.STRONG_GREEN    = '\033[38;5;46m'   # ;gg
            Color.STRONG_YELLOW   = '\033[38;5;226m'  # ;yy
            Color.STRONG_BLUE     = '\033[38;5;21m'   # ;bb
            Color.STRONG_MAGENTA  = '\033[38;5;200m'  # ;mm
            Color.STRONG_CYAN     = '\033[38;5;51m'   # ;cc

            Color.BLACK           = '\033[38;5;0m'    # ;k
            Color.DARK_GRAY       = '\033[38;5;238m'  # ;A
            Color.GRAY            = '\033[38;5;242m'  # ;a
            Color.LIGHT_GRAY     = '\033[38;5;250m'   # ;aa
            Color.WHITE           = '\033[38;5;15m'   # ;w

            Color.ENDC            = '\033[0m'         # ;!

            Color.true_color = False


def code_list():
    """Returns a string with a list of all the available
    color names and their respective codes.

    """

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
\t- "CUSTOM RGB":     ;=      (rgb)             [from 0 to 255, comma separated]
\t- "CUSTOM RGB%":    ;%      (rgb)             [from 0\u00b710\u00b9\u2070 to 1, comma separated]
\t- "CUSTOM HEX":     ;#      (hexadecimal)     [from 000000 to ffffff]
    """

    brush(help_string, out=True)

    if Color.true_color:
        brush(extra_string, out=True)


def _fix_min_max_values(number):
    """Fixes the number if it's lower than 0 or higher than
    255, and returns it as a string.

    """
    if number < 0:
        number = 0

    if number > 255:
        number = 255
    
    return str(number)


def _percent_to_rgb(string):
    """Replaces the percentages in a comma separated
    rgb values with 0 to 255 numbers.

    """
    # if it's an unfinished code (e.g. "%0.8,,", missing the last two)
    string = string.split(',')
    for i, val in enumerate(string):
        if val == '':
            string[i] = '0' # fill with a '0'

    # get the percentages for each rgb value in a list
    percentages = tuple(map(float, string))

    # convert the percentages to decimal values
    r = int(255 * percentages[0])
    g = int(255 * percentages[1])
    b = int(255 * percentages[2])

    # return the fixed rgb values
    return map(_fix_min_max_values, [r, g, b])


def _hex_to_rgb(string):
    """Replaces the hexadecimal rgb values with 0 to 
    255 numbers

    """
    # if it's an unfinished hex (e.g. "#FF01", missing the last two)
    string += '0' * (6 - len(string))  # fill with '0'

    # convert the strings to decimal using base 16
    r = int(string[:2], 16)
    g = int(string[2:4], 16)
    b = int(string[4:], 16)

    # return the fixed rgb values
    return map(_fix_min_max_values, [r, g, b])


def _color_repl(matchobj):
    """Returns the new string for a match object.

    """

    code_to_color = {
        ";R" :  Color.ENDC + Color.DARK_RED,
        ";O" :  Color.ENDC + Color.DARK_ORANGE,
        ";G" :  Color.ENDC + Color.DARK_GREEN,
        ";Y" :  Color.ENDC + Color.DARK_YELLOW,
        ";B" :  Color.ENDC + Color.DARK_BLUE,
        ";M" :  Color.ENDC + Color.DARK_MAGENTA,
        ";C" :  Color.ENDC + Color.DARK_CYAN,
        ";r" :  Color.ENDC + Color.RED,
        ";o" :  Color.ENDC + Color.ORANGE,
        ";g" :  Color.ENDC + Color.GREEN,
        ";y" :  Color.ENDC + Color.YELLOW,
        ";b" :  Color.ENDC + Color.BLUE,
        ";m" :  Color.ENDC + Color.MAGENTA,
        ";c" :  Color.ENDC + Color.CYAN,
        ";rr" : Color.ENDC + Color.STRONG_RED,
        ";oo" : Color.ENDC + Color.STRONG_ORANGE,
        ";gg" : Color.ENDC + Color.STRONG_GREEN,
        ";yy" : Color.ENDC + Color.STRONG_YELLOW,
        ";bb" : Color.ENDC + Color.STRONG_BLUE,
        ";mm" : Color.ENDC + Color.STRONG_MAGENTA,
        ";cc" : Color.ENDC + Color.STRONG_CYAN,
        ";k" :  Color.ENDC + Color.BLACK,
        ";A" :  Color.ENDC + Color.DARK_GRAY,
        ";a" :  Color.ENDC + Color.GRAY,
        ";aa" : Color.ENDC + Color.LIGHT_GRAY,
        ";w" :  Color.ENDC + Color.WHITE,
        ";!" :  Color.ENDC,
    }

    # get the matched string, with no unwanted space characters
    matched_string = matchobj.group(0).replace(' ', '')

    # take the '/' off
    if '/' in matched_string:
        matched_string = matched_string[:-1]
    
    # if the matched string is a custom color code (rgb or hex)
    if '=' in matched_string or '%' in matched_string or '#' in matched_string:

        if '%' in matched_string: # transform to normal rgb values
            matched_rgb = _percent_to_rgb(matched_string[2:])

        elif '#' in matched_string: # transform to normal rgb values
            matched_rgb = _hex_to_rgb(matched_string[2:])

        else: # remove the ";=" at the start and fill missing values
            matched_rgb = matched_string[2:].split(',')
            for i, val in enumerate(matched_rgb):
                if val == '':
                    matched_rgb[i] = '0' # fill with '0'

        # split the values and place them in the color code for rgb
        r, g, b = matched_rgb
        return f'{Color.ENDC}\033[38;2;{r};{g};{b}m'
    
    # otherwise, if the matched string is a known color code
    else:
        return code_to_color[matched_string]


def _color_format(string):
    """Returns a string that has the color codes replaced
    by the colors needed.
    Function arguments:
    string -- the input string to be formatted

    """

    # clean the string at the start and the end
    string = ';!' + string + ';!'
    
    if Color.true_color: # if true_color is enabled, then custom rgb is enabled
        regex = r';(!|[AROGYBMCkw]|([arogybmc])\2?|=\d{0,3}\s?,\s?\d{0,3}\s?,\s?\d{0,3}|%(0?(\.\d{1,10})?|1)\s?,\s?(0?(\.\d{1,10})?|1)\s?,\s?(1|0?(\.\d{1,10})?)|#[0-9A-Fa-f]{0,6})\/?'

    else: # otherwise, only the default colors are available
        regex = r';(!|[AROGYBMCkw]|([arogybmc])\2?)\/?'

    return re.sub(regex, _color_repl, string)


def paint(*strings, **options):
    """Returns a string (can be printed directly) that reads
    and decodes color codes to make words or sentences be colored.
    Having the option to print ('out') as False doesn't mean the string 
    won't be returned by this function. It is always returned.

    Some of the options won't affect the resulting string if the argument
    'out' is False, because those are for printing only ('file' and
    'flush' to be precise). The only exception is 'end', which is only
    used when printing, for consistency.

    A color code can end with '/' to avoid problems with strong
    colors being accidentally used (e.g. ";ggo home" would return "o home"
    in strong green). The use of '/' at the end of a color code is
    completely optional.

    Note that any unclosed color code will pass through to the next
    string object by default. Also, color codes in the options arguments
    will not be parsed.

    Finally, having "look" set to 2 (classic) won't parse custom color
    codes.

    Function arguments:
    *strings -- all the strings that need to be decoded or printed
    **options:
      out -- if the result should be printed (default True)
      overflow -- if the color codes pass through objects (default False)
      sep -- what is used to separate the strings (default ' ')
      end -- what is used to end the result string (default '\n')
      file -- object with a 'write(string)' method (default sys.stdout)
      flush -- if the stream is forcibly flushed (default False)

    """

    # default values
    opt = {'out': True,
           'overflow': False,
           'sep': ' ',
           'end': '\n',
           'file': sys.stdout,
           'flush': False,}

    # go through option arguments and
    # replace them as needed
    for key, val in options.items():
        if key in opt.keys():
            opt[key] = val

    result = ''

    # if overflow is True, then color format the joined strings
    if opt['overflow']:
        result = _color_format(opt['sep'].join(strings))
        
    # else, color format one by one and then join
    else:
        formatted_strings = []
        for string in strings:
            formatted_strings.append(_color_format(string))
            
        result = opt['sep'].join(formatted_strings)

    # if 'out' is True, then print
    if opt['out']:
        print(result, sep=opt['sep'], end=opt['end'],
              file=opt['file'], flush=opt['flush'])
    
    return result


def look(mode=1):
    """This changes the overall color codes to a more "classic" feel
    by changin to a more standard and platform supported color codes.

    Function arguments:
    mode -- this can be either 1 (or "new") for the true color look 
    and feel, or 2 (or "classic") for the old color scheme (default 1)

    """
    repeated = ''

    if mode == 2 or (type(mode) == str and mode.lower() == 'classic'):
        if not Color.true_color:
            repeated = 'were already '

        Color._true_color(False)
        brush(f'[ ;acolor scheme;! ] Colors {repeated}set to ;gclassic;!.')
    elif mode == 1 or (type(mode) == str and mode.lower() == 'new'):
        if Color.true_color:
            repeated = 'were already '

        Color._true_color(True)
        brush(f'[ ;acolor scheme;! ] Colors {repeated}set to ;gnew;!.')


def help(function=None):
    """This prints a help menu with all of the commands.

    Function arguments:
    function -- the function to get the help menu from (default None)

    """

    function_help_strings = {
        'help' : """This prints a help menu with all of the commands.

    Function arguments:
    function -- the function to get the help menu from (default None)

    """,

        'look' : """This changes the overall color codes to a more "classic" feel
    by changin to a more standard and platform supported color codes.

    Function arguments:
    mode -- this can be either 1 (or "new") for the true color look 
    and feel, or 2 (or "classic") for the old color scheme (default 1)

    """,

        'paint' : """Returns a string (can be printed directly) that reads
    and decodes color codes to make words or sentences be colored.
    Having the option to print ('out') as False doesn't mean the string 
    won't be returned by this function. It is always returned.

    Some of the options won't affect the resulting string if the argument
    'out' is False, because those are for printing only ('file' and
    'flush' to be precise). The only exception is 'end', which is only
    used when printing, for consistency.

    A color code can end with '/' to avoid problems with strong
    colors being accidentally used (e.g. ";ggo home" would return "o home"
    in strong green). The use of '/' at the end of a color code is
    completely optional.

    Note that any unclosed color code will pass through to the next
    string object by default. Also, color codes in the options arguments
    will not be parsed.

    Finally, having "look" set to 2 (classic) won't parse custom color
    codes.

    Function arguments:
    *strings -- all the strings that need to be decoded or printed
    **options:
      out -- if the result should be printed (default True)
      overflow -- if the color codes pass through objects (default False)
      sep -- what is used to separate the strings (default ' ')
      end -- what is used to end the result string (default '\\n')
      file -- object with a 'write(string)' method (default sys.stdout)
      flush -- if the stream is forcibly flushed (default False)

    """,

        'code_list' : """Returns a string with a list of all the available
    color names and their respective codes.

    """,
    }

    help_string = """This module helps color coding strings with custom commands.

    To format a string, use the function 'brush' that will read the color codes
    used and format it to show the wanted colors. To see the list of color codes, 
    there is a function called 'code_list' that will print out all the colors 
    available.
    
    You can access individual colors with the Color class. For example: 'Color.DARK_RED'
    will return the string corresponding to a dark red color code. 
    
    Finally, if colors are not being correctly displayed, the use of the 'look' function
    will help using the old, classic colors that should be cross-platform.
    
    Functions:
    help -- prints this message, if you put a function as argument, it will print it's 
            help menu
    brush -- returns and prints* a string with the formatted colors as used according to
             the color codes present
    code_list -- prints a list of all the colors and color codes available"""

    if function == None:
        print(help_string)
    else:
        print('\n\t' + function_help_strings[function].strip())


if platform.system() == 'Windows':
    os.system('color')
    Color._true_color(True)
else:
    Color._true_color(False)
