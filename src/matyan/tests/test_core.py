# -*- coding: utf-8 -*-

import copy
import re
import logging
import os
import unittest

from ..utils import (
    create_config_file,
    generate_changelog_cli,
    generate_empty_tree,
    get_branch_type,
    get_logs,
    json_changelog_cli,
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

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = ('TestCore',)

LOGGER = logging.getLogger(__name__)


class TestCore(unittest.TestCase):
    """Core matyan functionality tests."""

    def setUp(self):
        """Set up."""
        # TODO

    def tearDown(self):
        """Tear down."""
        # TODO

    @log_info
    def test_01_merge_branch_patterns(self):
        """Test generate changelog."""
        merge_messages = [
            'Merge pull request #1234 in PROJ/repo from bugfix/PROJ-'
            '3545-currency-not-saved-at-sso to dev',
            'Merged in bugfix/MSFT-1236-prevent-duplicate-postal-codes '
            '(pull request #3)',
        ]
        for message in merge_messages:
            match = re.match(REGEX_PATTERN_MERGED_BRANCH_NAME, message)
            self.assertIsNotNone(match)


if __name__ == '__main__':
    unittest.main()
