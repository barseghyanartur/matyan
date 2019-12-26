import json
import os
from logging import config, getLogger

from .config import CONFIG

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'LOGGER',
)

ENABLE_LOGGING = False

try:
    ENABLE_LOGGING = CONFIG['Settings']['debug'] == 'true'
except (KeyError, TypeError):
    pass

if ENABLE_LOGGING:
    DEFAULT_LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['file'],
        },
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} '
                          '{message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'WARNING',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(os.getcwd(), "matyan.log"),
                'maxBytes': 1048576,
                'backupCount': 99,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'matyan': {
                'handlers': ['file'],
                'propagate': True,
            },
        },
    }

    LOGGING_CONFIG_STR = os.environ.get('MATYAN_LOGGING_CONFIG', "")

    if LOGGING_CONFIG_STR:
        try:
            config_dict = json.loads(LOGGING_CONFIG_STR)
        except Exception:
            config_dict = DEFAULT_LOGGING_CONFIG
    else:
        config_dict = DEFAULT_LOGGING_CONFIG

    config.dictConfig(config_dict)

LOGGER = getLogger(__name__)

if not ENABLE_LOGGING:
    LOGGER.disabled = True
