# Colorparse

#### Current version: 0.0.2

This unoriginal package let's the user generate strings with ansi color escape sequences (which are "*codes*" that tell the terminal what color to display the proceeding characters, and much more: <https://wikipedia.org/wiki/ANSI_escape_code>)

Colorparse will simplify the work by reading it's self-defined "*color codes*" inside the strings (e.g. `;r` will produce the color red).

Beware that the words "color code(s)" will be used extensively.

# Index
- [Installation](https://github.com/tubi-carrillo/colorparse/tree/master/example#installation)
- [How to use](https://github.com/tubi-carrillo/colorparse/tree/master/example#how-to-use)
- [Usage as imported module](https://github.com/tubi-carrillo/colorparse/tree/master/example#usage-as-imported-module)
- [Usage in terminal](https://github.com/tubi-carrillo/colorparse/tree/master/example#usage-in-terminal)
- [Color codes](https://github.com/tubi-carrillo/colorparse/tree/master/example#color-codes)
- [Further reading](https://github.com/tubi-carrillo/colorparse/tree/master/example#further-reading)

# Installation

- with pip:
`pip install --user colorparse`

# How to use
This will be a general approach to how the strings are parsed and how to use the color codes.

### List of color codes
To read the list of all available color codes, go to [color codes](https://github.com/tubi-carrillo/colorparse/tree/master/example#color-codes) below.

### How color codes work
The parser will look for color codes that always start with a semicolon or a colon (foreground and background respectively), and replace that value with it's ANSI color escape sequence. These sequences have a structure similar to this: `ESC[<n>;<n>;...;<n>m` where they start with a specific `ESC` string (which in this case, we use `\033`) and always end with the letter `m`. When accessing each color in the `Color` class, the returned value will be these color escape sequences.

When a color is initialized, it means that within the string, when we use a color code (like `;g` for green in the following example) the proceeding characters will have the same color until they are reset or changed to other colors.

The best way to explain is with an example. Note that the color codes have a "/" (slash) in front, to make it clear what the color code is (check below for an explanation of how closing color codes work):

_The first colored text shows how the green color code `;g` is displayed. Next, the following 3 show how the use of each "end color" works (`;:` ends all colors, `;;` ends foreground colors and `::` ends background colors, which didn't work because the green color was used as foreground). Finally, the last two show how `::` and `;;` can help by only endind that type of color)._
![example codes](https://github.com/tubi-carrillo/colorparse/blob/master/example/example_3.png)

### Closing color codes
To close a color code means that the parser will recognize normally what the color code is, but improves readability by making the user see better where the colors are being initialized or finished. Doing this is completely optional, but helps avoiding problems like getting `";rred box"` shown as `ed box` in dark red (the `;rr` is considered a color code). Instead, one could use `";r/red box"`.

Options to close a color code:
- Square brackets: there must be two opposing square brackets as such: `[<color code>]`, for example:`" [;r] "` (space characters are allowed at both sides).

- Normal brackets: the same as square brackets: `(<color code>)`, for example: `" (;r) "`.

- Slash: there can be one at each side, or only one at one side: `<color code>/`, `/<color code>` and `/<color code>/`, for example: `" ;r/ "`, `" /;r "` and `" /;r/ "` (no spaces are allowed before nor after the color code).

Having more than one closing for a color code is not accepted by the parser, which may be usefull when trying to get a color code inside brackets like `" [ /;r/ ]"`, that will return `" [  ] "` with the second bracket in red. Having at least one slash is enough to make the parser ignore the brackets.

### Escaping color codes
Sometimes it may be neccessary to escape color codes, so the use of a `\` (backslash) immediately before the `;` or `:` will make the parser ignore that color code (e.g. `" \;r "` won't parse the red color).

# Usage as imported module

When importing `colorparse`, the function `paint` is the most important one. This function is the one that will return and/or print the color coded string.

There is the option to get each color individually, by accessing the `Color` class with this structure: "`Color.type.color`", where `type` can be either `foreground` or `background`, and `color` is the color name in uppercase as shown when using the `codes` function (e.g. `Color.foreground.DARK_RED` returns the dark red color).

The following functions are the ones that can be used when importing this module:

---

`paint(string, ..., print=True, ret=True, overflow=False, sep=' ', end='\n', file=sys.stdout, flush=False)`

`paint(*string, **options)`


Returns a string that will have color codes converted to real ANSI color escape sequences (if `print` is `False`, then the string won't be printed and the arguments: `end`, `file` and `flush` won't be considered whatever their values may be, because those are for printing purposes only). The returned and/or printed string will always end all color codes, returning to normal even if they were already ended. Having `ret` as `False` will not return a string, though it's normally unnecessary to change this value.

If there is more than one string given as argument, then having `overflow` as `True`, will allow any unfinished color from a color code to pass through to the other strings. If it's `False` (which is by default), then all colors will be finished at the end of each string.

Example:

_In this example, the red color passes through to the next string because `overflow` was set to `True` in the first part. This is not the case for the second part, where `overflow` was `False` and that made the red color to stay within the first string._

  ![python example using the `paint` function](https://github.com/tubi-carrillo/colorparse/blob/master/example/example_1.png)
 

---

`codes()`

Prints a list of all the color codes available. It shows the background, foreground, code and the name of each color code.


---

`true_color(value=None)`

There are two available options for how colors are printed. When `value` is `True`, it means that the set of foreground colors will be using direct *rgb* values for each ANSI escape sequence. Note that background colors do not support this funcitonallity, so even if truecolor is active, background colors will always look the same. Be warned, that not all terminals support true color (because of that, it's set to `False` at the beggining of the program by default).

If no value is given, then the current state is returned (returns if true color is active or not)


---

`change_defaults(fn, key=value, ...)`

`change_defaults(fn, **kwargs)`

This can be used at the beggining of the program, to set the default values permanently for the rest of it. This way one can avoid setting the values for the function options (like in `paint`) each time it's used.

The argument `fn` can be the exact function or the function's name as a string. This was designed for future pruposes as more functions may be added with time.

Example:

![python example using the `change_defaults` function](https://github.com/tubi-carrillo/colorparse/blob/master/example/example_2.png)

# Usage in terminal

Using `colorparse` in the terminal has the following options:

```
colorparse [-h] [-t] [-f [FILE]] [-o] [-S SEP] [-E END] [-c] [-v]
                  [string [string ...]]

positional arguments:
  string                a string that may contain color codes

optional arguments:
  -h, --help            show this help message and exit
  -t, --true-color      use of rgb values for the color escape sequences,
                        allowing customized foreground color codes and having
                        the color set be more accurate (warning: having this
                        option won't work on all terminals as they do not all
                        have true color).
  -f [FILE], --file [FILE]
                        specify an output file to send the resulting formatted
                        string. If the file exists, it will be appended to the
                        end of said file.
  -o, --overflow        make color codes overflow to other strings if the
                        previous one has not ended the color code.
  -s SEP, --sep SEP     specify what to use to separate string arguments.
  -e END, --end END     specify what to use at the end of the resulting
                        formatted string
  -c, --codes           show the available color codes and exit.
  -v, --version         show the current version of this module and exit.

```

# Color codes

Each of the following colors (with the exception of the `ENDC` with it's variants, and the custom color codes that are available when the `true_color` function is set to true) can have either a `;` (semicolon) for foreground or a `:` (colon) for background, preceding the letter.

```
    DARK             NORMAL          STRONG

rr (DARK_RED)       r (RED)       R (STRONG_RED)
oo (DARK_ORANGE)    o (ORANGE)    O (STRONG_ORANGE)         examples: 
yy (DARK_YELLOW)    y (YELLOW)    Y (STRONG_YELLOW)            ;oo (sets foreground color to dark orange)
gg (DARK_GREEN)     g (GREEN)     G (STRONG_GREEN)             ;r (sets foreground color to red)
cc (DARK_CYAN)      c (CYAN)      C (STRONG_CYAN)
bb (DARK_BLUE)      b (BLUE)      B (STRONG_BLUE)              :pp (sets the background color to dark purple)
pp (DARK_PURPLE)    p (PURPLE)    P (STRONG_PURPLE)            :B (sets background color to strong blue)
mm (DARK_MAGENTA)   m (MAGENTA)   M (STRONG_MAGENTA)
```

For `ENDC` (end color) and it's variants, it can be `;:` or `:;` to end both foreground and background colors (regardless if there is one or the other actually being colored), `;;` to end only the foreground color and  `::` to end only the background color. Note that only `;:` and `:;` can be accessed by the `Color` class (with `Color.ENDC`) because the other two are the same concept, but they don't exist and are parsed by analysing what previous color was being used.

Finally, if true color is active, custom colors will have this structure (note that missing values are assigned to 0):
- `;=` will read rgb values, where all the following color codes are accepted: `;=255,255,255`, `;=255,255` (is the same as `;=255,255,0`), `;=255,,` (is the same as `;=255,0,0`), `;=` (is the same as `;=,,` and `;=0,0,0`). 

- `;#` will read hexadecimal values, where the following color codes are accepted: `;#ff00ff`, `;#00ff` (is the same as `;#00ff00`), `;#000` (is the same as `;#` and`;#000000`).

# Further reading

### Conventions
The following shall be considered as a recommendations:

- Allways use the color codes with one of the closing options, preferably the brackets. And stick to that for the rest of the string.
- Do not use `;;` nor `::` for large strings, as it may become difficult to remember where the color was initiated.
- Always write the complete values for the custom color codes (even if the values are 0, which the program allowes them to be omitted).
- If using slash as a color closing option, use it on both sides of the color codes.

### Known Issues
- Version in colorparse.py was not updated.
- New line character (and presumably other of that type) don't work when used with from terminal.

### Change log

```diff
! 0.0.2
* fixed Windows script file

! 0.0.1
# the first version has no changes
```