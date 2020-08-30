"""
Routes and views for the flask application.
"""

import flask, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from useless_number_game import app


@app.route('/')
def home():
	return render_template('home.html')
