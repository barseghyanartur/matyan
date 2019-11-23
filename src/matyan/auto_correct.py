from typing import AnyStr

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'add_final_dot',
    'capitalize',
    'capitalize_first_letter',
    'unslugify',
)


def capitalize_first_letter(value: AnyStr) -> AnyStr:
    if len(value) == 0:
        return value
    return value[0].upper() + value[1:]


def unslugify(value: AnyStr) -> AnyStr:
    return capitalize_first_letter(value.replace('-', ' ')) if value else ''


def capitalize(value: AnyStr) -> AnyStr:
    if len(value) == 0:
        return value
    return '. '.join(
        [capitalize_first_letter(val.strip()) for val in value.split('.')]
    ).strip()


def add_final_dot(value: AnyStr) -> AnyStr:
    if len(value) and value[-1].isalnum() and not value.endswith('.'):
        return value + "."
    return value
