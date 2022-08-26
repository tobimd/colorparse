&nbsp;

&nbsp;

<div align="center"><a href="#"><img src="/images/colorparse-logo.png" alt="[;colorparse]" width=500 /></a>
</div>

<p align="center">
  Give <b><a href="#">color</a></b> and <b><i>style</i></b> to text effortlessly using commands!
</p>

<div align="center">

[![python version compatibility >= 3.7](https://img.shields.io/badge/python-%3E%3D%203.7-blue?style=flat-square&logo=python&logoColor=white&logoWidth=12)](https://pypi.org/project/colorparse/)&ensp;
[![package version 2.0.0](https://img.shields.io/pypi/v/colorparse?color=green&label=package&style=flat-square)](https://pypi.org/project/colorparse/)&ensp;
[![python wheel available](https://img.shields.io/pypi/wheel/colorparse?color=%23fca32f&style=flat-square)](https://pypi.org/project/colorparse/)&ensp;
[![documentation available](https://img.shields.io/badge/docs-yes-%23fc8a8a?style=flat-square)](/)&ensp;
[![changelog available](https://img.shields.io/badge/changelog-latest-%23ed63e3?style=flat-square)](/CHANGELOG.md)

</div>

&nbsp;

&nbsp;
  
## Table of contents

- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
  - [Concepts](#concepts)
  - [Examples](#examples)
  - [Module](#module)
    - [Methods](#methods)
- [Default commands](#default-commands)
- [See more](#see-more)
  - [License](#license)
  - [Full documentation](#full-documentation)
  - [More examples](#more-examples)
  - [Changelog](#changelog)
<h2></h2>
&nbsp;

&nbsp;
  
## Installation

```terminal
py -m pip install colorparse
```

<div style="height: 25px"></div>

## Usage

&nbsp;

**NOTE**: Because I believe this package might include a lot more bloat than neccessary for some cases, [colorparse-mini is also available]().

&nbsp;

The main difference between most text-coloring packages for python and *colorparse*, is that the former ones use imported variables that contain the colors. For example, you would use something like:

```python
>>> print(Colors.red + "roman empire") # With colorparse: 'colors.foreground.RED'
```

However, even though you are allowed to use this structure with this package (a little bit more verbose anyways), the expected way is using the following:

```python
>>> print("[;r]roman empire") # The "color command" is ;r for red
```

The idea is to avoid cluttering print statements or plain strings with concatenations, and instead use commands (customizable) which will later get parsed into colors or styles.

### Concepts

<details open>
  <summary><a name="commands"></a><b>Commands</b></summary>

A command is an object that represents a specific color or style and holds 3 components:
- A variable name (to store it and manually access through code).
- The proper command string (used to replace with the final color or style, like `;r` for red or `;+b`.
- The [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) which is stored as a Code object inside the command.
  
&nbsp;
</details>
<details open>
  <summary><a name="types"></a><b>Types</b></summary>
  
For both colors and styles, there are two types. Colors have the types `foreground` (`;`) and `background` (`:`). Styles have `start` (`;+`) and `end` (`;-`).

This is useful when working around commands as variables (e.g. `colors.foreground.RED` or `styles.end.BOLD`), but also to disinguish between starting and ending styles.
  
&nbsp;
</details>
<details open>
  <summary><a name="stopping-commands"></a><b>Stopping commands</b></summary>
  
There are specific commands that stop foreground or background colors currently active: `;;` (any foreground color) and `::` (any background color). Use either `;:` or `:;` (interchangable) to stop any color regardless of type.

On the other hand, styles can be stopped using each style's counterpart (the `end` type). For example, if bold is used with `;+b` (with type `start`, because of the plus sign), the counterpart is `;-b` (of type `end`).

Use `:.` to stop all commands.
  
&nbsp;
</details>
<details open>
  <summary><a name="encapsulation"></a><b>Encapsulation</b></summary>
  
Any command can be encapsulated by surrounding it with special characters. This is useful to avoid situations where a command is next to text that is not meant to be part of the command like: "`;r`roman empire" (words "roman empire" in red) which would be interpreted as "`;rr`oman empire" ("oman empire" in **dark red** instead).

Commands can be surrounded by one or two forward slashes `/` on each side of the command, both regular parenthesis `(` and `)` or both square brackets `[` and `]`. Examples of these are: "`;r/`roman empire", "`(;r)`roman empire" and "`[;r]`roman empire". All result in the detection of red command, instead of the dark red variation.

***Note***: forward slashes can only be placed next to the command, unlike the parenthesis and square brackets which allow spaces in between.
  
&nbsp;
</details>
<details open>
  <summary><a name="escaping"></a><b>Escaping</b></summary>
  
If needed, commands can be escaped by using backslash `\` right before the start, not including encapsulation (e.g. "`\;rr`oman empire" returns ";rroman empire" and "`[\;r]`roman empire" returns "[;r]roman empire").

&nbsp;
</details>

&nbsp;

### Examples

```python
>>> import colorparse as cp # Use 'cp.print' to print and 'cp.paint' to return only
```

```python
>>> # ;g (green foreground)
>>> cp.print(";g/green goblin")
```

<div align="center" title='"green goblin" printed in green'>
  <img alt='"green goblin" printed in green' src="/images/colorparse-example-result-1-dark.png" width="288px" />
  <img src="/images/colorparse-example-result-1-light.png" width="288px" />
</div>

&nbsp;

```python
>>> # ;y  (yellow foreground)
>>> # ;:  (stop colors)
>>> cp.print("[ [;y]info[;:] ] program result")
```

<div align="center" title='"[ info ] program result" printed with "info" in yellow'>
  <img alt='"[ info ] program result" printed with "info" in yellow' src="/images/colorparse-example-result-2-dark.png" width="288px" />
  <img src="/images/colorparse-example-result-2-light.png" width="288px" />
</div>

&nbsp;

```python
>>> # ;R  (strong red foreground)
>>> # ;+b (start bold)
>>> # ;-b (stop bold)
>>> # :y  (yellow background)
>>> cp.print("[ /;R;+b/warning/;-b :y/!/;: ] program warning!")
```

<div align="center" title='"[ warning ! ] program warning!" printed with the first "warning" in bold, "warning !" in red and the first "!" with yellow background'>
  <img alt='"[ warning ! ] program warning!" printed with the first "warning" in bold, "warning !" in red and the first "!" with yellow background' src="/images/colorparse-example-result-3-dark.png" width="288px" />
  <img src="/images/colorparse-example-result-3-light.png" width="288px"/>
</div>
  
&nbsp;

```python
>>> # All the following strings should get parsed into the same result
>>> to_parse = [
>>>     ";r/roman empire",
>>>     "/;r/roman empire",
>>>     "[ ;r ]roman empire"
>>> ]
>>> 
>>> cp.paint(to_parse[0]) == cp.paint(to_parse[1]) == cp.paint(to_parse[2])
True
```
  
&nbsp;

### Module

When importing this module, there are the following accessible methods and variables:

#### Methods

<details>
<summary><code>print(*value, overflow:bool|None, sep:str|None, end:str|None, file:SupportsWrite[str]|None, flush:bool|None)</code></summary>

- **Description**: Prints a string with commands converted to ANSI escape sequences.

- **Examples**:

  ```python
  >>> cp.print("[", ";C/DEBUG", "]", "information...")
  ```

  ```python
  >>> test_variable = "message"
  >>> cp.print(";m;+b/warning: ", test_variable, overflow=True, sep="")
  ```

</details>
<details>
<summary><code>paint(*value, overflow:bool|None, sep:str|None, end:str|None)</code></summary>

- **Description**: Returns a string commands converted to ANSI escape sequences.

  **NOTE**: This is basically the same as `print`, but instead of directly sending output (to stdout or whatever `file` is set to) it returns the parsed string.

- **Examples**:

  ```python
  >>> cp.print("[", ";C/DEBUG", "]", "information...")
  '[\x1b[0m \x1b[38;5;45mDEBUG\x1b[0m ]\x1b[0m information...\x1b[0m'
  ```

  ```python
  >>> test_variable = "message"
  >>> cp.print(";m;+b/warning: ", test_variable, overflow=True, sep="")
  '\x1b[38;5;127m\x1b[1mwarning: message\x1b[0m'
  ```

</details>
<details>
<summary><code>register_command(name:str, command:str, value:str) -> None</code></summary>

- **Description**: Register a `Command` object. `name` is used to store the command as a variable and `command` is used when parsing (both `name` and `command` must follow Python's variable naming rules).

  **NOTE**: When adding a style command, `command` expects exactly 3 characters: ";<`+ or -`><`character`>" like ";+b" for starting bold (technically `:` can be used instead of `;`, but it doesn't affect anything).

- **Examples**:

  ```python
  >>> # A nice purple color
  >>> cp.register_command("MY_COMMAND", ";cmd", "\033[38:5:98m")
  >>> 
  >>> # Accessible from "colors.foreground.MY_COMMAND" or by its command:
  >>> cp.print(";cmd/testing new color")
  ```

  ```python
  >>> # "Framed" style. 
  >>> cp.register_command("SPECIAL_STYLE", ";+F", "\033[51m")
  >>> 
  >>> # Accessible from "styles.start.SPECIAL_STYLE" or by its command:
  >>> cp.print(";+F/probably won't show on most terminals!")
  ```

</details>
<details>
<summary><code>configuration(tag:str|_Options._OptionAttr, **values) -> None</code></summary>

- **Description**: Set global default values (or options in the case of flags) to a given value/state.

- **Examples**:

  ```python
  >>> # Set argument `overflow` to default to True for `paint`.
  >>> cp.configuration(cp.options.print, overflow=True) # "print" can also be used instead
  ```

  ```python
  >>> # Set "ignore_special" flag to be True (ignores special characters like tabs or newlines)
  >>> cp.configuration("flags", ignore_special=True)
    ```

</details>
<details>
<summary><code>show_commands()</code></summary>

- **Description**: Print a generated list of commands with their information

</details>

&nbsp;

#### Variables

<details>
<summary><code>colors</code></summary>

- **Description**: A container for both `foreground` and `background` types, and each one containing themselves the respective registered colors.
  
- **Examples**::

  ```python
  >>> cp.colors.foreground.RED
  ```

  ```python
  >>> cp.colors.background.DARK_GREEN
  ```

</details>
<details>
<summary><code>styles</code></summary>

- **Description**: A container for both `start` and `end` types, and each one containing themselves the respective registered styles.
  
- **Examples**:

  ```python
  >>> cp.styles.start.BOLD
  ```

  ```python
  >>> cp.styles.end.UNDERLINE
  ```

</details>
<details>
<summary><code>options</code></summary>

- **Description**: Stores program-wide configuration for default values and data (gets updated when calling `configuration`, and technically can be used instead of the method).
  
- **Examples**:

  ```python
  >>> if cp.options.flags.ignore_special:
  >>>     ...
  ```

  ```python
  >>> cp.options.print.overflow = True
      ```

</details>
<details>
<summary><code>RESET</code></summary>

- **Description**: Contains "`\033[0m`" which is equal to "`;.`" command (stops all commands).

</details>

&nbsp;

### Script

You can use the following to get more in-depth help for how to use colorparse in the terminal:

```terminal
colorparse --help
```

## Default commands

<div align="center">
<table>
<thead>
  <tr>
    <th colspan="2" valign="top"><b>Colors</b></br>foreground: <code>;&lt;value&gt;</code></br>background: <code>:&lt;value&gt;</code></th>
    <th colspan="2" valign="top"><b>Styles</b></br>start: <code>;+&lt;value&gt;</code></br>end: <code>;-&lt;value&gt;</code></th>
    <th colspan="2" valign="top"><b>Stopping</b></th>
  </tr>
</thead>
<tbody>
    <tr>
      <td valign="middle" align="center"><b>Value</b></td>
      <td valign="middle" align="center"><b>Attribute</b></td>
      <td valign="middle" align="center"><b>Value</b></td>
      <td valign="middle" align="center"><b>Attribute</b></td>
      <td valign="middle" align="center"><b>Command</b></td>
      <td valign="middle" align="center"><b>Targets</b></td>
    </tr>
    <tr>
      <td align="center"><code>rr</code></td><td align="left"><code>DARK_RED</code></td>
      <td align="center"><code>b</code></td><td align="left"><code>BOLD</code></td>
      <td align="center"><code>;.</code></td><td align="left">All</td>
    </tr>
    <tr>
      <td align="center"><code>oo</code></td><td align="left"><code>DARK_ORANGE</code></td>
      <td align="center"><code>i</code></td><td align="left"><code>ITALIC</code></td>
      <td align="center"><code>;:</code></td><td align="left">Colors</td>
    </tr>
    <tr>
      <td align="center"><code>yy</code></td><td align="left"><code>DARK_YELLOW</code></td>
      <td align="center"><code>u</code></td><td align="left"><code>UNDERLINE</code></td>
      <td align="center"><code>:;</code></td><td align="left">Colors</td>
    </tr>
    <tr>
      <td align="center"><code>gg</code></td><td align="left"><code>DARK_GREEN</code></td>
      <td align="center"><code>s</code></td><td align="left"><code>STRIKE</code></td>
      <td align="center"><code>;;</code></td><td align="left">Foreground</td>
    </tr>
    <tr>
      <td align="center"><code>cc<br></code></td><td align="left"><code>DARK_CYAN</code></td>
      <td align="center"><code>d</code></td><td align="left"><code>DIM</code></td>
      <td align="center"><code>::</code></td><td align="left">Background</td>
    </tr>
    <tr>
      <td align="center"><code>bb</code></td><td align="left"><code>DARK_BLUE</code></td>
      <td align="center"><code>r</code></td><td align="left"><code>REVERSE</code></td>
    </tr>
    <tr>
      <td align="center"><code>pp</code></td><td align="left"><code>DARK_PURPLE</code></td>
      <td align="center"><code>h</code></td><td align="left"><code>HIDE</code></td>
    </tr>
    <tr>
      <td align="center"><code>mm</code></td><td align="left"><code>DARK_MAGENTA</code></td>
    </tr>
    <tr>
      <td align="center"><code>r</code></td><td align="left"><code>RED<br></code></td>
    </tr>
    <tr>
      <td align="center"><code>o</code></td><td align="left"><code>ORANGE</code></td>
    </tr>
    <tr>
      <td align="center"><code>y</code></td><td align="left"><code>YELLOW</code></td>
    </tr>
    <tr>
      <td align="center"><code>g</code></td><td align="left"><code>GREEN</code></td>
    </tr>
    <tr>
      <td align="center"><code>c</code></td><td align="left"><code>CYAN</code></td>
    </tr>
    <tr>
      <td align="center"><code>b</code></td><td align="left"><code>BLUE</code></td>
    </tr>
    <tr>
      <td align="center"><code>p</code></td><td align="left"><code>PURPLE</code></td>
    </tr>
    <tr>
      <td align="center"><code>m</code></td><td align="left"><code>MAGENTA</code></td>
    </tr>
    <tr>
      <td align="center"><code>R</code></td><td align="left"><code>STRONG_RED</code></td>
    </tr>
    <tr>
      <td align="center"><code>O</code></td><td align="left"><code>STRONG_ORANGE</code></td>
    </tr>
    <tr>
      <td align="center"><code>Y</code></td><td align="left"><code>STRONG_YELLOW</code></td>
    </tr>
    <tr>
      <td align="center"><code>G</code></td><td align="left"><code>STRONG_GREEN</code></td>
    </tr>
    <tr>
      <td align="center"><code>C</code></td><td align="left"><code>STRONG_CYAN</code></td>
    </tr>
    <tr><td align="center"><code>B</code></td><td align="left"><code>STRONG_BLUE</code></td>
    </tr>
    <tr>
      <td align="center"><code>P</code></td><td align="left"><code>STRONG_PURPLE</code></td>
    </tr>
    <tr>
      <td align="center"><code>M</code></td><td align="left"><code>STRONG_MAGENTA</code></td>
    </tr>
</tbody>
</table>
</div>

## See more

### License

[MIT License](/module/LICENSE)

### Full documentation

### More examples

[See examples here](/examples/README.md)

### Changelog

[See changelog here](/CHANGELOG.md)
