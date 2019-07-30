colorparse
==========

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



``colorparse`` is a python package that will read and parse strings with defined color codes, showing their respective colors in the terminal. This way, a string can be easily written, simplifying the work for the user.


Contents
--------

* Installation
* Usage
* List of Color Codes
* Further Reading

Installation
------------

To install, use this command::

   $ pip install colorparse


After this, the package should be ready to use. To upgrade or uninstall, use the following::

   $ pip install --upgrade colorparse
   $ pip uninstall colorparse
   
Usage
-----

A ``color code`` is defined in two parts. The first, is the ``type`` which can be either *foreground* or *background* using a ``;`` (semicolon) or a ``:`` (colon) respectively. Second, comes the ``value`` representing the color that will be displayed.

The ``value`` can be defined letters, another ``type`` character and, if the terminal supports `true color`_, the option to use custom color codes is avaliable (detailed information about the possible values is in the `color code list <https://github.com/tubi-carrillo/colorparse#list-of-color-codes>`_ below).

The following command, will return the string " red box" in the color red (notice the space character at the start of the string)::

   $ colorparse ";r red box"
    red box

This happens because the ``type`` is a semicolon representing foreground colors and the ``value`` is the letter *r*. When the parser reads that, it understands that from there, the color red will be initiated and removes the ``color code``, which didn't include the space after it.

If we were to remove the space character when using the command, then only "ed box" in dark red would be returned, because the parser thinks that ``;rr`` is the code for dark red. To avoid this and having to use unwanted spaces, you can "*close*" a ``color code``.

The following commands will return the same string ("red box") colored in normal red::

   $ colorparse ";r/red box"   
   $ colorparse "/;r/red box"
   $ colorparse "[;r]red box"
   $ colorparse "(;r)red box"

List of Color Codes
-------------------
