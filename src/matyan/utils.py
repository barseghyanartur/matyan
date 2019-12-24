import argparse
import copy
import json
import os
import re
import logging
import sys
from shutil import copyfile
from typing import Union, Dict, AnyStr, Type, Any, List
from git import Git
from git.exc import GitCommandError

from .auto_correct import add_final_dot, capitalize, unslugify
from .constants import PRETTY_FORMAT, TICKET_NUMBER_OTHER
from .labels import (
    # get_all_branch_types,
    # get_branch_types,
    # get_ignore_commits_exact_words,
    get_ignore_commits_prefixes,
    # get_other_branch_type,
    # get_other_branch_type_key,
    # get_unreleased,
    # get_unreleased_key,
    # get_unreleased_key_label,
    get_settings,
    BRANCH_TYPE_OTHER,
    BRANCH_TYPES,
    IGNORE_COMMITS_EXACT_WORDS,
    UNRELEASED,
    UNRELEASED_LABEL,
)
from .fetchers import FetcherRegistry, BaseFetcher
from .renderers import (
    BaseRenderer,
    HistoricalMarkdownRenderer,
    MarkdownRenderer,
    RendererRegistry,
    RestructuredTextRenderer,
)
from .helpers import project_dir
from .patterns import (
    REGEX_PATTERN_BRANCH_NAME,
    REGEX_PATTERN_COMMIT,
    REGEX_PATTERN_COMMIT_LINE,
    REGEX_PATTERN_MERGED_BRANCH_NAME,
    REGEX_PATTERN_TAG,
)

LOGGER = logging.getLogger(__name__)
DEBUG = os.environ.get('DEBUG', False)

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'generate_changelog',
    'generate_changelog_cli',
    'get_branch_type',
    'get_logs',
    'get_repository',
    'json_changelog',
    'json_changelog_cli',
    'make_config_file',
    'make_config_file_cli',
    'prepare_changelog',
    'prepare_releases_changelog',
    'validate_between',
)


def get_repository(path: str = None) -> Git:
    if not (path and os.path.exists(path) and os.path.isdir(path)):
        path = os.getcwd()

    return Git(path)


def get_logs(between: str = None, path: str = None) -> Dict[str, Any]:
    """Get lots of logs.

    :param between:
    :param path:
    :return:
    """
    repository = get_repository(path)
    lower: Union[str, Type[None]] = None
    upper: Union[str, Type[None]] = None
    if between:
        try:
            rev_list_text = repository.rev_list(between)
            rev_list = rev_list_text.split('\n')
            if len(rev_list) >= 2:
                upper = rev_list[0]
                lower = rev_list[-1]
        except GitCommandError as err:
            pass

    # Merges log
    text_log_merges_args = []
    if lower and upper:
        # Note, that ~1 addition make sure the lower range is inclusive
        text_log_merges_args.append(
            "{}~1..{}".format(lower, upper)
        )
    text_log_merges_args.extend([
        "--pretty={}".format(PRETTY_FORMAT),
        "--source",
        # "--all",
        "--merges",
    ])
    text_log_merges = repository.log(*text_log_merges_args)
    log_merges = text_log_merges.split("\n")

    # Commits log
    text_log_args = []
    if lower and upper:
        # Note, that ~1 addition make sure the lower range is inclusive
        text_log_args.append(
            "{}~1..{}".format(lower, upper)
        )
    text_log_args.extend([
        "--pretty={}".format(PRETTY_FORMAT),
        "--source",
        # "--all"  # TODO: remove
    ])

    text_log = repository.log(*text_log_args)
    log = text_log.split("\n")

    # Tags log
    text_log_tags_args = []
    # if lower and upper:
    #     text_log_tags_args.append(
    #         "{}..{}".format(lower, upper)
    #     )
    text_log_tags_args.extend([
        "--tags",
        "--source",
        "--oneline"
    ])
    text_log_tags = repository.log(*text_log_tags_args)
    log_tags = text_log_tags.split("\n")
    commit_tags_list = [s.split(' ', 1)[0].split('\t', 1) for s in log_tags]
    commit_tags = dict([l for l in commit_tags_list if len(l) > 1])

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


