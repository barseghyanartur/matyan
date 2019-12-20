from typing import Dict, Type

from ..config import CONFIG
from ..registry import Registry

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'BaseRenderer',
)


class BaseRenderer(metaclass=Registry):

    uid: str = None
    instance: Type

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
