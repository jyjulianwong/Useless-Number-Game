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
	state_angel = states.find_one({'name': 'Angel'})
	in_united_kingdom_angel = state_angel['inUnitedKingdom'] == 'true'
	state_julian = states.find_one({'name': 'Julian'})
	in_united_kingdom_julian = state_julian['inUnitedKingdom'] == 'true'

	if request.method == 'POST':
		if 'Koala' in request.form['action']:
			name = 'Angel'
		else:
			name = 'Julian'

		state = states.find_one({'name': name})
		if state['isSleeping'] == 'true':
			is_sleeping = 'false'
		else:
			is_sleeping = 'true'

		if request.form.get('inUnitedKingdom{}'.format(name)):
			in_united_kingdom = "true"
			update_tz = pytz.timezone('Europe/London')
		else:
			in_united_kingdom = "false"
			update_tz = pytz.timezone('Asia/Hong_Kong')
		update_time = datetime.now().astimezone(update_tz)
		update_time_string = str(update_time.strftime("%d %b %H:%M"))

		states.update(
			{'name': name},
			{'$set': {
				'isSleeping': is_sleeping,
				'inUnitedKingdom': in_united_kingdom,
				'updateTime': update_time_string
			}}
		)
		return redirect(url_for('.home'))
	return render_template(
		'anjuls_sleep_indicator/home.html',
		state_angel=state_angel,
		in_united_kingdom_angel=in_united_kingdom_angel,
		state_julian=state_julian,
		in_united_kingdom_julian=in_united_kingdom_julian
	)
