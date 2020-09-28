"""
Routes and views for the flask application.
"""

from flask import Blueprint, render_template
from useless_number_game import app
from useless_number_game.views.forms_ub import SignUpForm, SignInForm

blueprint = Blueprint('ub', __name__, '/ub')


@blueprint.route('/')
def home():
	return render_template('ub/home.html')


@blueprint.route('/sign-up', methods=['GET', 'POST'])
@blueprint.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
	form = SignUpForm()
	return render_template('ub/signup.html', form=form)


@blueprint.route('/sign-in', methods=['GET', 'POST'])
@blueprint.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
	form = SignInForm()
	return render_template('ub/signin.html', form=form)
