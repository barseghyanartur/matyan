from .config import CONFIG

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'REGEX_PATTERN_BRANCH_NAME',
    'REGEX_PATTERN_BRANCH_TYPE',
    'REGEX_PATTERN_COMMIT',
    'REGEX_PATTERN_COMMIT_LINE',
    'REGEX_PATTERN_MERGED_BRANCH_NAME',
    'REGEX_PATTERN_TAG',
)


def get_branch_types_for_regex() -> str:
    """Get branch types for regular expression.

    :return:
    """
    branches_regex_list = []
    for branch_key in dict(CONFIG['BranchTypes']).keys():
        branches_regex_list.append(
            r'({FIRST_LETTER}|{first_letter}){the_rest}'.format(
                FIRST_LETTER=branch_key[0].upper(),
                first_letter=branch_key[0].lower(),
                the_rest=branch_key[1:]
            )
        )
    return r'|'.join(branches_regex_list)


REGEX_PATTERN_BRANCH_TYPE = r'(((?P<branch_type>{branch_types}))\/)?'.format(
    branch_types=get_branch_types_for_regex()
)


REGEX_PATTERN_BRANCH_NAME = REGEX_PATTERN_BRANCH_TYPE + \
    r'((?P<ticket_number>[a-zA-Z]{1,12}-\d{1,12})-)?' \
    r'(?P<branch_title>[a-zA-Z-\d]*)'

REGEX_PATTERN_MERGED_BRANCH_NAME = r'(\s*)' \
                                   r'(' \
                                   r'(Merged in )|' \
                                   r'(Merge pull request .* from )' \
                                   r')' + \
                                   REGEX_PATTERN_BRANCH_NAME

REGEX_PATTERN_COMMIT = r'(?P<ticket_number>[a-zA-Z]{1,12}-\d{1,12})?'
REGEX_PATTERN_COMMIT_LINE = r'(\s*)' + \
                            REGEX_PATTERN_COMMIT + \
                            r'\s?(?P<commit_message>.*)'


REGEX_PATTERN_TAG = r'(?P<tag>((\d{1,12}\.)+(\d)+))'
