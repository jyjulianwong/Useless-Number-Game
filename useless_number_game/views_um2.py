"""
Routes and views for the flask application.
"""

import flask
from flask import Flask, Config, render_template, url_for, request, session, redirect
from useless_number_game import app


@app.route('/um2')
@app.route('/um2/')
def um2_home():
	return render_template('um2/main.html')
