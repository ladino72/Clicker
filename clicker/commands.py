import click
from flask.cli import with_appcontext
from .extensions import db
from .utils.remove_databases import RemoveDatabases
from clicker.models import Commands, Role, User


# In terminal: type "flask create_tables" without quotations to create db.sqlite3 and commands.db
# databases with corresponding tables. If both databases already exist, the command delete them and create
# the new ones.
# Databases created: db.sqlite3 and commands.db ---> Each database contains a table called User and Commands
# respectively


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    # First remove old databases, otherwise the db.create_all() doe not create new databases
    RemoveDatabases.remove_databases()
    # Next command create two databases (db.sqlite3 and commands.db) with corresponding tables
    db.create_all()
    # Commands table requires to have the next fields initialized

    commands = Commands(enable_test=False, end_test=False, grade_already=False, auth_see_sol=False)
    db.session.add(commands)
    db.session.commit()

    # The next 8 lines populate the Role table with two rows and the admin user
    # The content of the two rows is:
    # id    name    description
    #  1    admin    Test administer
    #  2    student  Regular student

    admin_role = Role(name="admin", description="Test Administer")
    student_role = Role(name="student", description="Regular user")
    db.session.add(admin_role)
    db.session.add(student_role)
    db.session.commit()
    # The admin user is: (ONLY one admin is admissible)
    admin_user = User(name="Luis Alejandro Ladino Gaspar", password="alfabeta",
                      email_address="ladino72@hotmail.com", admin=True, sent_answers=False)

    db.session.add(admin_user)
    db.session.commit()

# In terminal: type "flask create_command_table" without quotations to create commands.db database
# with corresponding table called Commands. If database already exist, the command delete it and creates
# a new one.
@click.command(name='create_commands_table')
@with_appcontext
def create_commands_table():
    # First remove old database, otherwise the db.create_all((bind="commands")) doe not create new databases
    RemoveDatabases.remove_command_database()
    # Next command create one database (commands.db) with corresponding table
    db.create_all(bind="commands")
    # Commands table requires to have the next fields initialized
    commands = Commands(enable_test=False, end_test=False, grade_already=False, auth_see_sol=False)
