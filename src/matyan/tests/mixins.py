import os
import git
import shutil

from ..helpers import project_dir
from ..utils import get_repository

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'ChangelogMixin',
)


class ChangelogMixin:
    """Changelog mixin."""

    @classmethod
    def clean_up(cls):
        """Clean up."""
        shutil.rmtree(os.path.join(cls.test_dir, 'htmlcov'), ignore_errors=True)
        ini_file_path = os.path.join(cls.test_dir, '.matyan.ini')
        if os.path.exists(ini_file_path):
            os.remove(ini_file_path)

    @classmethod
    def prepare_changelog_data(cls):
        """Prepare data."""
        # if is_internet_available() or is_travis():
        # Test directory for cloning the repo
        cls.test_dir = project_dir("tests/matyan-testing")
        if not os.path.exists(cls.test_dir):
            git.Repo.clone_from(
                "https://barseghyanartur@bitbucket.org/barseghyanartur/matyan-testing.git",  # NOQA
                cls.test_dir,
                StrictHostKeyChecking=False
            )
            cls.repo = get_repository(cls.test_dir)
        else:
            cls.repo = get_repository(cls.test_dir)
            cls.repo.pull()

        # Go to cloned repository
        os.chdir(cls.test_dir)

        # ************************** Markdown *******************************

        # Expected output of the `generate-changelog` command.
        no_args_out = project_dir(
            'tests/output/generate-changelog.md'
        )
        with open(no_args_out, 'r') as file:
            cls.no_args_out = file.read().strip()

        # Expected output of the `generate-changelog --show-releases`
        # command.
        show_releases_out = project_dir(
            'tests/output/generate-changelog-show-releases.md'
        )
        with open(show_releases_out, 'r') as file:
            cls.show_releases_out = file.read().strip()

        # Expected output of the `generate-changelog --show-releases
        # --renderer=historical-markdown` command.
        show_releases_rend_hist_out = project_dir(
            'tests/output/generate-changelog-show-releases-rend-hist.md'
        )
        with open(show_releases_rend_hist_out, 'r') as file:
            cls.show_releases_rend_hist_out = file.read().strip()

        # Expected output of the
        # `generate-changelog --show-releases --latest-release`
        # command.
        latest_release_show_releases_out = project_dir(
            'tests/output/generate-changelog-latest-release-show-releases.md'
        )
        with open(latest_release_show_releases_out, 'r') as file:
            cls.latest_release_show_releases_out = file.read().strip()

        # Expected output of the
        # `generate-changelog --show-releases --headings-only`
        # command.
        show_releases_headings_only_out = project_dir(
            'tests/output/generate-changelog-show-releases-headings-only.md'
        )
        with open(show_releases_headings_only_out, 'r') as file:
            cls.show_releases_headings_only_out = file.read().strip()

        # Expected output of the
        # `generate-changelog --headings-only`
        # command.
        headings_only_out = project_dir(
            'tests/output/generate-changelog-headings-only.md'
        )
        with open(headings_only_out, 'r') as file:
            cls.headings_only_out = file.read().strip()

        # Expected output of the
        # `generate-changelog --show-releases --unreleased-only`
        # command.
        show_releases_unreleased_only_out = project_dir(
            'tests/output/generate-changelog-show-releases-unreleased-only.md'
        )
        with open(show_releases_unreleased_only_out, 'r') as file:
            cls.show_releases_unreleased_only_out = file.read().strip()

        # *********************** Restructured text ***********************

        # Expected output of the `generate-changelog --show-releases`
        # command.
        show_releases_rst_out = project_dir(
            'tests/output/generate-changelog-show-releases.rst'
        )
        with open(show_releases_rst_out, 'r') as file:
            cls.show_releases_rst_out = file.read().strip()

        # **************************** JSON *******************************

        # Expected output of the `json-changelog` command.
        json_no_args_out = project_dir(
            'tests/output/json-changelog.json'
        )
        with open(json_no_args_out, 'r') as file:
            cls.json_no_args_out = file.read().strip()

        # Expected output of the `json-changelog --show-releases`
        # command.
        json_show_releases_out = project_dir(
            'tests/output/json-changelog-show-releases.json'
        )
        with open(json_show_releases_out, 'r') as file:
            cls.json_show_releases_out = file.read().strip()

        # Expected output of the
        # `json-changelog --show-releases --latest-release`
        # command.
        json_latest_release_show_releases_out = project_dir(
            'tests/output/json-changelog-latest-release-show-releases.json'
        )
        with open(json_latest_release_show_releases_out, 'r') as file:
            cls.json_latest_release_show_releases_out = file.read().strip()

        # Expected output of the
        # `json-changelog --show-releases --headings-only`
        # command.
        json_show_releases_headings_only_out = project_dir(
            'tests/output/json-changelog-show-releases-headings-only.json'
        )
        with open(json_show_releases_headings_only_out, 'r') as file:
            cls.json_show_releases_headings_only_out = file.read().strip()

        # Expected output of the
        # `json-changelog --headings-only`
        # command.
        json_headings_only_out = project_dir(
            'tests/output/json-changelog-headings-only.json'
        )
        with open(json_headings_only_out, 'r') as file:
            cls.json_headings_only_out = file.read().strip()