# def generate_empty_tree() -> Dict[str, dict]:
#     """Generate empty tree.
#
#     Example:
#
#         {
#             'feature': {},
#             'bugfix': {},
#             'hotfix': {},
#             'deprecation': {},
#             'other': {
#                 TICKET_NUMBER_OTHER: {
#                     # 'title': '',
#                     'commits': {}
#                 }
#             },
#         }
#
#     :return:
#     """
#     empty_tree = {}
#     for key, value in BRANCH_TYPES.items():
#         empty_tree.update({key: {}})
#
#     empty_tree[BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER] = {'commits': {}}
#     return empty_tree


def prepare_changelog(
    between: str = None,
    unique_commit_messages: bool = False,
    headings_only: bool = False,
    unreleased_only: bool = False,
    fetch_title: bool = False,
    fetch_description: bool = False,
    path: str = None
) -> Dict[
        str, Dict[str, Dict[str, Union[str, Dict[str, Union[str, str]]]]]
]:
    """Prepare changelog.

    :param between:
    :param unique_commit_messages:
    :param headings_only:
    :param unreleased_only:
    :param fetch_title:
    :param fetch_description:
    :param path:
    :return:
    """
    logs = get_logs(between=between, path=path)
    settings = get_settings()
    tree = {}

    cur_branch = None
    cur_branch_type = None
    branch_types = {}

    fetcher = None

    if (
        (fetch_title or fetch_description)
        and settings.get('fetchDataFrom')
        and settings.get('fetchDataFrom') in FetcherRegistry.REGISTRY
    ):
        fetcher_cls = FetcherRegistry.REGISTRY[settings.get('fetchDataFrom')]
        fetcher = fetcher_cls()
    elif (
        settings.get('fetchDataFrom')
        and settings.get('fetchDataFrom') not in FetcherRegistry.REGISTRY
    ):
        LOGGER.debug(
            f"settings.get('fetchDataFrom') is not found in the registry!"
        )

    # First fill feature branches only
    for json_entry in logs['LOG_MERGES']:
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

            branch_title = None
            branch_description = None
            if fetcher is not None and ticket_number != TICKET_NUMBER_OTHER:
                fetcher_data = fetcher.fetch_issue_data(ticket_number)
                if fetch_title and 'title' in fetcher_data:
                    branch_title = fetcher_data['title']
                if fetch_description and 'description' in fetcher_data:
                    branch_description = fetcher_data['description']

            if not branch_title:
                branch_title = match.group('branch_title')

            # For normal tree
            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])

            if branch_type not in tree:
                tree[branch_type] = {}

            if ticket_number not in tree[branch_type]:
                tree[branch_type][ticket_number] = {
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'date': entry['datetime'],
                    'ticket_number': ticket_number,
                    'branch_type': branch_type,
                    'slug': branch_title,
                    'title': unslugify(branch_title),
                    'description': branch_description,
                    'commits': {},
                    'release': release,
                }
            branch_types.update({ticket_number: branch_type})

    if headings_only:
        return tree

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

            commit_message = unslugify(commit_message)
            commit_message = capitalize(commit_message)
            commit_message = add_final_dot(commit_message)

            # Ignore the following messages
            if commit_message.lower() in IGNORE_COMMITS_EXACT_WORDS:
                continue

            ignore_commits_prefixes = tuple(get_ignore_commits_prefixes())
            if commit_message.lower().startswith(ignore_commits_prefixes):
                continue

            commit_hash = commit_message \
                if unique_commit_messages \
                else entry['commit_hash']

            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])

            if cur_branch:

                if cur_branch_type not in tree:
                    tree[cur_branch_type] = {}

                if cur_branch not in tree[cur_branch_type]:
                    tree[cur_branch_type][cur_branch] = {}

                if 'commits' not in tree[cur_branch_type][cur_branch]:
                    tree[cur_branch_type][cur_branch]['commits'] = {}

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
                        if other_branch_type not in tree:
                            tree[other_branch_type] = {}

                        if ticket_number not in tree[other_branch_type]:
                            tree[other_branch_type][ticket_number] = {}

                        if 'commits' not in tree[other_branch_type][ticket_number]:
                            tree[other_branch_type][ticket_number]['commits'] = {}

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
                if BRANCH_TYPE_OTHER not in tree:
                    tree[BRANCH_TYPE_OTHER] = {}

                if TICKET_NUMBER_OTHER not in tree[BRANCH_TYPE_OTHER]:
                    tree[BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER] = {}

                if 'commits' not in tree[BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]:
                    tree[BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]['commits'] = {}

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
    unique_commit_messages: bool = False,
    headings_only: bool = False,
    unreleased_only: bool = False,
    fetch_title: bool = False,
    fetch_description: bool = False,
    path: str = None
) -> Dict[
        str, Dict[str, Dict[str, Union[str, Dict[str, Union[str, str]]]]]
]:
    """Prepare releases changelog.

    :param between:
    :param unique_commit_messages:
    :param headings_only:
    :param unreleased_only:
    :param fetch_title:
    :param fetch_description:
    :param path:
    :return:
    """
    logs = get_logs(between=between, path=path)
    settings = get_settings()
    releases_tree = {}

    cur_branch = None
    cur_branch_type = None
    branch_types = {}

    fetcher = None

    if (
        (fetch_title or fetch_description)
        and settings.get('fetchDataFrom')
        and settings.get('fetchDataFrom') in FetcherRegistry.REGISTRY
    ):
        fetcher_cls = FetcherRegistry.REGISTRY[settings.get('fetchDataFrom')]
        fetcher = fetcher_cls()
    elif (
        settings.get('fetchDataFrom')
        and settings.get('fetchDataFrom') not in FetcherRegistry.REGISTRY
    ):
        LOGGER.debug(
            f"settings.get('fetchDataFrom') is not found in the registry!"
        )

    # First fill feature branches only
    for json_entry in logs['LOG_MERGES']:
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

            branch_title = None
            branch_description = None

            if fetcher is not None and ticket_number != TICKET_NUMBER_OTHER:
                fetcher_data = fetcher.fetch_issue_data(ticket_number)
                if fetch_title and 'title' in fetcher_data:
                    branch_title = fetcher_data['title']
                if fetch_description and 'description' in fetcher_data:
                    branch_description = fetcher_data['description']

            if not branch_title:
                branch_title = match.group('branch_title')

            # For normal tree
            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])
            if not release:
                release = UNRELEASED

            if release not in releases_tree:
                releases_tree[release] = {}

            if branch_type not in releases_tree[release]:
                releases_tree[release][branch_type] = {}

            if ticket_number not in releases_tree[release][branch_type]:
                releases_tree[release][branch_type][ticket_number] = {
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'date': entry['datetime'],
                    'ticket_number': ticket_number,
                    'branch_type': branch_type,
                    'slug': branch_title,
                    'title': unslugify(branch_title),
                    'description': branch_description,
                    'commits': {},
                    'release': release,
                }
            branch_types.update({ticket_number: branch_type})
    
    if headings_only:
        if unreleased_only:
            return {UNRELEASED: releases_tree.get(UNRELEASED, {})}
        return releases_tree

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

            commit_message = unslugify(commit_message)
            commit_message = capitalize(commit_message)
            commit_message = add_final_dot(commit_message)

            # Ignore the following messages
            if commit_message.lower() in IGNORE_COMMITS_EXACT_WORDS:
                continue

            ignore_commits_prefixes = tuple(get_ignore_commits_prefixes())
            if commit_message.lower().startswith(ignore_commits_prefixes):
                continue

            commit_hash = commit_message \
                if unique_commit_messages \
                else entry['commit_hash']

            release = logs['COMMIT_TAGS'].get(entry['commit_abbr'])
            if not release:
                release = UNRELEASED

            if cur_branch:

                if release not in releases_tree:
                    releases_tree[release] = {}

                if cur_branch_type not in releases_tree[release]:
                    releases_tree[release][cur_branch_type] = {}

                if cur_branch not in releases_tree[release][cur_branch_type]:
                    releases_tree[release][cur_branch_type][cur_branch] = {}

                if 'commits' not in releases_tree[release][cur_branch_type][cur_branch]:
                    releases_tree[release][cur_branch_type][cur_branch]['commits'] = {}

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
                        if release not in releases_tree:
                            releases_tree[release] = {}

                        if other_branch_type not in releases_tree[release]:
                            releases_tree[release][other_branch_type] = {}

                        if ticket_number not in releases_tree[release][other_branch_type]:
                            releases_tree[release][other_branch_type][ticket_number] = {}

                        if 'commits' not in releases_tree[release][other_branch_type][ticket_number]:
                            releases_tree[release][other_branch_type][ticket_number]['commits'] = {}

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
                if release not in releases_tree:
                    releases_tree[release] = {}

                if BRANCH_TYPE_OTHER not in releases_tree[release]:
                    releases_tree[release][BRANCH_TYPE_OTHER] = {}

                if TICKET_NUMBER_OTHER not in releases_tree[release][BRANCH_TYPE_OTHER]:
                    releases_tree[release][BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER] = {}

                if 'commits' not in releases_tree[release][BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]:
                    releases_tree[release][BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]['commits'] = {}

                releases_tree[release][BRANCH_TYPE_OTHER][TICKET_NUMBER_OTHER]['commits'][commit_hash] = {  # NOQA
                    'commit_hash': entry['commit_hash'],
                    'commit_abbr': entry['commit_abbr'],
                    'author': entry['author'],
                    'date': entry['datetime'],
                    'ticket_number': ticket_number,
                    'title': commit_message,
                }

    if unreleased_only:
        return {UNRELEASED: releases_tree.get(UNRELEASED, {})}

    return releases_tree


