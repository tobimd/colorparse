import sys
from typing import Callable, Iterator, Literal, Type, Union, overload
import unittest as ut
import pathlib as pl


class TestCase(ut.TestCase):
    def run(self, result=None):
        if result is None:
            self.result = self.defaultTestResult()
        else:
            self.result = result

        return ut.TestCase.run(self, result)

    def assertFileExists(self, path: str):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"File does not exist: {str(path)}")

    @overload
    def assertNotRaises(
        self,
        expected_exception: Union[Type[BaseException], tuple[Type[BaseException], ...]],
        callable: Callable[..., object],
        *args,
        **kwargs,
    ) -> None:
        ...

    def assertNotRaises(self, expected_exception, *args, **kwargs):
        msg = kwargs.pop("msg", None)
        callable_obj, *args = args

        try:
            callable_obj(*args, **kwargs)

        except expected_exception as e:
            if msg:
                raise AssertionError(msg)
            else:
                raise expected_exception(", ".join(e.args))

    def expect(self, val, msg=None, stop: bool = False):
        """
        Like TestCase.assert_, but doesn't halt the test.
        """
        if stop:
            self.assert_(val, msg)
            return

        try:
            self.assert_(val, msg)
        except:
            self.result.addFailure(self, sys.exc_info())

    def expectEqual(self, first, second, msg=None, stop: bool = False):
        if stop:
            self.assertEqual(first, second, msg)
            return

        try:
            self.assertEqual(first, second, msg)
        except:
            self.result.addFailure(self, sys.exc_info())

    def expectFileExists(self, path: str, stop: bool = False):
        if stop:
            self.assertFileExists(path)
            return

        try:
            self.assertFileExists(path)

        except:
            self.result.addFailure(self, sys.exc_info())

    @overload
    def expectNotRaises(
        self,
        expected_exception: Union[Type[BaseException], tuple[Type[BaseException], ...]],
        callable: Callable[..., object],
        stop: bool = False,
        *args,
        **kwargs,
    ) -> None:
        ...

    def expectNotRaises(self, expected_exception, *args, **kwargs):
        stop = kwargs.pop("stop", False)

        if stop:
            self.assertNotRaises(expected_exception, *args, **kwargs)
            return

        try:
            self.assertNotRaises(expected_exception, *args, **kwargs)
        except:
            self.result.addFailure(self, sys.exc_info())


# misc
e = "\x1b[0m"
b = "\x1b[1m"
w = "\x1b[1;37m"
c = "\x1b[38;5;45m"
y = "\x1b[38;5;226m"
g = "\x1b[38;5;82m"
r = "\x1b[38;5;196m"


def _print(t: str, *values, start: str, end: str, limit: bool):
    if limit:
        from os import get_terminal_size as get_size

        cols = get_size().columns
        max_len = (cols - 30 if cols < 200 else 200) if cols > 35 else 35

        values = [
            f"{v[:max_len-3]}\033[0m..." if len(v) >= max_len else v
            for v in ("\n".join(values)).split("\n")
        ]
    else:
        values = [v for v in ("\n".join(values)).split("\n")]
    print(start + t, end="")
    print(*values, sep=f"\n{t}", end=end)


def dprint(*values, start="", end="\n", limit: bool = False):
    _print(f"[ {g}debug{e} ]", *values, start=start, end=end, limit=limit)


def iprint(*values, start="", end="\n", limit: bool = True):
    _print(f"[ {y}info{e}  ] ", *values, start=start, end=end, limit=limit)


def tprint():
    import inspect
    import re

    name = re.sub(r"^test_(\d+_)?", "", inspect.stack()[1].function)
    res = f"\n\n[ {c}test {e} ] {b}Running test: '{r}{name}{e}{b}'{e}"
    print(res + f"\n{b}{'=' * (26 + len(name))}{e}\n")


def test_zip(
    *test_dict: dict[Union[Literal["input"], Literal["output"]], list[str]],
    padding_count: int = 3,
    start: int = 0,
    end: int = -1,
) -> Iterator[tuple[int, str, str]]:
    i = -1
    j = -1
    for td in test_dict:
        for ipt, opt in zip(td["input"], td["output"]):
            j += 1

            if j >= start and (end == -1 or j < end):
                i += 1
                yield (f"{i:0{padding_count}}", ipt, opt)


file_default_print = "test/generated/test_print.log"

