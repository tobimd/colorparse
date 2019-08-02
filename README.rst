##########
colorparse
##########

| |version| |wheel| |docs| |downloads|

.. |version| image:: https://img.shields.io/pypi/v/colorparse?color=dark%20green&style=flat-square
   :target: https://github.com/tubi-carrillo/colorparse#change-log
   :alt: Package Version
  
.. |wheel| image:: https://img.shields.io/pypi/wheel/colorparse?style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Wheel Status
  
.. |docs| image:: https://readthedocs.org/projects/pip/badge/&style=flat-square
   :target: https://colorparse.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
   
.. |downloads| image:: https://img.shields.io/pypi/dd/colorparse?color=yellow&style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Download Count


``colorparse`` is a python package that will read and parse strings with defined color codes, showing their respective colors in the terminal. This way, a string can be easily colored, simplifying the work for the user.


Contents
========

* `Installation <https://github.com/tubi-carrillo/colorparse#installation>`_
* `Usage <https://github.com/tubi-carrillo/colorparse#usage>`_
   - `Initiating a color <https://github.com/tubi-carrillo/colorparse#initiating-a-color>`_
   - `Closing a color <https://github.com/tubi-carrillo/colorparse#closing-a-color>`_
   - `Finishing a color <https://github.com/tubi-carrillo/colorparse#finishing-a-color>`_
   - `Escaping a color <https://github.com/tubi-carrillo/colorparse#escaping-a-color>`_
* `List of Color Codes <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_
* `Documentation <https://github.com/tubi-carrillo/colorparse#documentation>`_
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
   
Usage
=====

A ``color code`` is defined in two parts. The first, is the ``type`` which can be either *foreground* or *background* using a ``;`` (semicolon) or a ``:`` (colon) respectively. Second, comes the ``value`` representing the color that will be displayed.

The ``value`` can be: defined letters, another ``:`` or ``;`` character or for custom colors (if the terminal supports `true color <https://github.com/tubi-carrillo/colorparse#about-true-color>`_, then this option is available) an ``=`` or ``#``. Detailed information about all possible values is in the `color code list <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_ below.

This guide will use the terminal form of this package, but this also applies to the function ``paint``, when the module is imported.

Initiating a color
------------------

The following command, will return the string " red box" in the color red (notice the space character at the start of the string)::

   $ colorparse ";r red box"
    red box

This happens because the ``type`` is a semicolon representing foreground colors and the ``value`` is the letter *r*. When the parser reads that, it understands that from there, the color red will be initiated and removes the ``color code``, which didn't include the space after it.

Closing a color
---------------

If we were to remove the space character when using the command, then only "ed box" in dark red would be returned, because the parser thinks that ``;rr`` is the code for dark red. To avoid this and having to use unwanted spaces, you can "*close*" a ``color code``.

The following commands will return the same string ("red box") colored in normal red::

   $ colorparse ";r/red box"   
   $ colorparse "/;r/red box"
   $ colorparse "[;r]red box"
   $ colorparse "(;r)red box"
   
Note that, the variations for closing a color shown before, cannot be mixed with eachother. This might help to avoid absorbing the brackets when trying to use them for something else. The parser will not replace brackets if they have at least one ``/`` (slash) either at the start or the end of the ``color code`` (with no spaces in between). Some examples are::
   
   $ colorparse "[ ;r/ ]red box"
   [  ]red box
   
   $ colorparse "[ /;r ]red box"
   [  ]red box
   
   $ colorparse "[;r red box]"
    red box]                    # bad!
    
   $ colorparse "[/;r/ red box ]"
   [ red box ]
   
Finishing a color
-----------------

To finish a color, can mean two things: changing to another color, or resetting colors to normal (to the color the terminal uses, which is normally not white). 

To change colors, all is needed is to initiate a new color like before::
   
   $ colorparse ";r/red box ;b/blue box"
   red box blue box

This can be mixed with background colors as well, swapping the ``;`` for a ``:`` (it's worth mentioning that setting a new foreground color when only a background color is initiated won't finish the latter, only the ones of the same ``type`` will affect each other).

Resetting to normal, can be done in three major ways, where one of those has two forms (it is used to stop both background and foreground colors, and every string will have one at the end added by the program). The following strings get the same result, therefore ``;:`` and ``:;`` are interchangeable::

   $ colorparse ":b/;r/both foreground and background colors stop ;:/here"
   $ colorparse ":b/;r/both foreground and background colors stop :;/here"
   
The other two ways are: using ``;;`` to stop only the current foreground color and ``::`` to stop only the current background color::

   $ colorparse ":b/;r/both colors ;;/only the blue background"
   $ colorparse ":b/;r/both colors ::/only the red foreground"
   
Escaping a color
----------------

To escape ``color codes``, add a ``\`` (backslash) to the beggining of it's ``type`` character (the one that determines if it is a background or a foreground color)::

   $ colorparse "[\;r] this text is not red"
   [;r] this text is not red

List of Color Codes
===================

To remember easily, the colors available are: ``red``, ``orange``, ``yellow``, ``green``, ``cyan``, ``blue``, ``purple`` and ``magenta``. They all have three variations for the first letter. If it's alone, then it's a normal color; if it's repeated two times, means that it's a dark color; if it's uppercase, then it's a strong color.

