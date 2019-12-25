__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'PRETTY_FORMAT',
    'TICKET_NUMBER_OTHER',
)

PRETTY_FORMAT = '{' \
                '"commit_hash": "%H", ' \
                '"commit_abbr": "%h", ' \
                '"datetime": "%ci", ' \
                '"title": "%s",' \
                '"author": "%an", ' \
                '"author_email": "%ae", ' \
                '"merge": "%P"' \
                '}'

TICKET_NUMBER_OTHER = 'other'
