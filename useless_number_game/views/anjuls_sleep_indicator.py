"""
Routes and views for the flask application.
"""

import flask, ssl, pytz
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from datetime import datetime, timezone
from useless_number_game import app

blueprint = Blueprint('anjuls_sleep_indicator', __name__, url_prefix='/anjul')

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


@blueprint.route('/', methods=['GET', 'POST'])
def home():
	state_a = states.find_one({'name': 'Angel'})
	is_sleeping_a = state_a['isSleeping'] == 'true'
	in_united_kingdom_a = state_a['inUnitedKingdom'] == 'true'

	state_j = states.find_one({'name': 'Julian'})
	is_sleeping_j = state_j['isSleeping'] == 'true'
	in_united_kingdom_j = state_j['inUnitedKingdom'] == 'true'

	if request.method == 'POST':
		# TODO: Clear wake and sleep times if a change in region is detected
		name = 'Angel' if 'Koala' in request.form['action'] else 'Julian'
		state = states.find_one({'name': name})
		is_sleeping = 'false' if state['isSleeping'] == 'true' else 'true'
		in_united_kingdom = 'true' if request.form.get('inUnitedKingdom{}'.format(name)) else 'false'
		update_time_phase = 'updateWakeTime' if state['isSleeping'] == 'true' else 'updateSleepTime'
		update_tz = pytz.timezone('Europe/London') if request.form.get('inUnitedKingdom{}'.format(name)) else pytz.timezone('Asia/Hong_Kong')
		update_time = datetime.now().astimezone(update_tz)
		update_time_string = str(update_time.strftime("%d %b %H:%M"))

		states.update(
			{'name': name},
			{'$set': {
				'isSleeping': is_sleeping,
				'inUnitedKingdom': in_united_kingdom,
				update_time_phase: update_time_string
			}}
		)

		return redirect(url_for('.home'))

	return render_template(
		'anjuls_sleep_indicator/home.html',
		state_a=state_a,
		is_sleeping_a=is_sleeping_a,
		in_united_kingdom_a=in_united_kingdom_a,
		state_j=state_j,
		is_sleeping_j=is_sleeping_j,
		in_united_kingdom_j=in_united_kingdom_j
	)
