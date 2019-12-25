from typing import Dict, Type

from ..config import CONFIG
from ..registry import Registry

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'BaseFetcher',
    'FetcherRegistry',
)


class FetcherRegistry(Registry):
    """Fetcher registry."""

    REGISTRY: Dict[str, Type] = {}


class BaseFetcher(metaclass=FetcherRegistry):

    uid: str = None
    instance: Type
    retries: int = 0
    max_retries: int = 10

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

    def should_continue(self) -> bool:
        return self.retries < self.max_retries

    def register_error(self) -> None:
        self.retries += 1
