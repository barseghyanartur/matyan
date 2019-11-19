import logging
import unittest

import subprocess

from .base import log_info
from .mixins import ChangelogMixin

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('TestCommands',)

LOGGER = logging.getLogger(__name__)


class TestCommands(unittest.TestCase, ChangelogMixin):
    """Commands tests."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestCommands, cls).setUpClass()
        cls.prepare_changelog_data()

    @log_info
    def test_01_generate_changelog_command(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(res, self.changelog_output)
        return res

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

    @log_info
    def test_03_generate_changelog_command_show_latest_release(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--latest-release',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.changelog_latest_release_show_releases_output
        )
        return res

    @log_info
    def test_04_json_changelog_command(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog'
        ]).strip().decode()
        self.assertEqual(res, self.json_output)
        return res

    @log_info
    def test_05_json_changelog_command_show_releases(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog',
            '--show-releases'
        ]).strip().decode()
        self.assertEqual(res, self.json_show_releases_output)
        return res

    @log_info
    def test_06_json_changelog_command_show_latest_release(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog',
            '--show-releases',
            '--latest-release'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.json_latest_release_show_releases_output
        )
        return res

    @log_info
    def test_07_make_config_file(self):
        """Test make config command."""
        res = subprocess.check_output([
            'matyan-make-config',
        ]).strip().decode()
        self.assertEqual(res, '')
        return res


if __name__ == '__main__':
    unittest.main()
