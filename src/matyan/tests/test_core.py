# -*- coding: utf-8 -*-

import copy
import logging
import os
import unittest

import six
from six.moves.urllib.parse import urlsplit
from ..utils import (
    create_default_config_file,
    generate_changelog_cli,
    generate_empty_tree,
    get_branch_type,
    get_logs,
    json_changelog_cli,
    prepare_changelog,
    prepare_releases_changelog,
    validate_between,
)

from .base import internet_available_only, log_info

__title__ = 'matyan.tests.test_core'
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

    @property
    def good_url(self):
        return self.good_patterns[0]['url']

    @property
    def bad_url(self):
        return list(self.bad_patterns.keys())[0]

    @internet_available_only
    @log_info
    def test_01_generate_changelog_command(self):
        """Test generate changelog."""
        # TODO


if __name__ == '__main__':
    unittest.main()
