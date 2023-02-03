import os
import pathlib

from dotenv import load_dotenv

load_dotenv()
PACKAGE_FOLDER = pathlib.Path(__file__).parent
PROXIES_FOLDER = pathlib.Path(PACKAGE_FOLDER, 'proxies')
if not PROXIES_FOLDER.exists():
    os.mkdir(PROXIES_FOLDER)

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', int('8181'))
