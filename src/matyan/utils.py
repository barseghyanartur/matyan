import argparse
import copy
import json
import os
import re
import sys
from shutil import copyfile
from pprint import pprint
from typing import Union, Dict, AnyStr, Type, Any
import git
from git.exc import GitCommandError

from .labels import (
    get_all_branch_types,
    get_other_branch_type,
    get_branch_types,
    get_unreleased,
    get_other_branch_type_key,
    get_unreleased_key,
    get_unreleased_key_label,
    get_ignore_commits_exact_words,
)
from .helpers import project_dir
from .patterns import (
    REGEX_PATTERN_BRANCH_NAME,
    REGEX_PATTERN_MERGED_BRANCH_NAME,
    REGEX_PATTERN_COMMIT,
    REGEX_PATTERN_COMMIT_LINE,
    REGEX_PATTERN_TAG,
)

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'create_config_file',
    'generate_changelog_cli',
    'generate_empty_tree',
    'get_branch_type',
    'get_logs',
    'json_changelog_cli',
    'prepare_changelog',
    'prepare_releases_changelog',
    'validate_between',
)

REPOSITORY = git.Git(os.getcwd())

PRETTY_FORMAT = '{' \
                '"commit_hash": "%H", ' \
                '"commit_abbr": "%h", ' \
                '"datetime": "%ci", ' \
                '"title": "%s",' \
                '"author": "%an", ' \
                '"author_email": "%ae", ' \
                '"merge": "%P"' \
                '}'

BRANCH_TYPE_OTHER = get_other_branch_type_key()  # 'other'
BRANCH_TYPES = get_all_branch_types()
# BRANCH_TYPES = {
#     'other': "Other",
#     'feature': "Features",
#     'bugfix': "Bugfixes",
#     'hotfix': "Hotfixes",
#     'deprecation': "Deprecations",
# }
TICKET_NUMBER_OTHER = 'other'
# UNRELEASED = 'unreleased'
UNRELEASED, UNRELEASED_LABEL = get_unreleased_key_label()

IGNORE_COMMITS_EXACT_WORDS = get_ignore_commits_exact_words()


def get_logs(between: str = None) -> Dict[str, Any]:
    """Get lots of logs.

    :param between:
    :return:
    """
    lower: Union[str, Type[None]] = None
    upper: Union[str, Type[None]] = None
    if between:
        try:
            rev_list_text = REPOSITORY.rev_list(between)
            rev_list = rev_list_text.split('\n')
            if len(rev_list) >= 2:
                upper = rev_list[0]
                lower = rev_list[-1]
        except GitCommandError as err:
            pass

    # Merges log
    text_log_merges_args = []
    if lower and upper:
        text_log_merges_args.append(
            "{}..{}".format(lower, upper)
        )
    text_log_merges_args.extend([
        "--pretty={}".format(PRETTY_FORMAT),
        "--source",
        # "--all",
        "--merges",
    ])
    text_log_merges = REPOSITORY.log(*text_log_merges_args)
    log_merges = text_log_merges.split("\n")

    # Commits log
    text_log_args = []
    if lower and upper:
        text_log_args.append(
            "{}..{}".format(lower, upper)
        )
    text_log_args.extend([
        "--pretty={}".format(PRETTY_FORMAT),
        "--source",
        # "--all"  # TODO: remove
    ])

    text_log = REPOSITORY.log(*text_log_args)
    log = text_log.split("\n")

    # Tags log
    text_log_tags = REPOSITORY.log(
        "--tags",
        "--source",
        "--oneline"
    )
    log_tags = text_log_tags.split("\n")
    commit_tags = dict([s.split(' ', 1)[0].split('\t') for s in log_tags])

    return {
        'TEXT_LOG_MERGES': text_log_merges,
        'LOG_MERGES': log_merges,
        'TEXT_LOG': text_log,
        'LOG': log,
        'TEXT_LOG_TAGS': text_log_tags,
        'LOG_TAGS': log_tags,
        'COMMIT_TAGS': commit_tags,
    }


def get_branch_type(branch_type: AnyStr) -> str:
    """Get branch type.

    :param branch_type:
    :return:
    """
    branch_type = branch_type.lower()
    return branch_type if branch_type in BRANCH_TYPES else BRANCH_TYPE_OTHER