def validate_between(between: str = None) -> bool:
    """Validate between.

    :param between:
    :return:
    """
    if between:
        pass  # TODO
    return True


# def get_latest_release(path: str = None) -> str:
#     """Get latest release.
#
#     Command:
#
#         git describe --match '*.*' --abbr=0
#
#     :return:
#     """
#     repository = get_repository(path)
#     return repository.describe('--match', '*.*', '--abbr=0')


def get_latest_releases(limit: int = 2, path: str = None) -> list:
    """Get latest <limit> releases.

    Command:

        git tag --sort=-version:refname -l '*.*' | head -n <limit>

    :return:
    """
    repository = get_repository(path)
    return repository.tag(
        '--sort=-version:refname', '--list', '*.*'
    ).split('\n')[:limit]


def json_changelog(between: str = None,
                   include_other: bool = True,
                   show_releases: bool = False,
                   latest_release: bool = False,
                   headings_only: bool = False,
                   fetch_title: bool = False,
                   fetch_description: bool = False,
                   path: str = None):
    if latest_release:
        latest_two_releases = get_latest_releases(limit=2, path=path)
        latest_two_releases = latest_two_releases[::-1]
        if len(latest_two_releases):
            between = '..'.join(latest_two_releases)

    if not show_releases:
        tree = prepare_changelog(
            between=between,
            unique_commit_messages=True,
            headings_only=headings_only,
            path=path
        )
        return tree
    else:
        releases_tree = prepare_releases_changelog(
            between=between,
            unique_commit_messages=True,
            headings_only=headings_only,
            path=path
        )
        return releases_tree


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
    parser.add_argument(
        '--latest-release',
        dest="latest_release",
        default=False,
        action='store_true',
        help="Generate changelog for the latest release only",
    )
    parser.add_argument(
        '--headings-only',
        dest="headings_only",
        default=False,
        action='store_true',
        help="Generate headings only (no commit messages, only branch titles)",
    )
    parser.add_argument(
        '--fetch-title',
        dest="fetch_title",
        default=False,
        action='store_true',
        help="Fetch title",
    )
    parser.add_argument(
        '--fetch-description',
        dest="fetch_description",
        default=False,
        action='store_true',
        help="Fetch description",
    )

    args = parser.parse_args(sys.argv[1:])
    between = args.between if validate_between(args.between) else None
    include_other = not args.no_other
    show_releases = args.show_releases
    latest_release = args.latest_release
    headings_only = args.headings_only
    fetch_title = args.fetch_title
    fetch_description = args.fetch_description

    print(
        json_changelog(
            between=between,
            include_other=include_other,
            show_releases=show_releases,
            latest_release=latest_release,
            headings_only=headings_only,
            fetch_title=fetch_title,
            fetch_description=fetch_description
        )
    )


