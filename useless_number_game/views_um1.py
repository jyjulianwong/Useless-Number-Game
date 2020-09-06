"""
Routes and views for the flask application.
"""

import flask
from flask import Flask, Config, render_template, url_for, request, session, redirect
from useless_number_game import app


@app.route('/um1')
@app.route('/um1/')
def um1_home():
	return render_template('um1/main.html')