def generate_empty_tree() -> Dict[str, dict]:
    """Generate empty tree.

    Example:

        {
            'feature': {},
            'bugfix': {},
            'hotfix': {},
            'deprecation': {},
            'other': {
                TICKET_NUMBER_OTHER: {
                    # 'title': '',
                    'commits': {}
                }
            },
        }

    :return:
    """
    empty_tree = {}
    for key, value in BRANCH_TYPES.items():
        empty_tree.update({key: {}})

    empty_tree[BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER] = {'commits': {}}
    return empty_tree


def prepare_changelog(
    between: str = None,
    unique_commit_messages: bool = False
) -> Dict[
        str, Dict[str, Dict[str, Union[str, Dict[str, Union[str, str]]]]]
]:
    """Prepare changelog.

    :param between:
    :param unique_commit_messages:
    :return:
    """
    tree = generate_empty_tree()

    cur_branch = None
    cur_branch_type = None
    branch_types = {}

    logs = get_logs(between=between)

    # First fill feature branches only
    for json_entry in logs['LOG_MERGES']:
        entry = json.loads(json_entry)
        merge_commit = True if ' ' in entry['merge'] else False
        if merge_commit:
            match = re.match(REGEX_PATTERN_MERGED_BRANCH_NAME, entry['title'])

            # Skip strange feature branches
            if not match:
                continue

            # If no pattern found, use other branch
            try:
                branch_type = get_branch_type(match.group('branch_type'))
            except AttributeError:
                branch_type = BRANCH_TYPE_OTHER

            # If no pattern found, use other ticket number
            try:
                ticket_number = match.group('ticket_number')
            except AttributeError:
                ticket_number = TICKET_NUMBER_OTHER

            branch_title = match.group('branch_title')

            # For normal tree
            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])
            if ticket_number not in tree[branch_type]:
                tree[branch_type][ticket_number] = {
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'ticket_number': ticket_number,
                    'branch_type': branch_type,
                    'slug': branch_title,
                    'title': branch_title.replace('-', ' ').title(),
                    'commits': {},
                    'release': release,
                }
            branch_types.update({ticket_number: branch_type})

    # Now go through commits
    for json_entry in filter(None, logs['LOG']):
        try:
            entry = json.loads(json_entry)
        except json.decoder.JSONDecodeError:
            continue  # TODO: fix this (when commit message contains " symbols)
        merge_commit = True if ' ' in entry['merge'] else False
        if merge_commit:
            match = re.match(REGEX_PATTERN_MERGED_BRANCH_NAME, entry['title'])

            # Skip strange feature branches
            if not match:
                continue

            try:
                branch_type = get_branch_type(match.group('branch_type'))
            except AttributeError:
                branch_type = BRANCH_TYPE_OTHER

            try:
                ticket_number = match.group('ticket_number')
            except AttributeError:
                ticket_number = TICKET_NUMBER_OTHER

            branch_title = match.group('branch_title')
            cur_branch = copy.copy(ticket_number)
            cur_branch_type = copy.copy(branch_type)
        else:
            match = re.match(REGEX_PATTERN_COMMIT_LINE, entry['title'])
            try:
                ticket_number = match.group('ticket_number')
                commit_message = match.group('commit_message')
            except AttributeError:
                ticket_number = ''
                commit_message = entry['title'][:]

            # Ignore the following messages
            if commit_message.lower() in IGNORE_COMMITS_EXACT_WORDS:
                continue

            commit_hash = commit_message \
                if unique_commit_messages \
                else entry['commit_hash']

            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])

            if cur_branch:
                if cur_branch == ticket_number:
                    tree[cur_branch_type][cur_branch]['commits'][commit_hash] = {  # NOQA
                        'commit_hash': entry['commit_hash'],
                        'commit_abbr': entry['commit_abbr'],
                        'author': entry['author'],
                        'date': entry['datetime'],
                        'ticket_number': ticket_number,
                        'title': commit_message,
                    }
                else:
                    other_branch_type = branch_types.get(
                        ticket_number,
                        BRANCH_TYPE_OTHER
                    )
                    try:
                        tree[other_branch_type][ticket_number]['commits'][commit_hash] = {  # NOQA
                            'commit_hash': entry['commit_hash'],
                            'commit_abbr': entry['commit_abbr'],
                            'author': entry['author'],
                            'date': entry['datetime'],
                            'ticket_number': ticket_number,
                            'title': commit_message,
                        }
                    except:
                        # TODO: Anything here?
                        pass
            else:
                tree[BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]['commits'][commit_hash] = {  # NOQA
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'author': entry['author'],
                    'date': entry['datetime'],
                    'ticket_number': ticket_number,
                    'title': commit_message,
                }

    return tree


