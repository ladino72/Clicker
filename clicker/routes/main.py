from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from clicker.extensions import db
from clicker.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