# strings
TEST_PARSING: list[dict[Union[Literal["input"], Literal["output"]], list[str]]] = [
    {
        "input": [
            "[;g]green color + \;.[;.] normal string",
            "[;g]green color + \;:[;:] normal string",
            "[;g]green color + \:;[:;] normal string",
            "[;g]green color + \;;[;;] normal string",
            "[;g]green color + \::[::] green color",
            "[;g]green color + [:C]cyan background + \;.[;.] normal string",
            "[;g]green color + [:C]cyan background + \;:[;:] normal string",
            "[;g]green color + [:C]cyan background + \:;[:;] normal string",
            "[;g]green color + [:C]cyan background + \;;[;;] cyan background",
            "[;g]green color + [:C]cyan background + \::[::] green color",
            "[;g]green color + [;+b]bold text + [:C]cyan background + \;-b[;-b] green fg & cyan bg",
            "[;g]green color + [;+b]bold text + [;+d]dim text + [:C]cyan background + \;-b[;-b] dim green fg & cyan bg",
            "[;+b]bold text + [;+d]dim text + \;-d[;-d] bold text \;-b[;-b] normal text",
            "[;+b][;+i]italic bold text + \;-d[;-d] italic bold text",
            "[;+b][;+i]italic bold text + \;-b[;-b] italic text",
        ],
        "output": [
            "\033[38;5;34mgreen color + ;.\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + ;:\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + :;\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + ;;\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + ::\033[0m\033[38;5;34m green color\033[0m",
            "\033[38;5;34mgreen color + \033[48;5;45mcyan background + ;.\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + \033[48;5;45mcyan background + ;:\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + \033[48;5;45mcyan background + :;\033[0m normal string\033[0m",
            "\033[38;5;34mgreen color + \033[48;5;45mcyan background + ;;\033[0m\033[48;5;45m cyan background\033[0m",
            "\033[38;5;34mgreen color + \033[48;5;45mcyan background + ::\033[0m\033[38;5;34m green color\033[0m",
            "\033[38;5;34mgreen color + \033[1mbold text + \033[48;5;45mcyan background + ;-b\033[22m green fg & cyan bg\033[0m",
            "\033[38;5;34mgreen color + \033[1mbold text + \033[2mdim text + \033[48;5;45mcyan background + ;-b\033[22m\033[2m dim green fg & cyan bg\033[0m",
            "\033[1mbold text + \033[2mdim text + ;-d\033[22m\033[1m bold text ;-b\033[22m normal text\033[0m",
            "\033[1m\033[3mitalic bold text + ;-d\033[22m\033[1m italic bold text\033[0m",
            "\033[1m\033[3mitalic bold text + ;-b\033[22m italic text\033[0m",
        ],
    },
    {
        "input": [
            "\;tfg[;tfg] custom foreground color + \:tbg[:tbg] custom background color + \;+E[;+E] with custom style 1 + \;+F[;+F] with custom style 2 - \;-E[;-E] remove style 1",
            "\;r;r/red;; \;o;o/orange;; \;y;y/yellow;; \;g;g/green;; \;c;c/cyan;; \;b;b/blue;; \;p;p/purple;; \;m;m/magenta;; \;tfg;tfg/test foreground",
            "\:r:r/red:: \:o:o/orange:: \:y:y/yellow:: \:g:g/green:: \:c:c/cyan:: \:b:b/blue:: \:p:p/purple:: \:m:m/magenta:: \:tbg:tbg/test background",
        ],
        "output": [
            ";tfg\x1b[38;5;184m custom foreground color + :tbg\x1b[48;5;124m custom background color + ;+E\x1b[52m with custom style 1 + ;+F\x1b[51m with custom style 2 - ;-E\x1b[54m\x1b[51m remove style 1\x1b[0m",
            ";r\x1b[38;5;124mred\x1b[0m ;o\x1b[38;5;166morange\x1b[0m ;y\x1b[38;5;184myellow\x1b[0m ;g\x1b[38;5;34mgreen\x1b[0m ;c\x1b[38;5;39mcyan\x1b[0m ;b\x1b[38;5;27mblue\x1b[0m ;p\x1b[38;5;57mpurple\x1b[0m ;m\x1b[38;5;127mmagenta\x1b[0m ;tfg\x1b[38;5;184mtest foreground\x1b[0m",
            ":r\x1b[48;5;124mred\x1b[0m :o\x1b[48;5;166morange\x1b[0m :y\x1b[48;5;184myellow\x1b[0m :g\x1b[48;5;34mgreen\x1b[0m :c\x1b[48;5;45mcyan\x1b[0m :b\x1b[48;5;27mblue\x1b[0m :p\x1b[48;5;93mpurple\x1b[0m :m\x1b[48;5;165mmagenta\x1b[0m :tbg\x1b[48;5;124mtest background\x1b[0m",
        ],
    },
]

TEST_COMMAND_REGISTRATION: list[
    dict[Literal["cont", "subcont", "name", "command", "code"], str]
] = [
    {
        "cont": "colors",
        "subcont": "foreground",
        "name": "TEST_FG",
        "command": ";tfg",
        "code": "\033[38;5;184m",
    },
    {
        "cont": "colors",
        "subcont": "background",
        "name": "TEST_BG",
        "command": ":tbg",
        "code": "\033[48;5;124m",
    },
    {
        "cont": "styles",
        "subcont": "start",
        "name": "TEST_ST_FRAMED",
        "command": ";+F",
        "code": "\033[51m",
    },
    {
        "cont": "styles",
        "subcont": "end",
        "name": "TEST_ST_FRAMED",
        "command": ";-F",
        "code": "\033[54m",
    },
    {
        "cont": "styles",
        "subcont": "start",
        "name": "TEST_ST_ENCIRCLED",
        "command": ";+E",
        "code": "\033[52m",
    },
    {
        "cont": "styles",
        "subcont": "end",
        "name": "TEST_ST_ENCIRCLED",
        "command": ";-E",
        "code": "\033[54m",
    },
    {
        "cont": "styles",
        "subcont": "start",
        "name": "TEST_ST_OVERLINED",
        "command": ";+O",
        "code": "\033[53m",
    },
    {
        "cont": "styles",
        "subcont": "end",
        "name": "TEST_ST_OVERLINED",
        "command": ";-O",
        "code": "\033[55m",
    },
]