def generate_changelog(between: str = None,
                       include_other: bool = True,
                       show_releases: bool = False,
                       latest_release: bool = False,
                       headings_only: bool = False,
                       unreleased_only: bool = False,
                       fetch_title: bool = False,
                       fetch_description: bool = False,
                       renderer_cls: Union[
                           Type[HistoricalMarkdownRenderer],
                           Type[MarkdownRenderer],
                           Type[RestructuredTextRenderer]
                       ] = MarkdownRenderer,
                       path: str = None) -> str:
    """Generate changelog (markdown format)."""

    # if show_latest_release and between:
    #     raise Exception(
    #         "--show-latest-release can't be used in combination with specific"
    #         "tags/commits/branches range."
    #     )
    if latest_release:
        latest_two_releases = get_latest_releases(limit=2, path=path)
        latest_two_releases = latest_two_releases[::-1]
        if len(latest_two_releases):
            between = '..'.join(latest_two_releases)

    renderer = renderer_cls()

    if not show_releases:
        tree = prepare_changelog(
            between=between,
            unique_commit_messages=True,
            headings_only=headings_only,
            unreleased_only=unreleased_only and show_releases,
            fetch_title=fetch_title,
            fetch_description=fetch_description,
            path=path
        )

        return renderer.render_changelog(
            tree=tree,
            include_other=include_other,
            headings_only=headings_only,
            fetch_description=fetch_description
        )
    else:
        releases_tree = prepare_releases_changelog(
            between=between,
            unique_commit_messages=True,
            headings_only=headings_only,
            unreleased_only=unreleased_only and show_releases,
            fetch_title=fetch_title,
            fetch_description=fetch_description,
            path=path
        )

        return renderer.render_releases_changelog(
            releases_tree=releases_tree,
            include_other=include_other,
            headings_only=headings_only,
            fetch_description=fetch_description
        )


