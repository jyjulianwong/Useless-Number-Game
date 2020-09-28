"""
Routes and views for the flask application.
"""

import flask, datetime
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from useless_number_game import app

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def home():
	return render_template('home.html')


@blueprint.route('/coming-soon')
@blueprint.route('/coming-soon/')
def coming_soon():
	return render_template('comingsoon.html')
