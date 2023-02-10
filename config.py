import configparser
import os
import pathlib

from dotenv import load_dotenv

load_dotenv()
config = configparser.ConfigParser()
PACKAGE_FOLDER = pathlib.Path(__file__).parent
config.read(pathlib.Path(PACKAGE_FOLDER, 'config.ini'))

config_general = config['general']
PROXIES_FOLDER = pathlib.Path(PACKAGE_FOLDER, 'proxies')
if not PROXIES_FOLDER.exists():
    os.mkdir(PROXIES_FOLDER)

DEBUG = os.environ.get('DEBUG', False)
config_general['DEBUG'] = DEBUG
DEBUG = config_general.getboolean('DEBUG')

if not DEBUG:
    HOST = config_general.get('HOST', '0.0.0.0')
    PORT = config_general.getint('PORT', 8182)
else:
    HOST = config_general.get('TEST_HOST', 'localhost')
    PORT = config_general.getint('TEST_PORT', 8282)
