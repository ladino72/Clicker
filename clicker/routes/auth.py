import json
import os.path
import os

from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from clicker.extensions import db
from clicker.models import User
from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed
)

from .admin_test import set_grade_already_status, set_auth_see_sol_status, set_enable_test_status, set_end_test_status
from clicker.extensions import admin_permission, student_permission
from .admin_test import set_commands_table

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        print("request.remote_addr:", request.remote_addr)
        email_address = request.form['email']
        password = request.form['password']
        remember = request.form.getlist("rememberme")

        # Check that remember list is empty
        if not remember:
            remember_me = False
        else:
            remember_me = True

        user = User.query.filter_by(email_address=email_address).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Either email/password miss match or you are not registered")
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember_me)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id))

        #g.user = current_user
        #session['user'] = current_user.name
        # https://github.com/PacktPublishing/Flask-Building-Python-Web-Services/tree/master/Module%203
        if admin_permission.can():
        #if current_user.admin:

            return redirect(url_for('admin_test.command_console'))
        elif student_permission.can():
            return redirect(url_for('auth.show_test'))
        else:
            return "<h1>" + "Danger: An intruder has breached the system security"+"</h1>"

    return render_template('login.html', title="Login")


@auth.route('/show_test', methods=['GET', 'POST'])
def show_test():
    return render_template("index.html", title="User")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        flastname = request.form["first_lastname"]
        slastname = request.form["second_lastname"]
        email_address = request.form['email']
        password1 = request.form['password']
        password2 = request.form['repeat_password']

        full_name = name + " " + flastname + " " + slastname

        try:

            user = User(
                name=full_name,
                password=password1,
                email_address=email_address,
                admin=False,
                sent_answers=False
                )

            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect(url_for('auth.login'))

        except IntegrityError:
            flash('ERROR! Email: {} already exists!'.format(email_address), 'error')
            db.session.rollback()


    return render_template('register.html', title="Sign Up")

@auth.route('/logout')
@login_required
def logout():
    if admin_permission.can():
        set_commands_table()

    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    return redirect(url_for('auth.login'))

@auth.route('/admin')
def admin():
    for key in session:
        print(key, '->', session[key])
    return "<h1> hello</h1>"
