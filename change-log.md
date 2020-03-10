# Change Log
\* *the prefixes [t], [m] and [d] refer to terminal-only, module-only and docs-only changes, respectively.* *

- [1.1.4](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-113---2020---03---10)
- [1.1.3](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-113---2019---08---06)
- [1.1.2](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-112---2019---08---03)
- [1.1.1](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-111---2019---08---03)
- [1.1.0](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-110---2019---08---01)
- [1.0.0](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-100---2019---07---30)
- [0.0.2](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#version-002---2019---07---29)
- [0.0.1](https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md#release-version-001---2019---07---29)


## version 1.1.4   (2020 - 03 - 10)
- Re-did regular expression that obtained color codes, now works properly.
- Fixed ``end`` argument of ``paint`` function.
- Now, by default, ``end`` uses ``Color.ENDC`` before the new line character.
- Fixed the white color being the same as light gray (non-true color version).


## version 1.1.3   (2019 - 08 - 06)
- [m] Fixed ``end`` argument for the ``paint`` function not working properly.


## version 1.1.2   (2019 - 08 - 03)
+ color codes are parsed in ``sep`` and ``end`` arguments (``-s`` and ``-e`` arguments in the terminal, respectively)


## version 1.1.1   (2019 - 08 - 03)
+ [m] Objects that have a ``__str__`` method (e.g. iterables) can be used in ``paint``.
+ [d] Changed documentation, now using rST (sphinx) instead of md (mkdocs).


## version 1.1.0   (2019 - 08 - 01)
+ [t] Fixed problem with reading special characters on Windows.
+ [t] Improved (and fixed some grammatical errors) in the help menu.
+ [t] Replaced ``-r`` (``--read-special``) with ``-I`` (uppercase i) or ``--ignore-special`` (inverted roles).
+ [t] Added new optional argument ``-p`` or ``--position``.
+ [t] Added new optional argument ``-S`` (uppercase s) or ``--strip``.
+ [m] Added more documentation for the functions insde the module (use built-in ``help`` function).
+ [d] Created a documentation page.


## version 1.0.0   (2019 - 07 - 30)
+ [t] The use of ``colorparse`` without arguments, results in the usage help being displayed.
+ [t] Grouped the option arguments ``-v`` and ``-c`` as mutually exclusive arguments.
+ [t] Added new optional argument for reading strings from input file(s) with ``-i`` or ``--input-file``.
+ [t] Replaced the optional argument ``-f`` for ``-o`` (``--output-file``).
+ [t] Changed the optional argument for ``overflow`` to ``-O`` (uppercase o) or ``--overflow``.
+ [t] Added support for special characters to be read from the terminal input ``-r`` or ``--read-special``.


## version 0.0.2   (2019 - 07 - 29)
+ Fixed Windows script file


## release version 0.0.1   (2019 - 07 - 29)
