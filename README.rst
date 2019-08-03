##########
colorparse
##########

| |version| |wheel| |docs| |downloads| |python|

.. |version| image:: https://img.shields.io/pypi/v/colorparse?color=dark%20green&style=flat-square
   :target: https://github.com/tubi-carrillo/colorparse#change-log
   :alt: Package Version
  
.. |wheel| image:: https://img.shields.io/pypi/wheel/colorparse?style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Wheel Status
  
.. |docs| image:: https://readthedocs.org/projects/colorparse/badge/?version=latest&style=flat-square
   :target: https://colorparse.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
   
.. |downloads| image:: https://img.shields.io/pypi/dd/colorparse?color=yellow&style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Download Count

.. |python| image:: https://img.shields.io/badge/python-3.6%20%7C%203.7-blue?style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Python Version


``colorparse`` is a python package that will read and parse strings with defined color codes, showing their respective colors in the terminal. This way, a string can be easily colored, simplifying the work for the user.


Contents
========

* `Installation <https://github.com/tubi-carrillo/colorparse#installation>`_
* `Documentation <https://github.com/tubi-carrillo/colorparse#documentation>`_
   - `About Color Codes <https://github.com/tubi-carrillo/colorparse#about-color-codes>`_
   - `Using as an import <https://github.com/tubi-carrillo/colorparse#using-as-an-import>`_
   - `Using from the terminal <https://github.com/tubi-carrillo/colorparse#using-from-the-terminal>`_
* `List of Color Codes <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_
* `Further Reading <https://github.com/tubi-carrillo/colorparse#further-reading>`_
   - `Conventions <https://github.com/tubi-carrillo/colorparse#conventions>`_
   - `Known Issues <https://github.com/tubi-carrillo/colorparse#known-issues>`_
   - `Change Log <https://github.com/tubi-carrillo/colorparse#change-log>`_
   - `Examples <https://github.com/tubi-carrillo/colorparse#examples>`_
   - `License <https://github.com/tubi-carrillo/colorparse#license>`_

Installation
============

To install, use this command::

   $ pip install colorparse


After this, the package should be ready to use. To upgrade or uninstall, use the following::

   $ pip install --upgrade colorparse
   $ pip uninstall colorparse
   
   
Documentation
=============

Here will be described the most important parts of this package, for the full documentation, visit the `readthedocs <https://colorparse.readthedocs.io/en/latest/>`_ page.

About color codes
-----------------

A ``color code`` is defined in two parts. The first, is the ``type`` which can be either *foreground* or *background* using a ``;`` (semicolon) or a ``:`` (colon) respectively. Second, comes the ``value`` representing the color that will be displayed.

The ``value`` can be: defined letters, another ``:`` or ``;`` character or for custom colors ``=`` and ``#``. Detailed information about all possible values is in the `color code list <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_ below.

- A color is initiated when we use a color code. The following command, will return the string " red box" in red (notice the space character at the start of the string)::

   $ colorparse ";r red box"
    red box

This gets clored in red, because the ``type``, is a semicolon which represents foreground colors, and the ``value`` is the letter *r*. When the parser reads that, it understands that from there, the color red will be initiated and removes the ``color code``, which didn't include the space after it.

- Closing a color code (optional), means that it has surrounding characters which separate it from the rest of the string. The following commands will return the same string ("red box") colored in normal red::

   $ colorparse ";r/red box"   
   $ colorparse "/;r/red box"
   $ colorparse "[;r]red box"
   $ colorparse "(;r)red box"
   
Note that, the variations for closing a color shown before, cannot be mixed with eachother. This might help to avoid absorbing the brackets when trying to use them for something else. The parser **will not replace brackets if they have at least one ``/`` (slash) either at the start or the end** of the ``color code`` (with no spaces in between).
   
- To finish a color, can mean two things: initiating another color, or resetting colors to normal (to the color the terminal uses, which is normally not white). 

Note tha background colors can be used as well, swapping the ``;`` for a ``:`` (it's worth mentioning that setting a new foreground color when only a background color is initiated won't finish the latter, only the ones of the same ``type`` will affect each other).

Resetting to normal, can be done in three major ways, where one of those has two forms (it is used to stop both background and foreground colors, and every string will have one at the end added by the program). The following strings get the same result, therefore ``;:`` and ``:;`` are interchangeable::

   $ colorparse ":b/;r/both foreground and background colors stop ;:/here"
   $ colorparse ":b/;r/both foreground and background colors stop :;/here"
   
The other two ways are: using ``;;`` to stop only the current foreground color and ``::`` to stop only the current background color::

   $ colorparse ":b/;r/both colors ;;/only the blue background"
   $ colorparse ":b/;r/both colors ::/only the red foreground"
   
