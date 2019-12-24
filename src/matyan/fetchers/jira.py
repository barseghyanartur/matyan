import logging
from typing import Dict

from atlassian import Jira

from .base import BaseFetcher

LOGGER = logging.getLogger(__name__)

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'BaseFetcher',
    'JiraFetcher',
)


class JiraFetcher(BaseFetcher):

    uid: str = 'Jira'
    instance: Jira

    def get_instance(self) -> Jira:
        config = self.get_config()
        return Jira(
            url=config["url"],
            username=config["username"],
            password=config["token"]
        )

    def fetch_issue_data(self, issue_id: str) -> Dict[str, str]:
        if not self.should_continue():
            LOGGER.debug("Skip after number of retries reached")
            return {}

        try:
            issue = self.instance.issue(issue_id)
            return {
                'title': issue['fields']['summary'],
                'description': issue['fields']['description'],
            }
        except (TypeError, KeyError, IOError) as err:
            self.register_error()
            return {}
