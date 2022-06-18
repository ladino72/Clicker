import json

import sqlalchemy
from sqlalchemy import TypeDecorator

SIZE = 256

# https://stackoverflow.com/questions/1378325/python-dicts-in-sqlalchemy

class TextPickleType(TypeDecorator):
    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
