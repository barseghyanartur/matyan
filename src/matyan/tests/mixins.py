import os
import git

from ..helpers import project_dir

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'ChangelogMixin',
)


class ChangelogMixin:
    """Changelog mixin."""

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

        # Go to cloned repository
        os.chdir(cls.test_dir)

        # ************************** Markdown *******************************

        # Expected output of the `generate-changelog` command.
        changelog_output = project_dir(
            'tests/output/generate-changelog.md'
        )
        with open(changelog_output, 'r') as file:
            cls.changelog_output = file.read().strip()

        # Expected output of the `generate-changelog --show-releases`
        # command.
        changelog_releases_output = project_dir(
            'tests/output/generate-changelog-show-releases.md'
        )
        with open(changelog_releases_output, 'r') as file:
            cls.changelog_releases_output = file.read().strip()

        # Expected output of the
        # `generate-changelog --show-releases --latest-release`
        # command.
        changelog_latest_release_show_releases_output = project_dir(
            'tests/output/generate-changelog-latest-release-show-releases.md'
        )
        with open(changelog_latest_release_show_releases_output, 'r') as file:
            cls.changelog_latest_release_show_releases_output \
                = file.read().strip()

        # **************************** JSON *******************************

        # Expected output of the `json-changelog` command.
        json_output = project_dir(
            'tests/output/json-changelog.json'
        )
        with open(json_output, 'r') as file:
            cls.json_output = file.read().strip()

        # Expected output of the `json-changelog --show-releases`
        # command.
        json_show_releases_output = project_dir(
            'tests/output/json-changelog-show-releases.json'
        )
        with open(json_show_releases_output, 'r') as file:
            cls.json_show_releases_output = file.read().strip()

        # Expected output of the
        # `json-changelog --show-releases --latest-release`
        # command.
        json_latest_release_show_releases_output = project_dir(
            'tests/output/json-changelog-latest-release-show-releases.json'
        )
        with open(json_latest_release_show_releases_output, 'r') as file:
            cls.json_latest_release_show_releases_output \
                = file.read().strip()
