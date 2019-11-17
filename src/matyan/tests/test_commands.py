import logging
import unittest

import subprocess

from .base import log_info, internet_available_only

__title__ = 'matyan.tests.test_commands'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('TestCommands',)

LOGGER = logging.getLogger(__name__)


class TestCommands(unittest.TestCase):
    """Matyan commands tests."""

    def setUp(self):
        """Set up."""

    @internet_available_only
    @log_info
    def test_01_generate_changelog_command(self):
        """Test generate changelog command."""
        res = subprocess.check_output('generate-changelog').strip()
        self.assertEqual(res, b'')
        return res


if __name__ == '__main__':
    unittest.main()
