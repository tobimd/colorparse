# Colorparse

_current version: v0.0.1_\\

This unoriginal package let's the user generate strings with ansi color escape sequences (which are "*codes*" that tell the terminal what color to display the proceeding characters, and much more: <https://wikipedia.org/wiki/ANSI_escape_code>)

Colorparse will simplify the work by reading it's self-defined "*color codes*" inside the strings (e.g. " ;r " will produce the color red).

Beware that the words "color code(s)" will be used extensively.

# Index
- [Installation](https://github.com/tubi-carrillo/colorparse#installation)
- [How to color code](https://github.com/tubi-carrillo/colorparse#how-to-color-code)
- [Usage as imported module](https://github.com/tubi-carrillo/colorparse#usage-as-imported-module)
- [Usage in terminal](https://github.com/tubi-carrillo/colorparse#usage-in-terminal)
- [Color codes](https://github.com/tubi-carrillo/colorparse#color-codes)
- [Further reading](https://github.com/tubi-carrillo/colorparse#further-reading)

# Installation

# How to color code
### list of color codes
To read the list of all available color codes, go to [color codes](https://github.com/tubi-carrillo/colorparse#color-codes) below.

### how color codes work

### closing color codes

### ending color codes

### escaping color codes

# Usage as imported module

When importing `colorparse`, the function `paint` is the most important one. This function is the one that will return and/or print the color coded string.

The following functions are the ones that can be used when importing this module:


`paint(string, ..., print=True, ret=True, overflow=False, sep=' ', end='\n', file=sys.stdout, flush=False)`

`paint(*string, **options)`

Returns a string that will have color codes converted to real ANSI color escape sequences (if `print` is `False`, then the string won't be printed and the arguments: `end`, `file` and `flush` won't be considered whatever their values may be, because those are for printing purposes only). The returned and/or printed string will always end all color codes, returning to normal even if they were already ended. Having `ret` as `False` will not return a string, though it's normally unnecessary to change this value.

If there is more than one string given as argument, then having `overflow` as `True`, will allow any unfinished color from a color code to pass through to the other strings. If it's `False` (which is by default), then all colors will be finished at the end of each string.

Example:

  ![python example using the `paint` function](https://github.com/tubi-carrillo/colorparse/blob/master/example/example_1.png)




`codes()`

Prints a list of all the color codes available. It shows the background, foreground, code and the name of each color code.




`true_color(value=None)`

There are two available options for how to colors are printed. When `true_color` is set to `True`, it means that the set of foreground colors will be using direct *rgb* values for each ANSI escape sequence. Note that background colors do not support this funcitonallity, so even if you have `true_color` active, background colors will always look the same. Be warned, that not all terminals support true color (this way, it's set to `False` at the beggining of the program by default).

If no value is given, then the current state is returned (returns if true color is active or not)



`change_defaults(fn, key=value, ...)`
`change_defaults(fn, **kwargs)`

This can be used at the beggining of the program, to set the default values permanently for the rest of it. This way one can avoid setting the values for the function options (like in `paint`) each time it's used.

The argument `fn` can be the exact function or the function's name as a string. This was designed for future pruposes as more functions may be added with time.

Example:

![python example using the `change_defaults` function](https://github.com/tubi-carrillo/colorparse/blob/master/example/example_2.png)

# Usage in terminal

# Color codes

# Further reading

### Conventions
### Known Issues
### Change log

```diff
! 0.0.1
# the first version has no changes
```
