# SPDX-FileCopyrightText: 2022-present tobimd <tobimd@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import unittest as ut

from test.parse_test import *


def main():
    ut.defaultTestLoader.sortTestMethodsUsing = lambda *args: -1
    ut.TestLoader.sortTestMethodsUsing = lambda *args: -1
    ut.main()


if __name__ == "__main__":
    main()
