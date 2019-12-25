import json
import re
import logging
import unittest

from ..utils import (
    make_config_file,
    generate_changelog,
    get_branch_type,
    get_logs,
    json_changelog,
    prepare_changelog,
    prepare_releases_changelog,
    validate_between,
    get_repository,
)
from ..renderers import (
    HistoricalMarkdownRenderer,
    RestructuredTextRenderer,
)
from ..patterns import (
    REGEX_PATTERN_MERGED_BRANCH_NAME,
)

from .base import log_info
from .mixins import ChangelogMixin

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('TestCore',)

LOGGER = logging.getLogger(__name__)


class TestCore(unittest.TestCase, ChangelogMixin):
    """Core functionality tests."""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        super(TestCore, cls).setUpClass()
        cls.prepare_changelog_data()

    def tearDown(self):
        super(TestCore, self).tearDown()
        self.clean_up()
        self.repo.checkout('master')
        self.repo.pull()

    @log_info
    def test_generate_changelog(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            path=self.test_dir
        ).strip()
        self.assertEqual(res, self.no_args_out)
        return res

    @log_info
    def test_generate_changelog_show_releases(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            show_releases=True,
            path=self.test_dir
        ).strip()
        self.assertEqual(res, self.show_releases_out)
        return res

    @log_info
    def test_generate_changelog_rst_show_releases(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            show_releases=True,
            renderer_cls=RestructuredTextRenderer,
            path=self.test_dir
        ).strip()
        self.assertEqual(res, self.show_releases_rst_out)
        return res

    @log_info
    def test_generate_changelog_show_releases_renderer_historical(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            show_releases=True,
            renderer_cls=HistoricalMarkdownRenderer,
            path=self.test_dir
        ).strip()
        self.assertEqual(res, self.show_releases_rend_hist_out)
        return res

    @log_info
    def test_generate_changelog_latest_release_show_releases(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            show_releases=True,
            latest_release=True,
            path=self.test_dir
        ).strip()
        self.assertEqual(
            res,
            self.latest_release_show_releases_out
        )
        return res

    @log_info
    def test_generate_changelog_show_releases_headings_only(self):
        """Test generate changelog."""
        res = generate_changelog(
            include_other=False,
            show_releases=True,
            headings_only=True,
            path=self.test_dir
        ).strip()

        self.assertEqual(
            res,
            self.show_releases_headings_only_out
        )
        return res

    @log_info
    def test_generate_changelog_show_releases_unreleased_only(self):
        """Test generate changelog."""
        self.repo.checkout('test')
        self.repo.checkout('master')
        res = generate_changelog(
            between='master..test',
            include_other=False,
            show_releases=True,
            headings_only=False,
            unreleased_only=True,
            path=self.test_dir
        ).strip()

        self.assertEqual(
            res,
            self.show_releases_unreleased_only_out
        )
        return res

    @log_info
    def test_json_changelog(self):
        """Test JSON changelog."""
        res = json_changelog(
            include_other=False,
            path=self.test_dir
        )
        self.assertEqual(str(res), self.json_no_args_out)
        return res

    @log_info
    def test_json_changelog_show_releases(self):
        """Test json changelog."""
        res = json_changelog(
            include_other=False,
            show_releases=True,
            path=self.test_dir
        )
        self.assertEqual(str(res), self.json_show_releases_out)
        return res

    @log_info
    def test_json_changelog_latest_release_show_releases(self):
        """Test json changelog."""
        res = json_changelog(
            include_other=False,
            show_releases=True,
            latest_release=True,
            path=self.test_dir
        )
        self.assertEqual(
            str(res),
            self.json_latest_release_show_releases_out
        )
        return res

    @log_info
    def test_json_changelog_show_releases_headings_only(self):
        """Test json changelog."""
        res = json_changelog(
            include_other=False,
            show_releases=True,
            headings_only=True,
            path=self.test_dir
        )
        self.assertEqual(
            str(res),
            self.json_show_releases_headings_only_out
        )
        return res

    # @log_info
    # def test_json_changelog_show_releases_unreleased_only(self):
    #     """Test json changelog."""
    #     res = json_changelog(
    #         include_other=False,
    #         show_releases=True,
    #         headings_only=True,
    #         path=self.test_dir
    #     )
    #     self.assertEqual(
    #         str(res),
    #         self.json_show_releases_headings_only_out
    #     )
    #     return res

    @log_info
    def test_make_config_file(self):
        """Test make config file."""
        res = make_config_file()
        self.assertTrue(res)
        return res

    @log_info
    def test_merge_branch_patterns(self):
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
