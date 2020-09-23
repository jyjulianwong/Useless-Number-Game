"""
Routes and views for the flask application.
"""

import flask, ssl, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app
from useless_number_game.forms_ub import SignUpForm, SignInForm


@app.route('/ub')
@app.route('/ub/')
def ub_home():
	return render_template('ub/home.html')


@app.route('/ub/sign-up', methods=['GET', 'POST'])
@app.route('/ub/sign-up/', methods=['GET', 'POST'])
def ub_sign_up():
	form = SignUpForm()
	return render_template('ub/signup.html', form=form)


@app.route('/ub/sign-in', methods=['GET', 'POST'])
@app.route('/ub/sign-in/', methods=['GET', 'POST'])
def ub_sign_in():
	form = SignInForm()
	return render_template('ub/signin.html', form=form)
