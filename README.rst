##########
colorparse
##########

| |version| |wheel| |docs| |python| |change log|

.. |version| image:: https://img.shields.io/pypi/v/colorparse?color=dark%20green&style=flat-square
   :target: https://pypi.org/project/colorparse
   :alt: Package Version
  
.. |wheel| image:: https://img.shields.io/pypi/wheel/colorparse?style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Wheel Status
  
.. |docs| image:: https://readthedocs.org/projects/colorparse/badge/?version=latest&style=flat-square
   :target: https://colorparse.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |python| image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue?style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Python Version
   
.. |change log| image:: https://img.shields.io/badge/change%20log-v1.1.5-lightgrey?style=flat-square
   :target: https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#latest
   :alt: Project's Change Log


``colorparse`` is a python package that will read and parse strings with defined color codes, showing their respective colors in the terminal. This way, a string can be easily colored, simplifying the work for the user.

For the time being, this package has been tested only for python 3.6, 3.7 and 3.8 (if it works fine for other versions, `let me know <https://github.com/tubi-carrillo/colorparse/issues>`_).


Contents
========

* `Installation <https://github.com/tubi-carrillo/colorparse#installation>`_
* `Documentation <https://github.com/tubi-carrillo/colorparse#documentation>`_
   - `About Color Codes <https://github.com/tubi-carrillo/colorparse#about-color-codes>`_
   - `Examples <https://github.com/tubi-carrillo/colorparse#examples>`_
* `List of Color Codes <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_
* `Further Reading <https://github.com/tubi-carrillo/colorparse#further-reading>`_
   - `Conventions <https://github.com/tubi-carrillo/colorparse#conventions>`_
   - `Known Issues <https://github.com/tubi-carrillo/colorparse#known-issues>`_
   - `Change Log <https://github.com/tubi-carrillo/colorparse#change-log>`_
   - `License <https://github.com/tubi-carrillo/colorparse#license>`_

Installation
============

To install the package, upgrade and uninstall, do the following commands::

	$ pip install colorparse
	$ pip install --upgrade colorparse
	$ pip uninstall colorparse
   
   
Documentation
=============

Here will be described how color codes work for both terminal and module uses, for the full documentation, please `visit the readthedocs page <https://colorparse.readthedocs.io/en/latest/>`_.

About color codes
-----------------

A ``color code`` has two parts: the ``type`` (``;`` for *foreground* and ``:`` for *background*) and the ``value``.

- A color is initiated when we use a color code. The following command, will return the string " red color" in red (notice the space character at the start of the string)::

   $ colorparse ";r red color"
    red color

  The ``value`` for that code was the letter ``r``. When the parser reads that, it understands that from there, the color red will be initiated and then removes the ``;r`` (which didn't include the space after it).

- Closing a color code, is optional, and means that it has surrounding characters which separate it from the rest of the string. The following commands will return the same string ("red color") colored in normal red::

   $ colorparse ";r/red color"   
   $ colorparse "/;r/red color"
   $ colorparse "[;r]red color"
   $ colorparse "( ;r )red color"
   
- To finish a color, can mean two things: initiating another color, or resetting them to normal (to what the terminal uses, which is normally not white). Resetting to normal, can be done in three major ways, using: ``;:`` to stop both background and foreground colors (or ``:;``, interchangable), ``;;`` to stop only the foreground colors and ``::`` to stop only the background colors::

   $ colorparse "/:b;r/both foreground and background colors stop/;: here"
   $ colorparse "/:b;r/both foreground and background colors stop/:; here"
   $ colorparse "/:b;r/both colors/;; only the blue background"
   $ colorparse "/:b;r/both colors/:: only the red foreground"
   
- To escape ``color codes``, add a ``\`` (backslash) immediately before the ``type``::

   $ colorparse "[\;r] this color is not red"
   [;r] this color is not red

- For custom colors, use ``;=`` for RGB values and ``;#`` for HEX values (these color codes may not work on all terminals, see `the custom colors section in the docs <https://colorparse.readthedocs.io/en/latest/source/getting-started.html#custom-colors>`_ for more information). Note that empty values will be considered as ``0``::

    $ colorparse -t "[;=255]red"
    $ colorparse -t "[;=255,,]red"
    $ colorparse -t "[;=255,0,0]red"
    $ colorparse -t "[;=]black"

    $ colorparse -t "[;#FF]red"
    $ colorparse -t "[;#FF00]red"
    $ colorparse -t "[;#FF0000]red"
    $ colorparse -t "[;#]black"
   
Examples
--------

`Here are more examples <https://github.com/tubi-carrillo/colorparse/blob/master/example/README.md>`_ with actual colors.

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
    | ``;#``      | HEX ``*`` ``+``        | Reads hexadecimal values for RGB                                           |
    +-------------+------------------------+----------------------------------------------------------------------------+


``*`` cannot be accessed directly through the class ``Color``. They can only be used as a color code in a string (see `Color Class <https://colorparse.readthedocs.io/en/latest/source/module-content.html#color-class>`_ in the documentation).

``+`` only available if `your terminal supports true color <https://gist.github.com/XVilka/8346728#terminals--true-color>`_, because their assigned values are transformed to RGB values, and not all terminals support having direct RGB colors in `ANSI escape sequences <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

Further Reading
===============

Conventions
-----------

The following shall be considered as recommendations only. These are for a better and faster way of working arround with color codes according to me.

- Use closing options consistently throughout the string(s).
- Prefer the use of closing brackets for large strings and ``/`` (slash) for smaller strings.
- Prefer placing a right-side only ``/`` when using regular color codes (e.g. ";r/red color"), and conversely, place a left-side only ``/`` when using ending color codes (e.g. ";r/red color/;:").
- When two or more color codes are side by side, prefer adding a ``/`` (slash) on both ends of the group, instead of each one (e.g. "/;r:b/red and blue").
- Prefer sticking the "slash-closed" color codes to other strings on the same side the ``/`` is on. For example, do not do "hello;r/ there" and instead do "hello ;r/there".
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

\* *there is nothing to show yet* \*

Change Log
----------

\* *the prefixes [t], [m] and [d] refer to terminal-only, module-only and docs-only changes, respectively.* *

Too see previous versions go to the `change-log.md <https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md>`_ file.

.. code:: diff

   ## version 1.1.5   (2020 - 03 - 12)
   + Fixed raised error when using RGB or HEX color codes without true color active (now jus ignores the color code).

License
-------

`MIT License <https://github.com/tubi-carrillo/colorparse/blob/master/LICENSE>`_
