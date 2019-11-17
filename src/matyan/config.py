import configparser
import os

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'CONFIG',
    'CONFIG_INI_PATH',
    'project_dir',
)


CONFIG = configparser.ConfigParser()


def project_dir(base):
    """Absolute path to a file from current directory."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), base).replace('\\', '/')
    )


CONFIG_INI_PATH = os.path.join(os.getcwd(), '.matyan.ini')

if not os.path.exists(CONFIG_INI_PATH):
    CONFIG_INI_PATH = project_dir('.matyan.ini')

CONFIG.read(CONFIG_INI_PATH)
