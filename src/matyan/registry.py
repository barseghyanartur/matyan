from typing import Dict, Type

__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'MPL-1.1 OR GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'Registry',
)


class Registry(type):
    """Base registry."""

    REGISTRY: Dict[str, Type]

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        # Here the name of the class is used as key but it could be any class
        # parameter.
        if getattr(new_cls, '_uid', None):
            cls.REGISTRY[new_cls._uid] = new_cls
        return new_cls

    @property
    def _uid(cls) -> str:
        return getattr(cls, 'uid', cls.__name__)

    @classmethod
    def reset(cls) -> None:
        cls.REGISTRY = {}

    @classmethod
    def get(cls, key, default=None):
        return cls.REGISTRY.get(key, default)

    @classmethod
    def items(cls):
        return cls.REGISTRY.items()
