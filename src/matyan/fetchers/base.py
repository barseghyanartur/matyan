from typing import Dict, Type

from ..config import CONFIG
from ..registry import Registry

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'BaseFetcher',
)


class BaseFetcher(metaclass=Registry):

    uid: str = None
    instance: Type

    def __init__(self, *args, **kwargs):
        if not self.uid:
            raise NotImplementedError

        self.instance = self.get_instance()

    def get_config(self) -> Dict[str, str]:
        return dict(CONFIG[self.uid])

    def get_instance(self) -> Type:
        raise NotImplementedError

    def fetch_issue_data(self, issue_id: str) -> Dict[str, str]:
        raise NotImplementedError