- To escape ``color codes``, add a ``\`` (backslash) immediately before the ``type`` (the one that determines if it is a background or a foreground color)::

   $ colorparse "[\;r] this text is not red"
   [;r] this text is not red

* To use custom colors with: ``;=`` for RGB and ``;#`` for HEX, means that `your terminal supports true color <https://gist.github.com/XVilka/8346728#terminals--true-color>`_, and that the method ``true_color`` was given the value ``True`` (if you are `importing the module <https://colorparse.readthedocs.io/en/latest/source/module-content.html#true-color>`_) or by using ``-t`` or ``--true-color`` flags `from the terminal <https://colorparse.readthedocs.io/en/latest/source/terminal.html#options>`_. All of the following examples work::

    $ colorparse -t "[;=255,255,255]white"
    $ colorparse -t "[;=255]red"
    $ colorparse -t "[;=255,,]red"
    $ colorparse -t "[;=255,0,0]red"
    $ colorparse -t "[;=]black"
    $ colorparse -t "[;=,,]black"

    $ colorparse -t "[;#FFFFFF]white"
    $ colorparse -t "[;#FF]red"
    $ colorparse -t "[;#FF00]red"
    $ colorparse -t "[;#FF0000]red"
    $ colorparse -t "[;#000000]black"
    $ colorparse -t "[;#]black"
   
Using as an import
------------------

The most important function is ``paint``, which is defined as follows::

   paint(*value, **options)
   paint(value, ..., print=True, ret=True, overflow=False, sep=' ', end='n', file=sys.stdout, flush=False)
   
This function returns a single string which will have all the color codes converted to ANSI escape sequences. **It will always finish color codes at the end**.

+-------------+------------------------------------------------------------------------+
| **ARGUMENT**| **DESCRIPTION**                                                        |
+=============+========================================================================+
| ``value``   | One or more strings to be parsed.                                      |
+-------------+------------------------------------------------------------------------+
| ``print``   | If True, the obtained string will be printed.                          |
+-------------+------------------------------------------------------------------------+ 
| ``ret``     | If True, the obtained string will be returned.                         |
+-------------+------------------------------------------------------------------------+
| ``overflow``| If true, allow unfinished colors to overflow onto other stirngs.       |
+-------------+------------------------------------------------------------------------+ 
| ``sep``     | Inserted between the given values.                                     |
+-------------+------------------------------------------------------------------------+
| ``end``     | Appended after the last value (when it’s printed).                     |
+-------------+------------------------------------------------------------------------+
| ``file``    | A file-like object (stream).                                           |
+-------------+------------------------------------------------------------------------+
| ``flush``   | Whether to forcibly flush the stream (when the strings are printed).   |
+-------------+------------------------------------------------------------------------+

Using from the terminal
-----------------------

The usage is as follows::

   usage: colorparse [options] [string ...] [input files ...]

- The options are

+------------------------------+------------------------------------------------------------------------+----------------+
| **ARGUMENT**                 | **DESCRIPTION**                                                        | **DEFAULT**    |
+==============================+========================================================================+================+
| ``-t``, ``--true-color``     | Use of RGB values for the color escape sequences.                      | ``False``      |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-s``, ``--sep``            | Specify what to use to separate string arguments.                      | ``' '``        |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-e``, ``--end``            | Specify what to use at the end of the printed string.                  | ``'\n'``       |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-o``, ``--output-file``    | Append obtained string to a file (stream).                             | ``sys.stdout`` |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-O``, ``--overflow``       | Make colors overflow to other strings.                                 | ``False``      |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-I``, ``--ignore-special`` | Ignore special characters (new line, tab, etc).                        | ``False``      |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-S``, ``--strip``          | Remove leading and trailing characters from input files.               | ``None``       |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-p``, ``--position``       | Place all strings after the nth input file.                            | ``0``          |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-h``, ``--help``           | Show a help menu and exit.                                             |                |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-c``, ``--codes``          | Show the list of color codes and exit.                                 |                |
+------------------------------+------------------------------------------------------------------------+----------------+
| ``-v``, ``--version``        | Show the current version of the module and exit.                       |                |
+------------------------------+------------------------------------------------------------------------+----------------+

- The ``string`` arguments can be 0 or more.

- For the ``input files``, even though these are optional as well, any proceeding arguments after using the ``-i`` or ``--input-file`` flags will be considered as files to open. For that reason, it's recommended to use after any ``string``, to avoid getting an error for missing files.

List of Color Codes
===================

To remember easily, the colors available are: ``red``, ``orange``, ``yellow``, ``green``, ``cyan``, ``blue``, ``purple`` and ``magenta``. They all have three variations for the first letter. If it's alone, then it's a normal color; if it's repeated two times, means that it's a dark color; if it's uppercase, then it's a strong color.

