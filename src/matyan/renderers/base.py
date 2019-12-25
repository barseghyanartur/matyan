from typing import Dict, Type, List

from ..config import CONFIG
from ..labels import BRANCH_TYPES, BRANCH_TYPE_OTHER, UNRELEASED_LABEL, UNRELEASED
from ..logger import LOGGER
from ..registry import Registry

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'BaseRenderer',
    'RendererRegistry',
)


class RendererRegistry(Registry):
    """Renderer registry."""

    REGISTRY: Dict[str, Type] = {}


class AbstractRenderer(metaclass=RendererRegistry):

    uid: str = None
    instance: Type
    changelog: List[str] = []

    def __init__(self, *args, **kwargs):
        if not self.uid:
            raise NotImplementedError

    def get_config(self) -> Dict[str, str]:
        return dict(CONFIG[self.uid])

    def render_changelog(self,
                         tree: dict,
                         include_other: bool,
                         headings_only: bool,
                         show_description: bool) -> str:
        raise NotImplementedError

    def render_releases_changelog(self,
                                  releases_tree: dict,
                                  include_other: bool,
                                  headings_only: bool,
                                  show_description: bool) -> str:
        raise NotImplementedError


class BaseRenderer(AbstractRenderer):

    def append_release(self, release_label: str):
        raise NotImplementedError

    def append_feature_type(self, branch_type: str):
        raise NotImplementedError

    def append_ticket_title(self, ticket_number: str, ticket_title: str):
        raise NotImplementedError

    def append_ticket_description(self, ticket_description: str):
        raise NotImplementedError

    def append_commit_message(self,
                              commit_data: Dict[str, str],
                              branch_type: str,
                              counter: int = 0):
        raise NotImplementedError

    def render_changelog(self,
                         tree: dict,
                         include_other: bool,
                         headings_only: bool,
                         fetch_description: bool) -> str:
        # changelog = []
        self.changelog = []
        for branch_type, tickets in tree.items():
            # Skip adding orphaned commits if explicitly asked not to.
            if branch_type == BRANCH_TYPE_OTHER and not include_other:
                continue

            # Do not add branch type if no related branches found
            if not tickets:
                continue

            if BRANCH_TYPES.get(branch_type):
                # Feature type label `append_feature_type`
                self.append_feature_type(branch_type)
                # changelog.append(
                #     "\n**{}**{}".format(
                #         BRANCH_TYPES.get(branch_type),
                #         '\n' if branch_type == BRANCH_TYPE_OTHER else ''
                #     )
                # )

            # Add tickets
            for ticket_number, ticket_data in tickets.items():
                if 'title' not in ticket_data:
                    continue

                if branch_type != BRANCH_TYPE_OTHER:
                    # Ticket name `append_ticket_title`
                    self.append_ticket_title(
                        ticket_number,
                        ticket_data['title']
                    )
                    # changelog.append(
                    #     "\n*{} {}*".format(
                    #         ticket_number,
                    #         ticket_data['title']
                    #     )
                    # )

                    if fetch_description and ticket_data['description']:
                        # Description quote `append_ticket_description`
                        self.append_ticket_description(
                            ticket_data['description']
                        )
                        # changelog.append(
                        #     "\n```\n{}\n```".format(
                        #         ticket_data['description'].strip()
                        #     )
                        # )

                if headings_only:
                    continue

                counter = 0
                for commit_hash, commit_data in ticket_data['commits'].items():
                    # Commit text `append_commit_message`
                    self.append_commit_message(
                        commit_data=commit_data,
                        branch_type=branch_type,
                        counter=counter
                    )
                    # changelog.append(
                    #     "{}- {} [{}]".format(
                    #         '\n' if counter == 0 and branch_type != BRANCH_TYPE_OTHER else '',
                    #         commit_data['title'],
                    #         commit_data['author']
                    #     )
                    # )
                    counter = counter + 1

        # return '\n'.join(changelog)
        return '\n'.join(self.changelog)

    def render_releases_changelog(self,
                                  releases_tree: dict,
                                  include_other: bool,
                                  headings_only: bool,
                                  fetch_description: bool) -> str:
        # changelog = []
        self.changelog = []
        for release, branches in releases_tree.items():
            release_label = UNRELEASED_LABEL \
                if release == UNRELEASED \
                else release

            # Release label `append_release`
            self.append_release(release_label)
            # changelog.append("\n### {}".format(release_label))

            for branch_type, tickets in branches.items():

                # Skip adding orphaned commits if explicitly asked not to.
                if branch_type == BRANCH_TYPE_OTHER and not include_other:
                    continue

                # Do not add branch type if no related branches found
                if not tickets:
                    continue

                # Feature type label `append_feature_type`
                if BRANCH_TYPES.get(branch_type):
                    self.append_feature_type(branch_type)
                    # changelog.append(
                    #     "\n**{}**{}".format(
                    #         BRANCH_TYPES.get(branch_type),
                    #         '\n' if branch_type == BRANCH_TYPE_OTHER else ''
                    #     )
                    # )

                # Add tickets
                for ticket_number, ticket_data in tickets.items():
                    # TODO: Investigate why this needs to be here at all?
                    # if 'title' not in ticket_data:
                    #     LOGGER.warning('NO title in ticket_data')
                    #     LOGGER.warning(ticket_number)
                    #     LOGGER.warning(ticket_data)
                    #     # continue
                    # else:
                    #     LOGGER.warning('title IS in ticket_data')
                    #     LOGGER.warning(ticket_number)
                    #     LOGGER.warning(ticket_data)

                    if branch_type != BRANCH_TYPE_OTHER:
                        # Ticket name `append_ticket_title`
                        self.append_ticket_title(
                            ticket_number,
                            ticket_data['title']
                        )
                        # changelog.append(
                        #     "\n*{} {}*".format(
                        #         ticket_number,
                        #         ticket_data['title']
                        #     )
                        # )

                        if fetch_description and ticket_data['description']:
                            # Description quote `append_ticket_description`
                            self.append_ticket_description(
                                ticket_data['description']
                            )
                            # changelog.append(
                            #     "\n```\n{}\n```".format(
                            #         ticket_data['description'].strip()
                            #     )
                            # )

                    if headings_only:
                        continue

                    counter = 0
                    for commit_hash, commit_data in ticket_data['commits'].items():  # NOQA
                        # Commit text `append_commit_message`
                        self.append_commit_message(
                            commit_data=commit_data,
                            branch_type=branch_type,
                            counter=counter
                        )
                        # changelog.append(
                        #     "{}- {} [{}]".format(
                        #         '\n' if counter == 0 and branch_type != BRANCH_TYPE_OTHER else '',
                        #         commit_data['title'],
                        #         commit_data['author']
                        #     )
                        # )
                        counter = counter + 1

        # return '\n'.join(changelog)
        return '\n'.join(self.changelog)
