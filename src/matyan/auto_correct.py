from typing import AnyStr

__author__ = 'Artur Barseghyan'
__copyright__ = '2019-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'add_final_dot',
    'capitalize',
    'capitalize_first_letter',
    'unslugify',
)


def capitalize_first_letter(value: AnyStr) -> AnyStr:
    """Capitalize first letter of the given string.

    :param value:
    :return:
    """
    if len(value) == 0:
        return value
    return value[0].upper() + value[1:]


def unslugify(value: AnyStr) -> AnyStr:
    """Un-slugify. Opposite of slugify.

    :param value:
    :return:
    """
    return capitalize_first_letter(value.replace('-', ' ')) if value else ''


def capitalize(value: AnyStr) -> AnyStr:
    """Capitalize.

    Make each first letter of each first word in the sentence uppercase.

    :param value:
    :return:
    """
    if len(value) == 0:
        return value
    return '. '.join(
        [capitalize_first_letter(val.strip()) for val in value.split('. ')]
    ).strip()


def add_final_dot(value: AnyStr) -> AnyStr:
    """Add final dot at the end of the sentence.

    :param value:
    :return:
    """
    if len(value) and value[-1].isalnum() and not value.endswith('.'):
        return value + "."
    return value
