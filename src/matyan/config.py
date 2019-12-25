import configparser
import os
from pathlib import Path

from .helpers import project_dir

__author__ = 'Artur Barseghyan'
__copyright__ = '2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'CONFIG',
    'CONFIG_INI_PATH',
)
CONFIG = configparser.ConfigParser()
HOME_PATH = Path.home()
CONFIG_INI_PATH = HOME_PATH.joinpath('.matyan.ini')
if CONFIG_INI_PATH.exists() and CONFIG_INI_PATH.is_file():
    CONFIG.read(str(CONFIG_INI_PATH))

LOCAL_CONFIG = configparser.ConfigParser()

LOCAL_CONFIG_INI_PATH = os.path.join(os.getcwd(), '.matyan.ini')

if not os.path.exists(LOCAL_CONFIG_INI_PATH):
    LOCAL_CONFIG_INI_PATH = project_dir('.matyan.ini')

LOCAL_CONFIG.read(LOCAL_CONFIG_INI_PATH)

CONFIG.update(LOCAL_CONFIG)