.. table::
    :widths: 10 24 50
    
    +-------------+------------------------+
    | **VALUES**  | **NAMES**              |
    +-------------+------------------------+
    | ``rr``      | DARK_RED               |
    +-------------+------------------------+
    | ``oo``      | DARK_ORANGE            |
    +-------------+------------------------+
    | ``yy``      | DARK_YELLOW            |
    +-------------+------------------------+
    | ``gg``      | DARK_GREEN             |
    +-------------+------------------------+
    | ``cc``      | DARK_CYAN              |
    +-------------+------------------------+
    | ``bb``      | DARK_BLUE              |
    +-------------+------------------------+
    | ``pp``      | DARK_PURPLE            |
    +-------------+------------------------+
    | ``mm``      | DARK_MAGENTA           |
    +-------------+------------------------+
    | ``r``       | RED                    |
    +-------------+------------------------+
    | ``o``       | ORANGE                 |
    +-------------+------------------------+
    | ``y``       | YELLOW                 |
    +-------------+------------------------+
    | ``g``       | GREEN                  |
    +-------------+------------------------+
    | ``c``       | CYAN                   |
    +-------------+------------------------+
    | ``b``       | BLUE                   |
    +-------------+------------------------+
    | ``p``       | PURPLE                 |
    +-------------+------------------------+
    | ``m``       | MAGENTA                |
    +-------------+------------------------+
    | ``R``       | STRONG_RED             |
    +-------------+------------------------+
    | ``O``       | STRONG_ORANGE          |
    +-------------+------------------------+
    | ``Y``       | STRONG_YELLOW          |
    +-------------+------------------------+
    | ``G``       | STRONG_GREEN           |
    +-------------+------------------------+
    | ``C``       | STRONG_CYAN            |
    +-------------+------------------------+
    | ``B``       | STRONG_BLUE            |
    +-------------+------------------------+
    | ``P``       | STRONG_PURPLE          |
    +-------------+------------------------+
    | ``M``       | STRONG_MAGENTA         |
    +-------------+------------------------+
    | ``;:``      | ENDC                   |
    +-------------+------------------------+
    | ``:;``      | ENDC                   |
    +-------------+------------------------+
    | ``;;``      | ENDFC ``*``            |
    +-------------+------------------------+
    | ``::``      | ENDBC ``*``            |
    +-------------+------------------------+
    | ``;=``      | RGB ``*`` ``+``        |
    +-------------+------------------------+
    | ``;#``      | HEX ``*`` ``+``        |
    +-------------+------------------------+

``*`` cannot be accessed directly through the class ``Color``. They can only be used as a ``color code`` in a string.

``+`` only available if the terminal supports `true color <https://en.wikipedia.org/wiki/Color_depth#True_color_(24-bit)>`_, because their assigned values are transformed to RGB values, and not all terminals support having direct RGB colors in `ANSI escape sequences <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

Documentation
=============

Here is the `readthedocs <https://colorparse.readthedocs.io/en/latest/>`_ documentation.

Further Reading
===============

Conventions
-----------

This shall be considered as recomendations, as they allow for a better and faster way of working arround with ``color codes``.

- Use closing options consistently throughout the string(s).
- Prefer the use of closing brackets for large strings and right-side only ``/`` (slash) for smaller strings.
- Avoid using ``;;`` or ``::`` for large strings.
- For custom color codes (RGB and HEX), do not ommit "0" values.
- If using the terminal, and there are many special characters (new lines, tabs, etc), prefer storing the string(s) in a file rather than directly using terminal input (this file can be accessed using the ``-i`` or ``--input-file`` option).
- Avoid using the ``Color`` class directly, unless it's used to redefine color values.
- If the ``change_defaults`` function is used (preferably at the beggining of the program), do not use the function again later in the code. 
- Do not use the ``codes`` function as part of the program (unless it's explicitly intended to be shown).
- Even though spaces are allowed in bracket closing (which is not the case for the ``/``), use as few as possible.
- Use either ``;:`` or ``:;`` consistently (prefer the first one, because the program automatically adds that one, to the end of the strings).

Known Issues
------------

- Special characters do not work as intended for Windows. For now, use input files for their correct usage.

Change Log
----------

\* *the prefixes [t] refer to terminal, [m] for module and [d] for docs only changes, respectively.* *

.. code:: diff

   # version 1.0.0   (2019 - 07 - 30)
   + [t] The use of ``colorparse`` without arguments, results in the usage help being displayed.
   + [t] Grouped the option arguments ``-v`` and ``-c`` as mutually exclusive arguments.
   + [t] Added new optional argument for reading strings from input file(s) with ``-i`` or ``--input-file``.
   + [t] Replaced the optional argument ``-f`` for ``-o`` (``--output-file``).
   + [t] Changed the optional argument for ``overflow`` to ``-O`` (uppercase o) or ``--overflow``.
   + [t] Added support for special characters to be read from the terminal input ``-r`` or ``--read-special``.


   # version 0.0.2   (2019 - 07 - 29)
   + Fixed Windows script file


   # release version 0.0.1   (2019 - 07 - 29)

Examples
--------

Sadly, there is no better way to show this examples without images, so `here <https://github.com/tubi-carrillo/colorparse/tree/master/example>`_ are some (this time with actual color). I will add more examples in a more organized way with future updates.

License
-------

`MIT License <https://github.com/tubi-carrillo/colorparse/blob/master/LICENSE>`_
