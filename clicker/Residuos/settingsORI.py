import os

from os import pardir
from os.path import abspath, dirname, join

PROJECT_PATH = abspath(join(dirname(__file__), pardir))
print("Project path, luis", PROJECT_PATH)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False