def generate_changelog_cli() -> Type[None]:
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
        '--latest-release',
        dest="latest_release",
        default=False,
        action='store_true',
        help="Generate changelog for the latest release only",
    )
    parser.add_argument(
        '--headings-only',
        dest="headings_only",
        default=False,
        action='store_true',
        help="Generate headings only (no commit messages, only branch titles)",
    )
    parser.add_argument(
        '--unreleased-only',
        dest="unreleased_only",
        default=False,
        action='store_true',
        help="Show unreleased only. Works in combination with --show-releases",
    )
    parser.add_argument(
        '--fetch-title',
        dest="fetch_title",
        default=False,
        action='store_true',
        help="Fetch title",
    )
    parser.add_argument(
        '--fetch-description',
        dest="fetch_description",
        default=False,
        action='store_true',
        help="Fetch description",
    )
    parser.add_argument(
        '--renderer',
        dest="renderer",
        default=MarkdownRenderer.uid,
        action='store',
        help="Renderer",
        choices=list(RendererRegistry.REGISTRY.keys())
    )
    args = parser.parse_args(sys.argv[1:])
    between = args.between if validate_between(args.between) else None
    include_other = not args.no_other
    show_releases = args.show_releases
    latest_release = args.latest_release
    headings_only = args.headings_only
    unreleased_only = args.unreleased_only
    fetch_title = args.fetch_title
    fetch_description = args.fetch_description
    renderer_uid = args.renderer

    renderer_cls = RendererRegistry.get(renderer_uid, MarkdownRenderer)

    print(
        generate_changelog(
            between=between,
            include_other=include_other,
            show_releases=show_releases,
            latest_release=latest_release,
            headings_only=headings_only,
            unreleased_only=unreleased_only,
            fetch_title=fetch_title,
            fetch_description=fetch_description,
            renderer_cls=renderer_cls
        )
    )


def make_config_file() -> bool:
    """Make (or overwrite) config file.

    :return:
    """
    source_filename = project_dir('.matyan.ini')
    dest_filename = os.path.join(os.getcwd(), '.matyan.ini')
    try:
        copyfile(source_filename, dest_filename)
        return True
    except Exception as err:
        return False


def make_config_file_cli():
    return not make_config_file()
