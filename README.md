# Colorparse

_current version: v0.0.1_

This unoriginal package let's the user generate strings with ansi color escape sequences (which are "*codes*" that tell the terminal what color to display the proceeding characters, and much more: <https://wikipedia.org/wiki/ANSI_escape_code>)

Colorparse will simplify the work by reading it's self-defined "*color codes*" inside the strings (e.g. " ;r " will produce the color red).

# Index
- [Installation](https://github.com/tubi-carrillo/colorparse#installation)
- [Use as an imported module](https://github.com/tubi-carrillo/colorparse#use-as-imported-module)
- [Use in terminal](https://github.com/tubi-carrillo/colorparse#use-in-terminal)
- [Color codes](https://github.com/tubi-carrillo/colorparse#color-codes)
- [Further reading](https://github.com/tubi-carrillo/colorparse#further-reading)

# Installation

# Using colorparse as an imported module

When importing `colorparse`, the function `paint` is the most important one. This function is the one that will return and/or print the color coded string.

The following functions are the ones that can be used when importing this module:

- **paint:**

`paint(string, ..., out=True, overflow=False, sep=' ', end='\n', file=sys.stdout, flush=False)`
`paint(*string, **options)`

Returns a string that will have color codes converted to real ANSI color escape sequences (if `out` is `False`, then the string won't be printed and the arguments: `end`, `file` and `flush` won't be considered whatever their values may be, because those are for printing purposes only).

Color codes can be "*closed*" which means that any color code can have extra characters to help the readability (e.g. the color code for red " ;r " can be closed with "\[ ;r \]", "/ ;r /", " ;r/ ", etc. where all mean the same). Closing a color code can be done by adding square brackets or normal parenthesis in both sides of the color code. A "/" (slash) can be on one side or both, but it's important to know that only one type of closing can be used for a color code (i.e. having "\[ ;r/ \]" will only convert " ;r/ " and leave the square brackets as they are).

Color codes can be "*ended*" (or "*finished*") which means that after a certain color has been initialized, if it's imperative to stop that color, the use of " ;: " or " :; " (semicolon followed by a colon, or viceversa) will finish both foreground **and** background colors (this works even if only one type of color, like a foreground color, has been initialized). One can also use " ;; " (two semicolons) to end only the current **foreground color** and " :: " (two colons) to end only the current **background color**. All of the strings will have a " ;: " (a semicolon and colon) added to the end of it, so if the option `overflow` is `False`, then this is added to the end of each string given **and** the end of the whole.

Finally, color codes can also be escaped with a "\\" (backslash) to make the program ignore it.

# Using colorpase in the terminal

# Color codes

# Further reading

### Conventions
### Known Issues
### Change log

```diff
! 0.0.1
# the first version has no changes
```
