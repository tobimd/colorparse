import os
import sys
import re
import platform


class Color:
    @classmethod
    def _true_color(cls, is_supported):
        """This function changes the set of chosen colors. If "true color" is
        supported by whatever stdout is being used. Some terminals don't
        support "true color", so it should be set to False.

        Arguments:
                 (boolean) is_supported -- if the color set should be "true
                                           color" (True) or what could be
                                           called "classic" (False).

        Example use:
        Color._true_color(False) -- sets the color set to "classic".

        """

	# if the stdout supports rgb color escape sequences
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
            
            Color.true_color = True  # current value

	# if the stdout does not support rgb color escape sequences
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

            Color.true_color = False  # current value


def codes():
    """ Prints a list with all the colors available, their codes and their
    names.

        If "true color" is available (see 'mode' function), then 3 other color
    codes are added. These are "custom color codes" which allow rgb values to
    be set, using the normal 0 to 255 integers for red, green and blue (using
    ';='); percentages from 0 to 1 for each color value, up to 10 decimals
    (using ';%') and finally, a simple hex code that will represent the color
    values (using ';#').

        Both ';=' and ';%' (rgb and percentage) use comma separated values,
    which only allow up to one space before and after the comma. The value 0
    can be omitted, though the comma must be in the color code, otherwise it
    won't be parsed. Also, for hex values, the 0 will be filled up to the 6th
    value if needed, meaning that having ';#ff', ';ff0', etc. will always
    return the red color (having ';#' only, is allowed and will return black).

        Color codes examples (for the 'paint' function):

                        ";Rred box" -- paints "red box" in dark red.

                       ";r/red box" -- paints "red box" in red and uses '/' to
                                       force the color code to end.

                       ";gggrass;!" -- paints "grass" in strong green (';gg')
                                       and finishes the color printing.

               ";=255, 0, 0red box" -- paints "red box" in red.

                   ";=255,,red box" -- paints "red box" in red.

  ";%0.9882352941, .5, 0.8pink box" -- paints "pink box" in pink

                ";#Fc71b9/pink box" -- paints "pink box" in pink (note that
                                       mixed casing is allowed).

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
\t- "CUSTOM RGB":     ;=      (rgb)         [from 0 to 255, comma separated]
\t- "CUSTOM RGB%":    ;%      (rgb)         [from 0 to 1, comma separated]
\t- "CUSTOM HEX":     ;#      (hexadecimal) [from 000000 to ffffff]
    """

    paint(help_string, out=True)

    if Color.true_color:
        paint(extra_string, out=True)


def clamp(number):
    """ Fixes the number if it's lower than 0 or higher than 255, and returns
    it as a string.

    Arguments:
                       (int) number -- the number to fix.

    """
    if number < 0:
        number = 0

    if number > 255:
        number = 255
    
    return str(number)


def _percent_to_rgb(string):
    """ Replaces the percentages in a comma separated rgb values with integers
    from 0 to 255.

    Arguments:                                    
                       (str) string -- the percentage string to be replaced by
                                       rgb values.

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
    return map(clamp, [r, g, b])


def _hex_to_rgb(string):
    """ Replaces the hexadecimal values with integers from 0 to 255.

    Arguments:
                       (str) string -- the hex string to be replaced by rgb
                                       values.

    """
    # if it's an unfinished hex (e.g. "#FF01", missing the last two)
    string += '0' * (6 - len(string))  # fill with '0'

    # convert the strings to decimal using base 16
    r = int(string[:2], 16)
    g = int(string[2:4], 16)
    b = int(string[4:], 16)

    # return the fixed rgb values
    return map(clamp, [r, g, b])


def _color_repl(matchobj):
    """ The color code replacement (with real color escape sequences) when
    found by the regex used.

    Arguments:
            (match object) matchobj -- the matched object that the regex
                                       returns when a color code is found.

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
    """ With regex, finds the color codes to be replaced and returns the string
    with real color escape sequences.

    Arguments:
                       (str) string -- the input string to be formatted.

    """

    # clean the string at the start and the end
    string = ';!' + string + ';!'
    
    if Color.true_color: # if true_color is enabled, then custom rgb is enabled
        regex = r';(!|[AROGYBMCkw]|([arogybmc])\2?|=\d{0,3}\s?,\s?\d{0,3}\s?,\s?\d{0,3}|%(0?(\.\d{1,10})?|1)\s?,\s?(0?(\.\d{1,10})?|1)\s?,\s?(1|0?(\.\d{1,10})?)|#[0-9A-Fa-f]{0,6})\/?'

    else: # otherwise, only the default colors are available
        regex = r';(!|[AROGYBMCkw]|([arogybmc])\2?)\/?'

    return re.sub(regex, _color_repl, string)