def prepare_releases_changelog(
    between: str = None,
    unique_commit_messages: bool = False
) -> Dict[
        str, Dict[str, Dict[str, Union[str, Dict[str, Union[str, str]]]]]
]:
    """Prepare releases changelog.

    :param between:
    :param unique_commit_messages:
    :return:
    """
    logs = get_logs(between=between)
    releases = [UNRELEASED] + [tag for tag in logs['COMMIT_TAGS'].values()]
    releases_tree = {tag: generate_empty_tree() for tag in releases}

    cur_branch = None
    cur_branch_type = None
    branch_types = {}

    # First fill feature branches only
    for json_entry in logs['LOG_MERGES']:
        entry = json.loads(json_entry)
        merge_commit = True if ' ' in entry['merge'] else False
        if merge_commit:
            match = re.match(REGEX_PATTERN_MERGED_BRANCH_NAME, entry['title'])

            # Skip strange feature branches
            if not match:
                continue

            # If no pattern found, use other branch
            try:
                branch_type = get_branch_type(match.group('branch_type'))
            except AttributeError:
                branch_type = BRANCH_TYPE_OTHER

            # If no pattern found, use other ticket number
            try:
                ticket_number = match.group('ticket_number')
            except AttributeError:
                ticket_number = TICKET_NUMBER_OTHER

            branch_title = match.group('branch_title')

            # For normal tree
            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])
            if not release:
                release = UNRELEASED

            if ticket_number not in releases_tree[release][branch_type]:
                releases_tree[release][branch_type][ticket_number] = {
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'ticket_number': ticket_number,
                    'branch_type': branch_type,
                    'slug': branch_title,
                    'title': branch_title.replace('-', ' ').title(),
                    'commits': {},
                    'release': release,
                }
            branch_types.update({ticket_number: branch_type})

    # Now go through commits
    for json_entry in filter(None, logs['LOG']):
        try:
            entry = json.loads(json_entry)
        except json.decoder.JSONDecodeError:
            continue  # TODO: fix this (when commit message contains " symbols)

        merge_commit = True if ' ' in entry['merge'] else False
        if merge_commit:
            match = re.match(REGEX_PATTERN_MERGED_BRANCH_NAME, entry['title'])

            # Skip strange feature branches
            if not match:
                continue

            try:
                branch_type = get_branch_type(match.group('branch_type'))
            except AttributeError:
                branch_type = BRANCH_TYPE_OTHER

            try:
                ticket_number = match.group('ticket_number')
            except AttributeError:
                ticket_number = TICKET_NUMBER_OTHER

            branch_title = match.group('branch_title')
            cur_branch = copy.copy(ticket_number)
            cur_branch_type = copy.copy(branch_type)
        else:
            match = re.match(REGEX_PATTERN_COMMIT_LINE, entry['title'])
            try:
                ticket_number = match.group('ticket_number')
                commit_message = match.group('commit_message')
            except AttributeError:
                ticket_number = ''
                commit_message = entry['title'][:]

            # Ignore the following messages
            if commit_message.lower() in IGNORE_COMMITS_EXACT_WORDS:
                continue

            commit_hash = commit_message \
                if unique_commit_messages \
                else entry['commit_hash']

            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])
            if not release:
                release = UNRELEASED

            if cur_branch:
                if cur_branch == ticket_number:
                    releases_tree[release][cur_branch_type][cur_branch]['commits'][commit_hash] = {  # NOQA
                        'commit_hash': entry['commit_hash'],
                        'commit_abbr': entry['commit_abbr'],
                        'author': entry['author'],
                        'date': entry['datetime'],
                        'ticket_number': ticket_number,
                        'title': commit_message,
                    }
                else:
                    other_branch_type = branch_types.get(
                        ticket_number,
                        BRANCH_TYPE_OTHER
                    )
                    try:
                        releases_tree[release][other_branch_type][ticket_number]['commits'][commit_hash] = {  # NOQA
                            'commit_hash': entry['commit_hash'],
                            'commit_abbr': entry['commit_abbr'],
                            'author': entry['author'],
                            'date': entry['datetime'],
                            'ticket_number': ticket_number,
                            'title': commit_message,
                        }
                    except:
                        # TODO: Anything here?
                        pass
            else:
                releases_tree[release][BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]['commits'][commit_hash] = {  # NOQA
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'author': entry['author'],
                    'date': entry['datetime'],
                    'ticket_number': ticket_number,
                    'title': commit_message,
                }

    return releases_tree


def validate_between(between: str = None) -> bool:
    """Validate between.

    :param between:
    :return:
    """
    if between:
        pass  # TODO
    return True


