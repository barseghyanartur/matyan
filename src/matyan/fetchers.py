from typing import Union, Dict, Any

from atlassian import Jira

from .config import CONFIG
from .registry import Registry

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'BaseFetcher',
    'JiraFetcher',
)


class BaseFetcher(metaclass=Registry):

    uid: str = None
    instance: Union[Jira]

    def __init__(self, *args, **kwargs):
        if not self.uid:
            raise NotImplementedError

        self.instance = self.get_instance()

    def get_config(self) -> Dict[str, str]:
        return dict(CONFIG[self.uid])

    def get_instance(self) -> Union[Jira]:
        raise NotImplementedError

    def fetch_issue_data(self, issue_id: str) -> Dict[str, str]:
        raise NotImplementedError


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
        issue = self.instance.issue(issue_id)
        return {
            'title': issue['fields']['summary'],
            'description': issue['fields']['description'],
        }
