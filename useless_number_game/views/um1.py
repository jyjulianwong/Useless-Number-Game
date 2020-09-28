"""
Routes and views for the flask application.
"""

import flask
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from useless_number_game import app

blueprint = Blueprint('um1', __name__, url_prefix='/um1')


@blueprint.route('/')
def main():
	return render_template('um1/main.html')
