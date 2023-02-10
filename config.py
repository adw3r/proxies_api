import configparser
import os
import pathlib

PACKAGE_FOLDER = pathlib.Path(__file__).parent
PROXIES_FOLDER = pathlib.Path(PACKAGE_FOLDER, 'proxies')
if not PROXIES_FOLDER.exists():
    os.mkdir(PROXIES_FOLDER)

config = configparser.ConfigParser()
config.read(pathlib.Path(PACKAGE_FOLDER, 'config.ini'))

HOST = config['general'].get('HOST', 'localhost')
PORT = config['general'].getint('PORT', 8182)
