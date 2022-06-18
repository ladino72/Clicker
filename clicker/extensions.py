from flask_principal import Principal, Permission, RoleNeed
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


principals = Principal()

admin_permission = Permission(RoleNeed('admin'))
student_permission = Permission(RoleNeed('student'))


login_manager = LoginManager()
db = SQLAlchemy()

