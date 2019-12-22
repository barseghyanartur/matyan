from typing import Dict

from ..labels import BRANCH_TYPES, BRANCH_TYPE_OTHER
from .base import BaseRenderer

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'MarkdownRenderer',
    'HistoricalMarkdownRenderer',
)


class MarkdownRenderer(BaseRenderer):

    uid: str = 'markdown'

    def append_release(self, release_label: str):
        self.changelog.append("\n### {}".format(release_label))

    def append_feature_type(self, branch_type: str):
        self.changelog.append(
            "\n#### {}{}".format(
                BRANCH_TYPES.get(branch_type),
                '\n' if branch_type == BRANCH_TYPE_OTHER else ''
            )
        )

    def append_ticket_title(self, ticket_number: str, ticket_title: str):
        self.changelog.append(
            "\n##### {} {}".format(
                ticket_number,
                ticket_title
            )
        )

    def append_ticket_description(self, ticket_description: str):
        self.changelog.append(
            "\n```\n{}\n```".format(
                ticket_description.strip()
            )
        )

    def append_commit_message(self,
                              commit_data: Dict[str, str],
                              branch_type: str,
                              counter: int = 0):
        self.changelog.append(
            "{}- {} [{}]".format(
                (
                    '\n'
                    if counter == 0 and branch_type != BRANCH_TYPE_OTHER
                    else ''
                ),
                commit_data['title'],
                commit_data['author']
            )
        )


class HistoricalMarkdownRenderer(MarkdownRenderer):

    uid: str = 'historical-markdown'

    def append_release(self, release_label: str):
        self.changelog.append("\n### {}".format(release_label))

    def append_feature_type(self, branch_type: str):
        self.changelog.append(
            "\n**{}**{}".format(
                BRANCH_TYPES.get(branch_type),
                '\n' if branch_type == BRANCH_TYPE_OTHER else ''
            )
        )

    def append_ticket_title(self, ticket_number: str, ticket_title: str):
        self.changelog.append(
            "\n*{} {}*".format(
                ticket_number,
                ticket_title
            )
        )
