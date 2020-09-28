"""
Routes and views for the flask application.
"""

import flask
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from useless_number_game import app

blueprint = Blueprint('useless_meme_2', __name__, url_prefix='/uselessmeme2')


@blueprint.route('/')
def main():
	return render_template('useless_meme_2/main.html')
