"""
Routes and views for the flask application.
"""

import flask, ssl, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from useless_number_game import app

cluster_username = 'admin'
cluster_password = 'admin'
cluster_dbname = 'anjuls-sleep-indicator'

app.config['MONGO_DBNAME'] = cluster_dbname
app.config[
	'MONGO_URI'] = 'mongodb+srv://{}:{}@useless-number-game.idxzf.azure.mongodb.net/{}?retryWrites=false&w=majority'.format(
	cluster_username,
	cluster_password,
	cluster_dbname
)

states = PyMongo(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE).db.states


@app.route('/asi')
@app.route('/asi/')
def asi_home():
	state_angel = states.find_one({'name': 'Angel'})
	state_julian = states.find_one({'name': 'Julian'})
	return render_template('asi/home.html', state_angel=state_angel, state_julian=state_julian)


@app.route('/asi/update/<name>')
@app.route('/asi/update/<name>/')
def asi_update(name):
	state = states.find_one({'name': name})
	if state['isSleeping'] == 'true':
		is_sleeping = 'false'
	else:
		is_sleeping = 'true'

	states.update(
		{'name': name},
		{'$set': {
			'isSleeping': is_sleeping,
			'updateTime': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		}}
	)
	return redirect(url_for('asi_home'))
