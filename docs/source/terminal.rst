##############
Terminal Usage
##############

To better understand how to use the colorparse command, we will simplify things by separating it in four parts. For the full version of the help menu, you can use the flags ``-h`` or ``--help`` in the terminal, or go to the :ref:`help-message` below.

.. code-block:: console

        usage: colorparse [options] [string ...] [input files ...]

.. _options:

*******
options
*******

There are the following options available:

.. csv-table::
        :file: options-table.csv
        :header-rows: 1
        :widths: 15, 30, 10

.. note:: Special characters are: ``\n`` (new line), ``\r`` (carriage return), ``\t`` (horizontal tab), ``\v`` (vertical tab), ``\a`` (bell), ``\b`` (backspace) and ``\f`` (formfeed).

Most of these optional arguments work exactly the same as the functions seen before. Here are a few that need some explanation:

- ``-I``, ``--ignore-special``

  This option will ignore special characters and return the strings as if those characters were escaped.
  
  |
- ``-S``, ``--strip``

  Just like the built-in ``strip`` method for strings, having the strip flag will remove specified leading and trailing characters from all input files. If no character is given, then the default value ``None`` means that whitespaces will be removed. 
  
  To specify which characters to strip, the string should only have them without spaces or separators. For example, having "abc" will remove all combinations of those 3 characters.

  .. important:: If possible, this argument will try to use the proceeding value. To use this flag without arguments, it must be either before another flag (e.g. "-I -t"), after another flag's argument (with the exception of ``--input-file`` as we will discuss it later) or at the end of the terminal command.
  
  |
- ``-p``, ``--position``

  By default, any strings given will be added before input files. With this option, you can choose in which position those strings should be in relation to the input files. Works like the built-in ``insert`` method for lists, including the option to have negative indexes.
  
  |

******
string
******

The input strings (0 or more).

.. note:: If no arguments are given whatsoever (both the strings and optional arguments), the program will output to the terminal a small help menu about the usage.

***********
input files
***********

There is the option to read and parse color codes from external files. Using either ``-i`` or ``--input-file`` flags, the proceeding arguments will be considered as the files to open.

Even though this flag can be used before the ``string`` arguments (because it's an optional argument, it can be technically used anywhere), doing so will make the program think that anything that follows said flag, are files to look for, which may not be true if some of those values are actually ``string`` arguments. If a file doesn't exist, it will raise an error, so for this reason, it's recommended to add this flag at the end or after adding all ``string`` arguments.

.. _help-message:

************
help message
************

The following is what the terminal shows when using the help flags:

.. code-block:: console

	usage: colorparse [-h] [-c] [-v] [-t] [-s SEP] [-e END] [-O] [-I] [-S [STRIP]]
	                  [-p [POSITION]] [-i [INPUT_FILE [INPUT_FILE ...]]]
	                  [-o [OUTPUT_FILE]]
	                  [string [string ...]]
	
	positional arguments::
	  string                one or more input strings.
	
	optional arguments::
	  -h, --help            show this help message and exit
	  -c, --codes           show the available color codes and exit.
	  -v, --version         show the current version of this module and exit.
	  -t, --true-color      use of RGB values for the ANSI escape sequences.
	                        Allowes customized foreground color codes and a more
	                        accurate color set (warning: having this option won't
	                        work on all terminals as they do not all support true
	                        color).
	  -s SEP, --sep SEP     specify what string to use, to separate string
	                        arguments (default is ' ').
	  -e END, --end END     specify what string to use at the end of the printed
	                        string (default is '\n')
	  -O, --overflow        make colors overflow to other strings if a color code
	                        is not finished.
	  -I, --ignore-special  tell the parser to ignore special characters like (new
	                        line, tab, etc.).
	  -S [STRIP], --strip [STRIP]
	                        specify which leading and trailing characters to
	                        remove from input file(s) (by default removes
	                        whitespace if the flag is used).
	  -p [POSITION], --position [POSITION]
	                        place all strings after the nth input file.
	  -i [INPUT_FILE [INPUT_FILE ...]], --input-file [INPUT_FILE [INPUT_FILE ...]]
	                        specify one or more files to read the color coded
	                        strings from. If a file doesn't exist, an error will
	                        be raised. It must be used after any string argument.
	  -o [OUTPUT_FILE], --output-file [OUTPUT_FILE]
	                        specify an output file to append the resulting string
	                        (default is sys.stdout).
