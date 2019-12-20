from typing import Dict

from ..labels import BRANCH_TYPES, BRANCH_TYPE_OTHER, UNRELEASED_LABEL, UNRELEASED
from .base import BaseRenderer

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'MarkdownRenderer',
)


class MarkdownRenderer(BaseRenderer):

    uid: str = 'markdown'

    def render_changelog(self,
                         tree: dict,
                         include_other: bool,
                         headings_only: bool,
                         show_description: bool) -> str:
        changelog = []
        for branch_type, tickets in tree.items():
            # Skip adding orphaned commits if explicitly asked not to.
            if branch_type == BRANCH_TYPE_OTHER and not include_other:
                continue

            # Do not add branch type if no related branches found
            if not tickets:
                continue

            if BRANCH_TYPES.get(branch_type):
                changelog.append(
                    "\n**{}**{}".format(
                        BRANCH_TYPES.get(branch_type),
                        '\n' if branch_type == BRANCH_TYPE_OTHER else ''
                    )
                )

            # Add tickets
            for ticket_number, ticket_data in tickets.items():
                if 'title' not in ticket_data:
                    continue

                if branch_type != BRANCH_TYPE_OTHER:
                    changelog.append(
                        "\n*{} {}*".format(
                            ticket_number,
                            ticket_data['title']
                        )
                    )
                    if show_description and ticket_data['description']:
                        changelog.append(
                            "\n```\n{}\n```".format(
                                ticket_data['description'].strip()
                            )
                        )

                if headings_only:
                    continue

                counter = 0
                for commit_hash, commit_data in ticket_data['commits'].items():
                    changelog.append(
                        "{}- {} [{}]".format(
                            '\n' if counter == 0 and branch_type != BRANCH_TYPE_OTHER else '',
                            commit_data['title'],
                            commit_data['author']
                        )
                    )
                    counter = counter + 1
        return '\n'.join(changelog)

    def render_releases_changelog(self,
                                  releases_tree: dict,
                                  include_other: bool,
                                  headings_only: bool,
                                  show_description: bool) -> str:
        changelog = []
        for release, branches in releases_tree.items():
            release_label = UNRELEASED_LABEL \
                if release == UNRELEASED \
                else release

            changelog.append("\n### {}".format(release_label))
            for branch_type, tickets in branches.items():

                # Skip adding orphaned commits if explicitly asked not to.
                if branch_type == BRANCH_TYPE_OTHER and not include_other:
                    continue

                # Do not add branch type if no related branches found
                if not tickets:
                    continue

                if BRANCH_TYPES.get(branch_type):
                    changelog.append(
                        "\n**{}**{}".format(
                            BRANCH_TYPES.get(branch_type),
                            '\n' if branch_type == BRANCH_TYPE_OTHER else ''
                        )
                    )

                # Add tickets
                for ticket_number, ticket_data in tickets.items():
                    if 'title' not in ticket_data:
                        continue

                    if branch_type != BRANCH_TYPE_OTHER:
                        changelog.append(
                            "\n*{} {}*".format(
                                ticket_number,
                                ticket_data['title']
                            )
                        )

                        if show_description and ticket_data['description']:
                            changelog.append(
                                "\n```\n{}\n```".format(
                                    ticket_data['description'].strip()
                                )
                            )

                    if headings_only:
                        continue

                    counter = 0
                    for commit_hash, commit_data in ticket_data[
                        'commits'].items():  # NOQA
                        changelog.append(
                            "{}- {} [{}]".format(
                                '\n' if counter == 0 and branch_type != BRANCH_TYPE_OTHER else '',
                                commit_data['title'],
                                commit_data['author']
                            )
                        )
                        counter = counter + 1

        return '\n'.join(changelog)
