
import os
from os import pardir
from os.path import abspath, dirname, join

PROJECT_PATH = abspath(join(dirname(__file__), pardir))


class RemoveDatabases:
    @staticmethod
    def remove_databases():
        if os.path.isfile(join(PROJECT_PATH, 'clicker/databases/commands.db')):
            os.remove(join(PROJECT_PATH, 'clicker/databases/commands.db'))

        if os.path.isfile(join(PROJECT_PATH, 'clicker/databases/db.sqlite3')):
            os.remove(join(PROJECT_PATH, "clicker/databases/db.sqlite3"))

    @staticmethod
    def remove_command_database():
        if os.path.isfile(join(PROJECT_PATH, 'clicker/databases/commands.db')):
            os.remove(join(PROJECT_PATH, 'clicker/databases/commands.db'))