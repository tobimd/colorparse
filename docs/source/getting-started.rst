.. _getting-started:

###############
Getting Started
###############

************
Installation
************

To install the package, upgrade and uninstall, do the following commands::

	$ pip install colorparse
	$ pip install --upgrade colorparse
	$ pip uninstall colorparse

***********
Color Codes
***********
Syntax
------
A ``color code`` consists mainly of two parts. The first is the ``type``, which can be either *foreground* or *background*. Secondly there is the ``value``, which represents the color to display.

As an example, we will use (a lot) the foreground color red. This color is represented with: ``;r``, where the ``;`` (semicolon) is the foreground type, and the letter ``r`` is the value for the color red. Then, using the string "``;r`` hello" will return "hello" in red.

We can use background colors as well, with a ``:`` (colon) instead of the foreground type ``;``. That way, "``:r`` hello" would return "hello" with its background in red.

.. tip:: To see the all the available codes, go to the :ref:`list-of-color-codes` section below.

Closing
-------
Sometimes, using the same color as an example, the words that we want to color will start with the same letter as the value. Initiating a darker color, is done by having the value repeated twice, which means that having ``;rred box`` will return ``ed box`` in dark red, because the parser thinks that ``;rr`` is the color for dark red. This may become a problem, so to avoid this, and having to add a space in between where we don't want one, there is the option to "*close*" a color code.

Closing can be done with three items (characters, really). Using normal brackets: ``(`` and ``)``, square brackets: ``[`` and ``]``, or slashes: ``/``, will make them be consumed by the color code. Both types of brackets must be on both sides of the color code, without any ``/`` inside. The ``/`` can be on either side or both if needed. The next examples will show how the use of closure works using the terminal::


	$ colorparse ";rred box"
	ed box             # "ed box" in dark red
 	$
	$ colorparse ";r red box"
	 red box           # " red box" with a space at the start
	$
	$ colorparse ";r/red box"
	red box
	$
	$ colorparse "/;rred box"
	ed box             # "ed box" again
	$
	$ colorparse "/;r/red box"
	red box
	$
	$ colorparse "[;r]red box"
	red box
	$
	$ colorparse "(  ;r  )red box"
	red box
	$
	$ colorparse "[ ;r/ ]redbox"
	[  ]red box        # using / inside, won't make the brackets be absorbed


.. important:: A colored version of these examples can be seen at: :ref:`examples` below.


Finishing
---------

If we want a color to stop being shown, there are two ways of finishing (or ending). 

One way is by initiating another color, for example a foreground blue (``;b``), if there was another foreground color before. Initiating a new color to end a previous one, won't work if both are different types.

The second way is by resetting the colors, which is done by using ``;:`` or ``:;`` (a semicolon followed by a colon, or viceversa). Both work the same, and they reset foreground and background colors at once. Because of that, there is also the code ``;;``, which resets only the foreground colors and ``::`` that resets only the background colors::

	$ colorparse ";r/red box ;b/blue box"
	red box blue box
	$
	$ colorparse ";r:b/foreground red and background blue"
	foreground red and background blue    # both colors appear
	$
	$ colorparse ";r:b/foreground and background stop ;:/here"
	foreground and background stop here   # "here" is not in red nor blue
	$
	$ colorparse ";r:b/only stop ;;/the red color"
	only stop the red color               # "the red color" has blue background

.. important:: A colored version of these examples can be seen at :ref:`examples` below.


Escaping
--------
To escape a color code from being rendered, use a ``\`` (backslash), then::

	$ colorparse "[\;r]red box"
	[;r]red box


Custom Colors
-------------

.. caution:: To use the custom colors: ``;=`` for RGB and ``;#`` for HEX, means that `your terminal supports true color <https://gist.github.com/XVilka/8346728#terminals--true-color>`_.

Both of these codes won't show or work, unless the method ``true_color`` was given the value ``True`` (if you are importing the module) or by using the ``-t`` or ``--true-color`` flags in the terminal. See :ref:`module-content` and :ref:`options` for more information on these.

.. note:: It's important to note, that because background colors do not allow RGB values, the codes ``:=`` and ``:#`` don't exist.

- For RGB, you need to give it **at most** the three values corresponding to red, green and blue, which go from 0 to 255 each one (values that are 0 can be ommited). All of the following examples work::

	$ colorparse -t "[;=255,255,255]white"
	$ colorparse -t "[;=255]red"
	$ colorparse -t "[;=255,,]red"
	$ colorparse -t "[;=255,0,0]red"
	$ colorparse -t "[;=]black"
	$ colorparse -t "[;=,,]black"
	

- For HEX, there needs to be **at most** 6 values. Like before, by pairs these represent red, green and blue, which go from 0 to F each one (zeros can be ommited, though missing ones will be considered to be at the right-most part). The following examples also work::

	$ colorparse -t "[;#FFFFFF]white"
	$ colorparse -t "[;#FF]red"
	$ colorparse -t "[;#FF00]red"
	$ colorparse -t "[;#FF0000]red"
	$ colorparse -t "[;#000000]black"
	$ colorparse -t "[;#]black"

.. _list-of-color-codes:

*******************
List of Color Codes
*******************
.. hint:: To remember easily, the colors available are: ``red``, ``orange``, ``yellow``, ``green``, ``cyan``, ``blue``, ``purple`` and ``magenta``. They all have three variations for the first letter. If it's alone, then it's a normal color; if it's repeated two times, it means that it's a dark color; if it's uppercase, then it's a strong color.

.. table::
    :widths: 10 24 50
    
    +-------------+------------------------+----------------------------------------------------------------------------+
    | **VALUES**  | **NAMES**              | **DESCRIPTION**                                                            |
    +-------------+------------------------+----------------------------------------------------------------------------+
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


.. attention:: Color names with ``*``, cannot be accessed directly through the class ``Color``. They can only be used as a color code in a string (see :ref:`color-class`).

.. attention:: Color names with ``+``, are only available if `your terminal supports true color <https://gist.github.com/XVilka/8346728#terminals--true-color>`_, because their assigned values are transformed to RGB values, and not all terminals support that in `ANSI escape sequences <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

.. _examples:

********
Examples
********

The following examples cover the ones show before, with images. Follow `this link to see more examples <https://github.com/tubi-carrillo/colorparse/blob/master/example/README.md>`_. Note that the exact color shown, may look different depending on which terminal is being used.

.. image:: https://raw.githubusercontent.com/tubi-carrillo/colorparse/master/example/example-getting-started.png
    :target: https://github.com/tubi-carrillo/colorparse/blob/master/example/README.md
    :alt: colored terminal example

