"""
Routes and views for the flask application.
"""

import flask, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from useless_number_game import app


@app.route('/uobt')
@app.route('/uobt/')
def uobt_home():
	return render_template('uobt/home.html')
