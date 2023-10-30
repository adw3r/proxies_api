import configparser
import os
import pathlib

from dotenv import load_dotenv

load_dotenv()
config = configparser.ConfigParser()
PACKAGE_FOLDER = pathlib.Path(__file__).parent.parent
config.read(pathlib.Path(PACKAGE_FOLDER, 'config.ini'))

config_general = config['general']
PROXIES_FOLDER = pathlib.Path(PACKAGE_FOLDER, 'proxies')
if not PROXIES_FOLDER.exists():
    os.mkdir(PROXIES_FOLDER)

DEBUG = config_general.getboolean('DEBUG', True)

if not DEBUG:
    HOST = config_general.get('HOST', '0.0.0.0')
    PORT = config_general.getint('PORT', 8182)
else:
    HOST = config_general.get('TEST_HOST', '0.0.0.0')
    PORT = config_general.getint('TEST_PORT', 8282)

FACTORIES_JSON = pathlib.Path(PACKAGE_FOLDER, 'factories.json')
