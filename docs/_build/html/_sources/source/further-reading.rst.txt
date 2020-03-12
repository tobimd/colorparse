###############
Further Reading
###############

***********
Conventions
***********

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

*************
More Examples
*************

You can see `more examples here <https://github.com/tubi-carrillo/colorparse/tree/master/example>`_.

**********
Change Log
**********

See the `change logs here <https://github.com/tubi-carrillo/colorparse/blob/master/change-log.md>`_.

*******
License
*******
MIT License

Copyright (c) 2019, 2020 Esteban Carrillo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
