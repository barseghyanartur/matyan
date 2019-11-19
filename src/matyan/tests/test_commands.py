import os
import logging
import unittest

import subprocess
import git

from ..helpers import project_dir
from .base import (
    log_info,
    internet_available_only,
    is_internet_available,
    internet_available_or_is_travis_only,
    is_travis,
)
from .mixins import ChangelogMixin

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('TestCommands',)

LOGGER = logging.getLogger(__name__)


class TestCommands(unittest.TestCase, ChangelogMixin):
    """Matyan commands tests."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestCommands, cls).setUpClass()
        cls.prepare_changelog_data()

    # @internet_available_or_is_travis_only
    @log_info
    def test_01_generate_changelog_command(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(res, self.changelog_output)
        return res

    # @internet_available_or_is_travis_only
    @log_info
    def test_02_generate_changelog_command_show_releases(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(res, self.changelog_releases_output)
        return res


if __name__ == '__main__':
    unittest.main()
