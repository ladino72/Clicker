import os

from os import pardir
from os.path import abspath, dirname, join

PROJECT_PATH = abspath(join(dirname(__file__), pardir))
print("Project path, luis", PROJECT_PATH)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(PROJECT_PATH, 'clicker/databases/db.sqlite3')
SQLALCHEMY_BINDS = {'commands': 'sqlite:///' + join(PROJECT_PATH, 'clicker/databases/commands.db')}
SECRET_KEY = 'rebumd8xvrywgkvufsnrtvji7fyjeu4tue'
SQLALCHEMY_TRACK_MODIFICATIONS = False