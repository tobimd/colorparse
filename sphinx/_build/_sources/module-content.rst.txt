.. _module-content:

##############
Module Content
##############

.. _color-class:

***********
Color class
***********

When this module is imported, you will have access to individual colors with the ``Color`` class. 

To get the value of a color, one must use the following structure: ``Color.<type>.<color name>`` such as ``Color.foreground.DARK_RED``.

The ``<type>`` can be either "foreground" or "background" and ``<color name>`` can be any of the color codes (that don't have a ``*``) in the :ref:`list-of-color-codes` section, in :ref:`getting-started`. An exception to that structure, is the ``ENDC`` color code, which is accessed with ``Color.ENDC``.

.. hint:: Generally, you needn't use this class unless it is to change the color values manually.

*******
Methods
*******

paint
-----

.. function:: paint(\*value, \*\*options)
.. function:: paint(value, ..., print=True, ret=True, overflow=False, sep=' ', end='\n', file=sys.stdout, flush=False)



Returns a string that will have color codes converted to ANSI escape sequences. 

Having ``print`` as ``False``, makes the arguments ``end``, ``file`` and ``flush`` to not be considered whatever their values may be, because those are only used when printing.

When there is more than one ``value`` argument, and ``overflow`` is ``True``, any unfinished color will pass through to other strings. Otherwise, colors will be finished at the end of each string.

It's worth noting that regardless of the value this argument has, the function will **always** finish all color codes at the end of the last string (the same as adding a ``;:``).

.. csv-table::
        :file: paint-table.csv
        :header-rows: 1
        :widths: 7, 20

codes
-----

.. function:: codes()

Prints a list of all the color codes available. It also displays what the colors look as background type and foreground type.


true\_color
-----------

.. function:: true_color(value=None)

Changes the global value for true color. When set to ``True``, it means that the set of **foreground colors** will be using RGB values directly for each ANSI escape sequence. This does not apply to the background colors, as they do not allow RGB values in their codes. Be aware that not all terminals support true colors in ANSI escape sequences, so by default it's set to false at the start.

When no argument is given, it returns the current state for the global value.

.. csv-table::
        :file: true-color-table.csv
        :header-rows: 1
        :widths: 7, 20

change\_defaults
----------------

.. function:: change_defaults(fn, \*\*kwargs)



This function is meant to be used at the beggining of the program, to set permanent default values. This way, it helps to avoid having to constantly set the same arguments that would otherwise be omitted. The ``kwargs`` argument recieves one or more ``key``/``value`` pairs for the function ``fn``.

It was designed to help both for future functions that may be added and to make lines of code shorter.

.. csv-table::
        :file: change-defaults-table.csv
        :header-rows: 1
        :widths: 7, 20
