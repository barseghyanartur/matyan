# -*- coding: utf-8 -*-

import copy
import re
import logging
import os
import unittest
from unittest import mock

from ..utils import (
    create_config_file,
    generate_changelog,
    generate_empty_tree,
    get_branch_type,
    get_logs,
    json_changelog,
    prepare_changelog,
    prepare_releases_changelog,
    validate_between,
)
from ..patterns import (
    REGEX_PATTERN_MERGED_BRANCH_NAME,
)

from .base import (
    internet_available_only,
    log_info,
    internet_available_or_is_travis_only,
)
from .mixins import ChangelogMixin

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = ('TestCore',)

LOGGER = logging.getLogger(__name__)


class TestCore(unittest.TestCase, ChangelogMixin):
    """Core functionality tests."""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        super(TestCore, cls).setUpClass()
        cls.prepare_changelog_data()

    @log_info
    def test_01_generate_changelog(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            path=self.test_dir
        ).strip()
        self.assertEqual(res, self.changelog_output)
        return res

    @log_info
    def test_02_generate_changelog_show_releases(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            show_releases=True,
            path=self.test_dir
        ).strip()
        self.assertEqual(res, self.changelog_releases_output)
        return res

    @log_info
    def test_03_merge_branch_patterns(self):
        """Test generate changelog."""
        merge_messages = {
            'Merge pull request #1234 in PROJ/repo from bugfix/PROJ-'
            '3545-currency-not-saved-at-sso to dev': {
                'ticket_number': 'PROJ-3545',
                'branch_title': 'currency-not-saved-at-sso'
            },
            'Merged in bugfix/MSFT-1236-prevent-duplicate-postal-codes '
            '(pull request #3)': {
                'ticket_number': 'MSFT-1236',
                'branch_title': 'prevent-duplicate-postal-codes'
            },
        }
        for message, parsed in merge_messages.items():
            match = re.match(REGEX_PATTERN_MERGED_BRANCH_NAME, message)
            with self.subTest(f'Testing {message}: {parsed}'):
                self.assertIsNotNone(match)
                ticket_number = match.group('ticket_number')
                self.assertEqual(ticket_number, parsed['ticket_number'])
                branch_title = match.group('branch_title')
                self.assertEqual(branch_title, parsed['branch_title'])


if __name__ == '__main__':
    unittest.main()
