import os
import logging
import socket

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'internet_available_only',
    'internet_available_or_is_travis_only',
    'is_internet_available',
    'is_travis',
    'log_info',
    'travis_only',
)

LOG_INFO = True
TRACK_TIME = False

LOGGER = logging.getLogger(__name__)


def log_info(func):
    """Log some useful info."""
    if not LOG_INFO:
        return func

    def inner(self, *args, **kwargs):
        """Inner."""
        if TRACK_TIME:
            import simple_timer
            timer = simple_timer.Timer()  # Start timer

        result = func(self, *args, **kwargs)

        if TRACK_TIME:
            timer.stop()  # Stop timer

        LOGGER.debug('\n\n%s', func.__name__)
        LOGGER.debug('============================')
        if func.__doc__:
            LOGGER.debug('""" %s """', func.__doc__.strip())
        LOGGER.debug('----------------------------')
        if result is not None:
            LOGGER.debug(result)
        if TRACK_TIME:
            LOGGER.debug('done in %s seconds', timer.duration)
        LOGGER.debug('\n++++++++++++++++++++++++++++')

        return result
    return inner


def is_internet_available(host: str = "8.8.8.8",
                          port: int = 53,
                          timeout: int = 3) -> bool:
    """Check if internet is available.

    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False


def internet_available_only(func):
    """Is internet available decorator.

    :param func:
    :return:
    """
    def inner(self, *args, **kwargs):
        """Inner."""
        if not is_internet_available():
            LOGGER.debug('\n\n%s', func.__name__)
            LOGGER.debug('============================')
            if func.__doc__:
                LOGGER.debug('""" %s """', func.__doc__.strip())
            LOGGER.debug('----------------------------')
            LOGGER.debug("Skipping because no Internet connection available.")
            LOGGER.debug('\n++++++++++++++++++++++++++++')
            return None

        result = func(self, *args, **kwargs)
        return result

    return inner


def is_travis() -> bool:
    """Is travis.

    :return:
    """
    return os.environ.get('TRAVIS') == 'true'


def travis_only(func):
    """Is on Travis CI decorator.

    :param func:
    :return:
    """
    def inner(self, *args, **kwargs):
        """Inner."""
        if not is_travis():
            LOGGER.debug('\n\n%s', func.__name__)
            LOGGER.debug('============================')
            if func.__doc__:
                LOGGER.debug('""" %s """', func.__doc__.strip())
            LOGGER.debug('----------------------------')
            LOGGER.debug("Skipping because this test is Travis CI only.")
            LOGGER.debug('\n++++++++++++++++++++++++++++')
            return None

        result = func(self, *args, **kwargs)
        return result

    return inner


def internet_available_or_is_travis_only(func):
    """Is internet available or is Travis only decorator.

    :param func:
    :return:
    """
    def inner(self, *args, **kwargs):
        """Inner."""
        if not is_internet_available() and not is_travis():
            LOGGER.debug('\n\n%s', func.__name__)
            LOGGER.debug('============================')
            if func.__doc__:
                LOGGER.debug('""" %s """', func.__doc__.strip())
            LOGGER.debug('----------------------------')
            LOGGER.debug(
                "Skipping because nor Internet connection available, "
                "neither the test is being executed on Travis CI."
            )
            LOGGER.debug('\n++++++++++++++++++++++++++++')
            return None

        result = func(self, *args, **kwargs)
        return result

    return inner