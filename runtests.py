#!/usr/bin/env python
import os
import sys
import pytest

try:
    if '--max-depth' in sys.argv:
        index = sys.argv.index('--max-depth')
        sys.argv.pop(index)  # --max-depth argument
        sys.argv.pop(index)  # --max-depth value
except Exception as err:
    pass


def main():
    sys.path.insert(0, os.path.abspath('src'))
    return pytest.main()


if __name__ == '__main__':
    sys.exit(main())
