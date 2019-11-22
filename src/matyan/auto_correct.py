from typing import AnyStr

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'add_final_dot',
    'capitalize',
    'unslugify',
)


def unslugify(value: AnyStr) -> AnyStr:
    return value.replace('-', ' ').title() if value else ''


def capitalize(value: AnyStr) -> AnyStr:
    if len(value) == 0:
        return value
    return '. '.join([val.strip().capitalize() for val in value.split('.')]).strip()


def add_final_dot(value: AnyStr) -> AnyStr:
    if len(value) and value[-1].isalnum():
        return value + "."
    return value
