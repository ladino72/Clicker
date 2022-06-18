from flask import Flask, flash, redirect, url_for
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from .commands import create_tables
from .commands import create_commands_table

from .extensions import db, login_manager, principals
from .models import User
from .routes.auth import auth
from .routes.main import main
from .routes.admin_test import admin_test, set_commands_table
from .utils.filters import title, caps, half_name


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        flash('You must be logged in to view that page.')
        return redirect(url_for('auth.login'))

    principals.init_app(app)
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin_test)

    app.cli.add_command(create_tables)
    app.cli.add_command(create_commands_table)

    app.jinja_env.filters['upper'] = title
    app.jinja_env.filters['cap'] = caps
    app.jinja_env.filters['names'] = half_name

    @app.before_first_request
    def settings():
        set_commands_table()

    return app
