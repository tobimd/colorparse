import unittest as ut
import colorparse as cp
from test.util import *


def _print_test(index: int, test: str, result: str, expected: str):
    iprint(f"({index}) input:    '{test}'", limit=False)
    iprint(f"({index}) parsed:   '{result[:-1]}{e}'", limit=False)
    iprint(f"({index}) raw:      {b}{ascii(result)}{e}")
    iprint(f"({index}) expected: {b}{ascii(expected)}{e}\n")


class ModuleParse(TestCase):
    """Test for `print` and `paint` calls"""

    def test_0_parsing_consistency(self):
        tprint()

        for i, test, expected in test_zip(TEST_PARSING[0]):
            result = cp.paint(test)
            _print_test(i, test, result, expected)

            with self.subTest(parse_test=i):
                self.assertEqual(ascii(result), ascii(expected))

    def test_1_consistency_with_custom_commands(self):
        tprint()

        def command_exists(
            cont: Literal["colors", "styles"],
            subcont: Literal["foreground", "background", "start", "end"],
            attr,
        ):
            if cont == "colors":
                getattr(
                    cp.colors.foreground, attr
                ) if subcont == "foreground" else getattr(cp.colors.background, attr)
            else:
                getattr(cp.styles.start, attr) if subcont == "start" else getattr(
                    cp.styles.end, attr
                )

        for i, reg in enumerate(TEST_COMMAND_REGISTRATION):
            with self.subTest(registration=f"{i:03}"):
                iprint(
                    f"({i:03}) registering {reg['cont'][:-1]} command: {b}{reg['name']}{e} ({reg['command']})"
                )
                cp.register_command(reg["name"], reg["command"], reg["code"])
                self.assertNotRaises(
                    AttributeError,
                    command_exists,
                    reg["cont"],
                    reg["subcont"],
                    reg["name"],
                )

        print()
        for i, test, expected in test_zip(TEST_PARSING[0], TEST_PARSING[1], start=10):
            result = cp.paint(test)
            _print_test(i, test, result, expected)

            with self.subTest(parse_test=i):
                self.assertEqual(ascii(result), ascii(expected))
