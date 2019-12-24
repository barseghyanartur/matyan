#!/usr/bin/env python
import os
import sys
import pytest

# Args with values
for arg in ('--max-depth', '-o', '-T', '-s',):
    try:
        if arg in sys.argv:
            index = sys.argv.index(arg)
            sys.argv.pop(index)  # argument
            sys.argv.pop(index)  # value

    except Exception as err:
        pass

# Args with no values
for arg in ('-O', '-v'):
    try:
        if arg in sys.argv:
            index = sys.argv.index(arg)
            sys.argv.pop(index)  # argument

    except Exception as err:
        pass


def main():
    sys.path.insert(0, os.path.abspath('src'))
    return pytest.main()


if __name__ == '__main__':
    sys.exit(main())
