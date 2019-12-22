from typing import Dict
from textwrap import indent

from ..labels import BRANCH_TYPES, BRANCH_TYPE_OTHER
from .base import BaseRenderer

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'RestructuredTextRenderer',
)


class RestructuredTextRenderer(BaseRenderer):

    uid: str = 'rest'

    def append_release(self, release_label: str):
        self.changelog.append(
            "\n{}\n{}".format(
                release_label,
                "-" * len(release_label)
            )
        )

    def append_feature_type(self, branch_type: str):
        branch_type_label = BRANCH_TYPES.get(branch_type)
        self.changelog.append(
            "\n{}\n{}{}".format(
                branch_type_label,
                "~" * len(branch_type_label),
                '\n' if branch_type == BRANCH_TYPE_OTHER else ''
            )
        )

    def append_ticket_title(self, ticket_number: str, ticket_title: str):
        ticket_title_label = "{} {}".format(ticket_number, ticket_title)
        self.changelog.append(
            "\n{}\n{}".format(
                ticket_title_label,
                "^" * len(ticket_title_label)
            )
        )

    def append_ticket_description(self, ticket_description: str):
        self.changelog.append(
            "\n.. code-block: text\n\n{}".format(
                indent(ticket_description.strip(), "    ")
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
