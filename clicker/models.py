from werkzeug.security import generate_password_hash
from flask_login import AnonymousUserMixin

from .extensions import db
from clicker.utils.clasedict import TextPickleType

import sys
if sys.version_info[0] >= 3:
    unicode = str

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password_hash = db.Column(db.String(100))
    email_address = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean)
    sent_answers = db.Column(db.Boolean, default=False)
    json_field = db.Column(TextPickleType())
    options = db.Column(TextPickleType())
    results = db.Column(TextPickleType())
    score = db.Column(db.Integer)

    # A many-many relationship between User and Role tables.

    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, name, password, email_address, admin, sent_answers):
        self.name = name
        self.password = password
        self.email_address = email_address
        self.admin = admin
        self.sent_answers = sent_answers

        if admin:
            default = Role.query.filter_by(name="admin").one()
            self.roles.append(default)
        else:
            default = Role.query.filter_by(name="student").one()
            self.roles.append(default)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return unicode(self.id)

    @property
    def password(self):
        raise AttributeError('can not view password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Commands(db.Model):
    __bind_key__ = 'commands'
    id = db.Column(db.Integer, primary_key=True)
    enable_test = db.Column(db.Boolean)
    end_test = db.Column(db.Boolean)
    auth_see_sol = db.Column(db.Boolean)
    grade_already = db.Column(db.Boolean)
