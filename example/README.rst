##########
colorparse
##########

| |version| |wheel| |docs|

.. |version| image:: https://img.shields.io/pypi/v/colorparse?color=dark%20green&style=flat-square
   :target: https://github.com/tubi-carrillo/colorparse#change-log
   :alt: Package Version
  
.. |wheel| image:: https://img.shields.io/pypi/wheel/colorparse?style=flat-square
   :target: https://pypi.org/project/colorparse/
   :alt: Wheel Status
  
.. |docs| image:: https://img.shields.io/badge/docs-in%20process-orange?style=flat-square
   :target: https://github.com/tubi-carrillo/colorparse
   :alt: Documentation
----


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
* `Further Reading <https://github.com/tubi-carrillo/colorparse#further-reading>`_

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

The ``value`` can be defined letters, another ``type`` character and, if the terminal supports `true color <https://github.com/tubi-carrillo/colorparse#about-true-color>`_, the option to use custom color codes is avaliable (detailed information about all possible values is in the `color code list <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_ below).

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

To finish a color, can mean two things: to change to another color, or reset to normal (to the color the terminal uses, which is normally not white). 

To change colors, all is needed is to initiate like before::
   
   $ colorparse ";r/red box ;b/blue box"
   red box blue box

This can be mixed with background colors as well, changing the ``;`` to ``:``.

Resetting to normal, can be done in 3 major ways, where 1 of those can be used in two forms (it is used to stop both background and foreground colors). The following two strings have the exact meaning::

   $ colorparse ":b/;r/both foreground and background colors stop ;:/here"
   $ colorparse ":b/;r/both foreground and background colors stop :;/here"
   
The other two ways are: using ``;;`` to stop only the current foreground color and ``::`` to stop only the current background color::

   $ colorparse ":b/;r/both colors ;;/only the blue background"
   $ colorparse ":b/;r/both colors ::/only the red foreground"
   
Escaping a color
----------------

To escape ``color codes``, add a ``\`` (backslash) to the beggining of it's ``type`` character (the one that determines if it is a background or a foreground color)::

   $ colorparse "[\;r] this text is not red"
   [\;r] this text is not red

List of Color Codes
===================

* the ones marked with a start (the last four), cannot be accessed directly through the class ``Color``. They can only be used as a ``color code`` in a string.

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
    | ``;;``      | ENDFC*                 |
    +-------------+------------------------+
    | ``::``      | ENDBC*                 |
    +-------------+------------------------+
    | ``;=``      | RGB*                   |
    +-------------+------------------------+
    | ``;#``      | HEX*                   |
    +-------------+------------------------+
