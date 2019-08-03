# Index
- [Color class](#color-class)
- [Methods](#methods)
	- [paint](#paint)
	- [codes](#codes)
	- [true\_color](#true95color)
	- [change\_defaults](#change95defaults)


# Color class
When this module is imported, you will have access to individual colors with the ``Color`` class. To get the color, one must use the following structure: ``Color.<type>.<color name>``, where ``<type>`` can be either "foreground" or "background" and ``<color name>`` can be any of the color codes (that don't have a ``*``) in the [List of Color Codes section](index.md#list-of-color-codes) in [Getting Started](index.md). An exception to that structure, is the `ENDC` color code, which is accessed with `Color.ENDC`.

```python
>>> from colorparse import Color
>>> 
>>> Color.foreground.DARK_RED
'\x1b[38;5;88m'
>>> 
>>> Color.ENDC
'\x1b[0m'
```

# Methods

## paint

```python
paint(strings, ..., print=True, ret=True, overflow=False, sep=' ', end='\n', file=sys.stdout, flush=False)
```

Returns a string that will have color codes converted to ANSI escape sequences. 

Having `print` as `False`, makes the arguments `end`, `file` and `flush` to not be considered whatever their values may be, because those are only used when printing.

When there is more than one string and the argument `overflow` is `True`, any unfinished color will pass through to other strings. Otherwise, colors will be finished at the end of each string.

It's worth noting that regardless of the value this argument has, the function will **always** finish all color codes at the end of the last string (the same as adding a `;:`).

| **Argument**        | **Description**                                                      |
|:--------------------|:---------------------------------------------------------------------|
| strings             | One or more ``str`` objects to be parsed.                            |
| print=`True`        | If true, the obtained string will be printed.                        |
| ret=`True`          | If true, the obtained string will be returned.                       |
| overflow=`False`    | If true, allow unfinished colors to overflow onto other strings.     |
| sep=`' '`           | Inserted between the given strings.                                  |
| end=`'\n'`          | Appended after the last string (when it's printed)                   |
| file=`sys.stdout`   | A file-like object (stream).                                         |
| flush=`False`       | Whether to forcibly flush the stream (when the strings are printed). |

Example: 

```python
>>> from colorparse import paint
>>>   
>>>   
>>> # with overflow=True, the second string will also be shown with a red foreground color
>>> paint(";r/red text", "on both strings", overflow=True, ret=False)
red text on both strings
>>>  
>>> # with overflow=False (default), the second string wont't have the color red.
>>> paint(";r/red text", "without color here", ret=False)
red text without color here
```

## codes

```python
codes()
```

Prints a list of all the color codes available. It also displays what the colors look as background type and foreground type.


## true\_color

```python
true_color(value=None)
```

Changes the global value for true color. When set to `True`, it means that the set of **foreground colors** will be using RGB values directly for each ANSI escape sequence. This does not apply to the background colors, as they do not allow RGB values in their codes. Be aware that not all terminals support true colors in ANSI escape sequences, so by default it's set to false at the start.

When no argument is given, it returns the current state for the global value.


| **Argument**        | **Description**                                                      |
|:--------------------|:---------------------------------------------------------------------|
| value=`None`        | If true color should be activated or not, using boolean arguments.   |


## change\_defaults

```python
change_defaults(fn, **kwargs)
```

This function is meant to be used at the beggining of the program, to set permanent default values. This way, it helps to avoid having to constantly set the same arguments that would otherwise be omitted. The `kwargs` argument recieves one or more `key`/`value` pairs for the function `fn`.

It was designed to help both for future functions that may be added and to make lines of code shorter.

| **Argument**        | **Description**                                                               |
|:--------------------|:------------------------------------------------------------------------------|
| fn                  | Either the name or the function itself, from which the  changes for default values will be applied |
| kwargs              | Key/value pairs for each default argument to set.                           |

Example:

```python
>>> from colorparse import paint, change_defaults
>>>  
>>>  
>>> # the paint function has "ret" set as True by default
>>> paint("printed text only", ret=False)
printed text only
>>>  
>>>  
>>> # doing this, becomes the same as before without writing "ret=False" all the time
>>> change_defaults(paint, ret=False)
>>> 
>>> paint("printed text only")
printed text only
```