def json_changelog_cli() -> Type[None]:
    """Generate changelog (JSON format)."""
    parser = argparse.ArgumentParser(description='Generate JSON changelog')
    parser.add_argument(
        'between',
        nargs='?',
        default=None,
        help="Range, might be tag or a commit or a branch.",
    )
    parser.add_argument(
        '--no-other',
        dest="no_other",
        default=False,
        action='store_true',
        help="No `Other` section",
    )
    parser.add_argument(
        '--show-releases',
        dest="show_releases",
        default=False,
        action='store_true',
        help="Show releases",
    )
    args = parser.parse_args(sys.argv[1:])
    between = args.between if validate_between(args.between) else None
    include_other = not args.no_other
    show_releases = args.show_releases

    if not show_releases:
        tree = prepare_changelog(
            between=between,
            unique_commit_messages=True
        )
        pprint(tree)
    else:
        releases_tree = prepare_releases_changelog(
            between=between,
            unique_commit_messages=True
        )
        pprint(releases_tree)

    # if not include_other:
    #     tree.pop(BRANCH_TYPE_OTHER)
    # pprint(tree)


def generate_changelog() -> str:
    """Generate changelog (markdown format)."""
    parser = argparse.ArgumentParser(description='Generate changelog')
    parser.add_argument(
        'between',
        nargs='?',
        default=None,
        help="Range, might be tag or a commit or a branch.",
    )
    parser.add_argument(
        '--no-other',
        dest="no_other",
        default=False,
        action='store_true',
        help="No `Other` section",
    )
    parser.add_argument(
        '--show-releases',
        dest="show_releases",
        default=False,
        action='store_true',
        help="Show releases",
    )
    parser.add_argument(
        '--output-file',
        dest="show_releases",
        default=False,
        action='store_true',
        help="Show releases",
    )
    args = parser.parse_args(sys.argv[1:])
    between = args.between if validate_between(args.between) else None
    include_other = not args.no_other
    show_releases = args.show_releases

    changelog = []

    if not show_releases:
        tree = prepare_changelog(
            between=between,
            unique_commit_messages=True
        )
        for branch_type, tickets in tree.items():
            # Skip adding orphaned commits if explicitly asked not to.
            if branch_type == BRANCH_TYPE_OTHER and not include_other:
                continue

            # Do not add branch type if no related branches found
            if tickets:
                changelog.append("\n**{}**".format(BRANCH_TYPES.get(branch_type)))

            # Add tickets
            for ticket_number, ticket_data in tickets.items():
                if branch_type != BRANCH_TYPE_OTHER:
                    changelog.append(
                        "\n*{} {}*\n".format(ticket_number, ticket_data['title'])
                    )
                else:
                    changelog.append('')

                for commit_hash, commit_data in ticket_data['commits'].items():
                    changelog.append(
                        "- {} [{}]".format(
                            commit_data['title'],
                            commit_data['author']
                        )
                    )
    else:
        releases_tree = prepare_releases_changelog(
            between=between,
            unique_commit_messages=True
        )
        for release, branches in releases_tree.items():
            release_label = UNRELEASED_LABEL \
                if release == UNRELEASED \
                else release

            changelog.append("\n### {}".format(release_label))
            for branch_type, tickets in branches.items():
                # Skip adding orphaned commits if explicitly asked not to.
                if branch_type == BRANCH_TYPE_OTHER and not include_other:
                    continue

                # Do not add branch type if no related branches found
                if tickets:
                    changelog.append(
                        "\n**{}**".format(BRANCH_TYPES.get(branch_type)))

                # Add tickets
                for ticket_number, ticket_data in tickets.items():
                    if branch_type != BRANCH_TYPE_OTHER:
                        changelog.append(
                            "\n*{} {}*\n".format(ticket_number,
                                                 ticket_data['title'])
                        )
                    else:
                        changelog.append('')

                    for commit_hash, commit_data in ticket_data['commits'].items():  # NOQA
                        changelog.append(
                            "- {} [{}]".format(
                                commit_data['title'],
                                commit_data['author']
                            )
                        )

    return '\n'.join(changelog)


def generate_changelog_cli() -> Type[None]:
    print(generate_changelog())


def create_config_file() -> bool:
    """Create config file.

    :return:
    """
    source_filename = project_dir('.matyan.ini')
    dest_filename = os.path.join(os.getcwd(), '.matyan.ini')
    try:
        copyfile(source_filename, dest_filename)
        return True
    except Exception as err:
        return False


def create_config_file_cli():
    return not create_config_file()
