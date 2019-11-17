import configparser
import os

from .helpers import project_dir

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = (
    'CONFIG',
    'CONFIG_INI_PATH',
)


CONFIG = configparser.ConfigParser()

CONFIG_INI_PATH = os.path.join(os.getcwd(), '.matyan.ini')

if not os.path.exists(CONFIG_INI_PATH):
    CONFIG_INI_PATH = project_dir('.matyan.ini')

CONFIG.read(CONFIG_INI_PATH)
