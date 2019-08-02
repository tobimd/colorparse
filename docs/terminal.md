To better understand how to use the colorparse command, we will simplify things by separating it in four parts. For the full version of the help menu, you can use the flags `-h` or `--help` in the terminal, or go to the [help message](#help-message) below.

```
usage: colorparse [options] [string ...] [-i ...] [-o]

```

## options

There are the following options available:

| **FLAG**                 | **DESCRIPTION**                                            | **DEFAULT VALUE** |
|:-------------------------|:-----------------------------------------------------------|------------------:|
| `-t`, `--true-color`     | Use of RGB values for the color escape sequences.          | ``False``         |
| `-s`, `--sep`            | Specify what to use, to separate string arguments          | ``' '``           |
| `-e`, `--end`            | Specify what to use at the end of the printed string.      | ``'\n'``          |
| `-O`, `--overflow`       | Make color codes overflow to other strings.                | ``False``         |
| `-I`, `--ignore-special` | Ignore special characters (new line, tab, etc.).           | ``False``         |
| `-S`, `--strip   `       | Remove leading and trailing characters from input file(s). | ``None``          |
| `-p`, `--position`       | Place all strings after the *n*th input file.                | ``0``             |
| `-h`, `--help`           | Show a help menu and exit.                                 |                   |
| `-c`, `--codes`          | Show the list of color codes and exit.                     |                   |
| `-v`, `--version`        | Show the current version of the module and exit.           |                   |


Here are a few options that are not present when importing colorparse as a module:

#### `-I`, `--ignore-special`
This option will ignore special characters and return the strings as if those characters were escaped.

#### `-S`, `--strip`
Just like the built-in string method, having the strip flag will remove specified leading and trailing characters from all input files. If no character is given, then the default value ``None`` means that whitespaces will be removed. To specify which characters to strip, the string should only have them without spaces or separators. For example, having "abc" will remove all combinations of those 3 characters. Note that, if possible, this argument will try to use the proceeding value, so to use this flag without arguments, it must be either before another flag, after a flag's argument (with the exception of ``--input-file`` as we will discuss it later) or at the end.

#### `-p`, `--position`
By default, any strings given will be added before input files. With this option, you can choose in which position those strings should be in relation to the input files. Works like the built-in `insert` method for lists, including the option to have negative indexes.

\* *special characters are: ``\n`` (new line), ``\r`` (carriage return), ``\t`` (horizontal tab), ``\v`` (vertical tab), ``\a`` (bell), ``\b`` (backspace) and ``\f`` (formfeed)* *

## string

The input strings (0 or more).

## input files

There is the option to read formatted strings (which means that it has color codes) from files. Using either `-i` or `--input-file` flags, the proceeding arguments will be considered as the files to open.

Even though this flag can be at the start of the options, or in other words, using the `-i` or `--input-file` flag before adding strings, doing so will make the program think that those strings are files to look for, which is not true and will raise an error (if a file doesn't exist). For this reason, it's recommended to add this flag at the end or after adding any `string` arguments.

## output file

Contrary to the input files, this optional argument can be set anywhere. It only accepts one file as an output and it won't raise any errors if the file doesn't exist. If it does exist whatsoever, any obtained string will be added to the end of it.

## help message

If nothing is given as an argument, then the "usage help" is printed and the program ends. The following is what the terminal shows when using the help flags:

```console
usage: colorparse [-h] [-c] [-v] [-t] [-s SEP] [-e END] [-O] [-I] [-S [STRIP]]
                  [-p [POSITION]] [-i [INPUT_FILE [INPUT_FILE ...]]]
                  [-o [OUTPUT_FILE]]
                  [string [string ...]]

positional arguments:
  string                one or more input strings.

optional arguments:
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
```
