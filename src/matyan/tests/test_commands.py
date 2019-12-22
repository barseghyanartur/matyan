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
    def test_generate_changelog(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(res, self.no_args_out)
        return res

    @log_info
    def test_generate_changelog_show_releases(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(res, self.show_releases_out)
        return res

    @log_info
    def test_generate_changelog_show_releases_rst(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--no-other',
            '--renderer=rest'
        ]).strip().decode()
        self.assertEqual(res, self.show_releases_rst_out)
        return res

    @log_info
    def test_generate_changelog_show_releases_renderer_historical(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--no-other',
            '--renderer=historical-markdown'
        ]).strip().decode()
        self.assertEqual(res, self.show_releases_rend_hist_out)
        return res

    @log_info
    def test_generate_changelog_show_releases_latest_release(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--latest-release',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.latest_release_show_releases_out
        )
        return res

    @log_info
    def test_generate_changelog_show_releases_headings_only(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--show-releases',
            '--headings-only',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.show_releases_headings_only_out
        )
        return res

    @log_info
    def test_generate_changelog_headings_only(self):
        """Test generate changelog command."""
        res = subprocess.check_output([
            'generate-changelog',
            '--headings-only',
            '--no-other'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.headings_only_out
        )
        return res

    @log_info
    def test_json_changelog_command(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog'
        ]).strip().decode()
        self.assertEqual(res, self.json_no_args_out)
        return res

    @log_info
    def test_json_changelog_command_show_releases(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog',
            '--show-releases'
        ]).strip().decode()
        self.assertEqual(res, self.json_show_releases_out)
        return res

    @log_info
    def test_json_changelog_show_releases_latest_release(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog',
            '--show-releases',
            '--latest-release'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.json_latest_release_show_releases_out
        )
        return res

    @log_info
    def test_json_changelog_show_releases_headings_only(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog',
            '--show-releases',
            '--headings-only'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.json_show_releases_headings_only_out
        )
        return res

    @log_info
    def test_json_changelog_headings_only(self):
        """Test json changelog command."""
        res = subprocess.check_output([
            'json-changelog',
            '--headings-only'
        ]).strip().decode()
        self.assertEqual(
            res,
            self.json_headings_only_out
        )
        return res

    @log_info
    def test_make_config_file(self):
        """Test make config command."""
        res = subprocess.check_output([
            'matyan-make-config',
        ]).strip().decode()
        self.assertEqual(res, '')
        return res


if __name__ == '__main__':
    unittest.main()