def paint(*strings, **options):
    """ Returns and prints a string (if the 'out' argument is False, the string
    won't be printed) that will have color codes parsed or converted to real
    color escape sequences.

        Some values in the 'options' argument, won't affect the resulting
    string because those are meant to be used if the string is printed, which
    are 'end', 'file' and 'flush'.

        Color codes can be "closed" (not to be confused with "ended" which will
    be explained later) with the character '/' (slash). This helps when the
    color code is followed by the same letter (e.g. ";rred box" then returns
    "ed box" in dark red, so to avoid this, use '/' like: ";r/red box"). It is
    recommended to always close color codes, for readability and unwanted
    mistakes.

        This function allows more than one string to be given as an argument,
    like printing does (this similarity also applies to the options, as they
    have to be used with the key word). If a color code is not "ended", it
    means that the color code ";!" has not been used. If that happens, then the
    color will not pass through to the other available strings given as an
    argument by default. To change this this, the option "overflow" can be set
    to "True".

        Finally, it's important to know the following: for security reasons,
    any resulting strings are returned with the ";!" color code at the
    beggining and the end; having the 'mode' function set to 2 or 'classic'
    (see 'mode' function) won't show and won't parse the extra 3 custom color
    codes (see 'codes' function)

    Arguments:
                      (str) *string -- one or more strings that may have color
                                       codes.

    **options:
                    (bool) out=True -- prints the resulting string if set to
                                       True.

              (bool) overflow=False --  let's color codes pass through other
                                        string arguments if set to True.

                      (str) sep=' ' -- used to separate the string arguments.

                     (str) end='\n' -- used at the end of a string when
                                       printed.

         (file obj) file=sys.stdout -- used by the interpreter for standard
                                       output.

                 (bool) flush=False -- the stream is forcibly flushed if set
                                       to True.

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


def mode(mode_type=1, out=False):
    """ This changes the set of colors. If this module is being used in
    Windows, then it's set to 1 or "new" beforehand, in any other case it's
    set to 2 or "classic" by default. This is because some terminals or other
    stdout don't have support for "true color" which is used when set to 1.

    Arguments:
            (int | str) mode_type=1 -- this can be either 1 (or "new") for the
                                       true color look and feel, or 2 (or
                                       "classic") for the old color scheme.

                   (bool) out=False -- if the change should be verbose and
                                       printed.

    """
    repeated = ''

    t = mode_type

    if t == 2 or (type(t) == str and t.lower() == 'classic'):
        
        if not Color.true_color:
            repeated = 'were already '

        Color._true_color(False)
        return paint(f'[ ;acolor scheme;! ] Colors {repeated}set to ;gclassic;!.', out=out)
    elif t == 1 or (type(t) == str and t.lower() == 'new'):
        if Color.true_color:
            repeated = 'were already '

        Color._true_color(True)
        return paint(f'[ ;acolor scheme;! ] Colors {repeated}set to ;gnew;!.', out=out)


def help(fn=None):
    """ This prints a help menu with all of the commands available.

    Arguments:
           (function | str) fn=None -- the function to get the help from.

    """

    help_strings = {
        'help' : """ This prints a help menu with all of the commands available.

    Arguments:
           (function | str) fn=None -- the function to get the help from.

    """,

        'mode' : """ This changes the set of colors. If this module is being used in
    Windows, then it's set to 1 or "new" beforehand, in any other case it's
    set to 2 or 'classic' by default. This is because some terminals or other
    stdout don't have support for "true color" which is used when set to 1.

    Arguments:
            (int | str) mode_type=1 -- this can be either 1 (or "new") for the
                                       true color look and feel, or 2 (or
                                       "classic") for the old color scheme.

                   (bool) out=False -- if the change should be verbose and
                                       printed.

    """,

        'paint' : """ Returns and prints a string (if the 'out' argument is False, the string
    won't be printed) that will have color codes parsed or converted to real
    color escape sequences.

        Some values in the 'options' argument, won't affect the resulting
    string because those are meant to be used if the string is printed, which
    are 'end', 'file' and 'flush'.

        Color codes can be "closed" (not to be confused with "ended" which will
    be explained later) with the character '/' (slash). This helps when the
    color code is followed by the same letter (e.g. ";rred box" then returns
    "ed box" in dark red, so to avoid this, use '/' like: ";r/red box"). It is
    recommended to always close color codes, for readability and unwanted
    mistakes.

        This function allows more than one string to be given as an argument,
    like printing does (this similarity also applies to the options, as they
    have to be used with the key word). If a color code is not "ended", it
    means that the color code ";!" has not been used. If that happens, then the
    color will not pass through to the other available strings given as an
    argument by default. To change this this, the option "overflow" can be set
    to "True".

        Finally, it's important to know the following: for security reasons,
    any resulting strings are returned with the ";!" color code at the
    beggining and the end; having the 'mode' function set to 2 or 'classic'
    (see 'mode' function) won't show and won't parse the extra 3 custom color
    codes (see 'codes' function)

    Arguments:
                      (str) *string -- one or more strings that may have color
                                       codes.

    **options:
                    (bool) out=True -- prints the resulting string if set to
                                       True.

              (bool) overflow=False --  let's color codes pass through other
                                        string arguments if set to True.

                      (str) sep=' ' -- used to separate the string arguments.

                     (str) end='\n' -- used at the end of a string when
                                       printed.

         (file obj) file=sys.stdout -- used by the interpreter for standard
                                       output.

                 (bool) flush=False -- the stream is forcibly flushed if set
                                       to True.

    """,

        'codes' : """ Prints a list with all the colors available, their codes and their
    names.

        If "true color" is available (see 'mode' function), then 3 other color
    codes are added. These are "custom color codes" which allow rgb values to
    be set, using the normal 0 to 255 integers for red, green and blue (using
    ';='); percentages from 0 to 1 for each color value, up to 10 decimals
    (using ';%') and finally, a simple hex code that will represent the color
    values (using ';#').

        Both ';=' and ';%' (rgb and percentage) use comma separated values,
    which only allow up to one space before and after the comma. The value 0
    can be omitted, though the comma must be in the color code, otherwise it
    won't be parsed. Also, for hex values, the 0 will be filled up to the 6th
    value if needed, meaning that having ';#ff', ';ff0', etc. will always
    return the red color (having ';#' only, is allowed and will return black).

        Color codes examples (for the 'paint' function):

                        ";Rred box" -- paints "red box" in dark red.

                       ";r/red box" -- paints "red box" in red and uses '/' to
                                       force the color code to be closed.

                       ";gggrass;!" -- paints "grass" in strong green (';gg')
                                       and ends the color printing.

               ";=255, 0, 0red box" -- paints "red box" in red.

                   ";=255,,red box" -- paints "red box" in red.

  ";%0.9882352941, .5, 0.8pink box" -- paints "pink box" in pink

                ";#Fc71b9/pink box" -- paints "pink box" in pink (note that
                                       mixed casing is allowed).

    """,
    }

    help_string = """ This module helps coloring strings with ease, by using
    color codes. If "true color" is available, then three other color codes
    are added which let the use of custom rgb colors.

        The following are the functions available:

                      help(fn=None) -- prints helpful messages and guides,
                                       where "fn" can be this module's
                                       functions or their respective names.

                            codes() -- prints a list of all the color codes.

          paint(*string, **options) -- returns and prints all the given strings
                                       with the color codes parsed to the real
                                       color escape sequences.

                  mode(mode_type=1) -- changes what color set is being used,
                                       where 1 is the same as "new" and 2 is
                                       the same as "classic".
        
    """

    if callable(fn) and fn.__name__ in help_strings:
        print('\n\t' + help_strings[fn.__name__].strip())

    elif type(fn) == str and fn in help_strings:
        print('\n\t' + help_strings[fn].strip())

    else:
        print('\n\t' + help_string)


if platform.system() == 'Windows':
    os.system('color')
    Color._true_color(True)
else:
    Color._true_color(False)
