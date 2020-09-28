"""
Routes and views for the flask application.
"""

import flask
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from useless_number_game import app

blueprint = Blueprint('useless_meme_1', __name__, url_prefix='/uselessmeme1')


@blueprint.route('/')
def main():
	return render_template('useless_meme_1/main.html')
