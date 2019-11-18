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

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('TestCommands',)

LOGGER = logging.getLogger(__name__)


class TestCommands(unittest.TestCase):
    """Matyan commands tests."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestCommands, cls).setUpClass()
        # if is_internet_available() or is_travis():
        # Test directory for cloning the repo
        test_dir = project_dir("tests/matyan-testing")
        if not os.path.exists(test_dir):
            git.Repo.clone_from(
                "https://barseghyanartur@bitbucket.org/barseghyanartur/matyan-testing.git",  # NOQA
                test_dir,
                StrictHostKeyChecking=False
            )

        # Go to cloned repository
        os.chdir(test_dir)

        # Expected output of the `generate-changelog` command.
        changelog_output = project_dir(
            'tests/output/generate-changelog.md'
        )
        with open(changelog_output, 'r') as file:
            cls.changelog_output = file.read().strip()

        # Expected output of the `generate-changelog --show-releases`
        # command.
        changelog_releases_output = project_dir(
            'tests/output/generate-changelog-releases.md'
        )
        with open(changelog_releases_output, 'r') as file:
            cls.changelog_releases_output = file.read().strip()

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