.. table::
    :widths: 10 24 50
    
    +-------------+------------------------+----------------------------------------------------------------------------+
    | **VALUES**  | **NAMES**              | **DESCRIPTION**                                                            |
    +=============+========================+============================================================================+
    | ``rr``      | DARK_RED               |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``oo``      | DARK_ORANGE            |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``yy``      | DARK_YELLOW            |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``gg``      | DARK_GREEN             |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``cc``      | DARK_CYAN              |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``bb``      | DARK_BLUE              |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``pp``      | DARK_PURPLE            |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``mm``      | DARK_MAGENTA           |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``r``       | RED                    |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``o``       | ORANGE                 |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``y``       | YELLOW                 |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``g``       | GREEN                  | Colors that can be preceeded either                                        |
    +-------------+------------------------+                                                                            +
    | ``c``       | CYAN                   | by a ``;`` (semicolon) or a ``:`` (colon)                                  |
    +-------------+------------------------+                                                                            +
    | ``b``       | BLUE                   |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``p``       | PURPLE                 |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``m``       | MAGENTA                |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``R``       | STRONG_RED             |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``O``       | STRONG_ORANGE          |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``Y``       | STRONG_YELLOW          |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``G``       | STRONG_GREEN           |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``C``       | STRONG_CYAN            |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``B``       | STRONG_BLUE            |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``P``       | STRONG_PURPLE          |                                                                            |
    +-------------+------------------------+                                                                            +
    | ``M``       | STRONG_MAGENTA         |                                                                            |
    +-------------+------------------------+----------------------------------------------------------------------------+
    | ``;:``      | ENDC                   | Ends both foreground and background colors                                 |
    +-------------+------------------------+----------------------------------------------------------------------------+
    | ``:;``      | ENDC                   | Ends both foreground and background colors                                 |
    +-------------+------------------------+----------------------------------------------------------------------------+
    | ``;;``      | ENDFC ``*``            | Ends only foreground colors                                                |
    +-------------+------------------------+----------------------------------------------------------------------------+
    | ``::``      | ENDBC ``*``            | Ends only background colors                                                |
    +-------------+------------------------+----------------------------------------------------------------------------+
    | ``;=``      | RGB ``*`` ``+``        | Reads RGB values separated with a ``,`` (comma)                            |
    +-------------+------------------------+----------------------------------------------------------------------------+
    | ``;*``      | HEX ``*`` ``+``        | Reads hexadecimal values for RGB                                           |
    +-------------+------------------------+----------------------------------------------------------------------------+


``*`` cannot be accessed directly through the class ``Color``. They can only be used as a color code in a string (see `Color Class <https://colorparse.readthedocs.io/en/latest/source/module-content.html#color-class>`_ in the documentation).

``+`` only available if `your terminal supports true color <https://gist.github.com/XVilka/8346728#terminals--true-color>`_, because their assigned values are transformed to RGB values, and not all terminals support having direct RGB colors in `ANSI escape sequences <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

Further Reading
===============

Conventions
-----------

The following shall be considered as recommendations only. These are for a better and faster way of working arround with color codes.

- Use closing options consistently throughout the string(s).
- Prefer the use of closing brackets for large strings and right-side only ``/`` (slash) for smaller strings.
- When two or more color codes are side by side, prefer adding a `/` (slash) on both ends of the group, instead of each one.
- Avoid using ``;;`` or ``::`` for large strings.
- For custom color codes (RGB and HEX), do not ommit "0" values.
- If using the terminal, and there are many special characters (new lines, tabs, etc), prefer storing the string(s) in a file rather than directly using terminal input (these files can be accessed using the ``-i`` or ``--input-file`` option).
- Avoid using the ``Color`` class directly, unless it's used to redefine color values.
- If the ``change_defaults`` function is used (preferably at the beggining of the program), do not use the function again later in the code. 
- Do not use the ``codes`` function as part of the program (unless it's explicitly intended to be shown).
- Even though spaces are allowed in bracket closing (which is not the case for the ``/``), use as few as possible.
- Use either ``;:`` or ``:;`` consistently.

Known Issues
------------

\* *there's nothing to show yet* *

Change Log
----------

\* *the prefixes [t], [m] and [d] refer to terminal-only, module-only and docs-only changes, respectively.* *

Too see previous versions go to the `change-log.md <https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md>`_ file.

.. code:: diff

   # version 1.1.1   (2019 - 08 - 03)
   + [m] Objects that have a "__str__" method (e.g. iterables) can be used in "paint".
   + [d] Changed documentation, now using rST (sphinx) instead of md (mkdocs).

Examples
--------

Sadly, there is no better way to show this examples without images, so `here are some <https://github.com/tubi-carrillo/colorparse/blob/master/example/README.md>`_ (this time with actual color). I will add more examples in a more organized way with future updates.

License
-------

`MIT License <https://github.com/tubi-carrillo/colorparse/blob/master/LICENSE>`_
