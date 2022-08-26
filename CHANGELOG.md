# Change Log

\* *the prefixes [t], [m] and [d] refer to terminal-only, module-only and docs-only changes, respectively.* *

<a name="toc"></a>

- [2.0.0](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-2.0.0)
- [1.1.6](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.6)
- [1.1.5](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.5)
- [1.1.4](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.4)
- [1.1.3](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.3)
- [1.1.2](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.2)
- [1.1.1](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.1)
- [1.1.0](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.1.0)
- [1.0.0](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-1.0.0)
- [0.0.2](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-0.0.2)
- [0.0.1](https://github.com/tobimd/colorparse/blob/master/CHANGELOG.md#version-0.0.1)

<a name="latest"></a>
<a name="version-2.0.0"></a>
<a name="2.0.0"></a>

## version 2.0.0   (2022 - 08 - 06)

<a name="version-1.1.6"></a>
<a name="1.1.6"></a>

## version 1.1.6   (2020 - 03 - 12)

- Fixed color code overflow when ending specific color types consecutively (e.g. "/;g:w/ green text/;; with white background/:: would make this text green", returns the part of the string "would make this text green" with the former color green).

<a name="version-1.1.5"></a>
<a name="1.1.5"></a>

## version 1.1.5   (2020 - 03 - 12)

- Fixed raised error when using RGB or HEX color codes without true color active (now just ignores the color code).

<a name="version-1.1.4"></a>
<a name="1.1.4"></a>

## version 1.1.4   (2020 - 03 - 10)

- Re-did regular expression that obtained color codes, now works properly.
- Fixed ``end`` argument of ``paint`` function.
- Now, by default, ``end`` uses ``Color.ENDC`` before the new line character.
- Fixed the white color being the same as light gray (non-true color version).
- [d] Changed some examples and other descriptions.

<a name="version-1.1.3"></a>
<a name="1.1.3"></a>

## version 1.1.3   (2019 - 08 - 06)

- [m] Fixed ``end`` argument for the ``paint`` function not working properly.

<a name="version-1.1.2"></a>
<a name="1.1.2"></a>

## version 1.1.2   (2019 - 08 - 03)

- color codes are parsed in ``sep`` and ``end`` arguments (``-s`` and ``-e`` arguments in the terminal, respectively)

<a name="version-1.1.1"></a>
<a name="1.1.1"></a>

## version 1.1.1   (2019 - 08 - 03)

- [m] Objects that have a ``__str__`` method (e.g. iterables) can be used in ``paint``.

- [d] Changed documentation, now using rST (sphinx) instead of md (mkdocs).

<a name="version-1.1.0"></a>
<a name="1.1.0"></a>

## version 1.1.0   (2019 - 08 - 01)

- [t] Fixed problem with reading special characters on Windows.

- [t] Improved (and fixed some grammatical errors) in the help menu.
- [t] Replaced ``-r`` (``--read-special``) with ``-I`` (uppercase i) or ``--ignore-special`` (inverted roles).
- [t] Added new optional argument ``-p`` or ``--position``.
- [t] Added new optional argument ``-S`` (uppercase s) or ``--strip``.
- [m] Added more documentation for the functions insde the module (use built-in ``help`` function).
- [d] Created a documentation page.

<a name="version-1.0.0"></a>
<a name="1.0.0"></a>

## version 1.0.0   (2019 - 07 - 30)

- [t] The use of ``colorparse`` without arguments, results in the usage help being displayed.

- [t] Grouped the option arguments ``-v`` and ``-c`` as mutually exclusive arguments.
- [t] Added new optional argument for reading strings from input file(s) with ``-i`` or ``--input-file``.
- [t] Replaced the optional argument ``-f`` for ``-o`` (``--output-file``).
- [t] Changed the optional argument for ``overflow`` to ``-O`` (uppercase o) or ``--overflow``.
- [t] Added support for special characters to be read from the terminal input ``-r`` or ``--read-special``.

<a name="version-0.0.2"></a>
<a name="0.0.2"></a>

## version 0.0.2   (2019 - 07 - 29)

- Fixed Windows script file

<a name="version-0.0.1"></a>
<a name="0.0.1"></a>

## release version 0.0.1   (2019 - 07 - 29)
