"""
Routes and views for the flask application.
"""

import flask, ssl, datetime
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app

blueprint = Blueprint('useless_number_game', __name__, url_prefix='/uselessnumbergame')

cluster_username = 'admin'
cluster_password = 'admin'
cluster_dbname = 'useless-number-game'

app.config['MONGO_DBNAME'] = cluster_dbname
app.config['MONGO_URI'] = 'mongodb+srv://{}:{}@useless-number-game.idxzf.azure.mongodb.net/{}?retryWrites=false&w=majority'.format(
	cluster_username,
	cluster_password,
	cluster_dbname
)

players = PyMongo(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE).db.players


def get_player_status():
	return ('Welcome, ' + session['username'] + '!') if ('username' in session) else 'Oh, hi loser! Want to sign in?'


@blueprint.route('/')
def home():
	return render_template(
		'useless_number_game/home.html',
		title_ext='',
		player_status=get_player_status()
	)


@blueprint.route('/sign-up', methods=['GET', 'POST'])
@blueprint.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
	error = None
	is_username_inval = False
	inval_chars = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '[', '{', ']', '}', '|', ';',
				   ':', '"', ',', '<', '>', '/', '?', ' ']
	if request.method == 'POST':
		player = players.find_one({'username': request.form['username']})
		for n in inval_chars:
			is_username_inval = not is_username_inval and (n in request.form['username'])
		if player:
			error = "Someone's taken that username. Sorry."
		elif request.form['username'] == '':
			error = 'Actually enter a username, please…'
		elif request.form['password'] == '':
			error = 'Actually enter a password, please…'
		elif (request.form['passwordConfirm'] == '') or (request.form['passwordConfirm'] != request.form['password']):
			error = "Your passwords aren't the same. Try again…"
		elif is_username_inval:
			error = "You can't put special symbols or spaces in your username. Try again…"
		else:
			sign_up_date = datetime.datetime.now()
			players.insert(
				{
					'username': request.form['username'],
					'password': generate_password_hash(request.form['password']),
					'signUpDate': str(sign_up_date.strftime("%Y-%m-%d"))
				}
			)
			session['username'] = request.form['username']
			return redirect(url_for('.home'))
	return render_template(
		'useless_number_game/signup.html',
		title_ext='Sign Up – ',
		error=error)


@blueprint.route('/sign-in', methods=['GET', 'POST'])
@blueprint.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
	error = None
	if request.method == 'POST':
		player = players.find_one({'username': request.form['username']})
		if player:
			if check_password_hash(player['password'], request.form['password']):
				session['username'] = request.form['username']
				return redirect(url_for('.home'))
			else:
				error = "You've got the wrong username or password, mate."
		else:
			error = "You've got the wrong username, mate."
	return render_template(
		'useless_number_game/signin.html',
		title_ext='Sign In – ',
		error=error
	)


@blueprint.route('/sign-out')
@blueprint.route('/sign-out/')
def sign_out():
	session.clear()
	return render_template('useless_number_game/signout.html', title_ext='Sign Out – ')


@blueprint.route('/main')
@blueprint.route('/main/')
def main():
	return render_template(
		'useless_number_game/main.html',
		title_ext='',
		player_status=get_player_status()
	)


@blueprint.route('/player-error')
@blueprint.route('/player-error/')
def player_error():
	return render_template('useless_number_game/playererror.html', title_ext='')


@blueprint.route('/player/<username>')
@blueprint.route('/player/<username>/')
def player_profile(username):
	player = players.find_one({'username': username})
	if player:
		username = player['username']
		sign_up_date = player['signUpDate']
		return render_template(
			'useless_number_game/player_profile.html',
			title_ext='{} – '.format(username),
			username=username,
			player_status=get_player_status(),
			sign_up_date=sign_up_date
		)
	return redirect(url_for('.player_error'))


@blueprint.route('/player/<username>/change-password', methods=['GET', 'POST'])
@blueprint.route('/player/<username>/change-password/', methods=['GET', 'POST'])
def player_change_password(username):
	if session['username'] != username:
		return redirect(url_for('.home'))

	error = None

	if request.method == 'POST':
		player = players.find_one({'username': username})
		if request.form['oldPassword'] == "" or request.form['newPassword'] == "" or request.form['newPasswordConfirm'] == "":
			error = "Actually enter a password, please..."
		elif check_password_hash(player['password'], request.form['oldPassword']):
			if request.form['newPassword'] == request.form['newPasswordConfirm']:
				players.update(
					{'username': session['username']},
					{'$set': {'password': generate_password_hash(request.form['newPassword'])}}
				)
				return redirect(url_for('.player_change_password_confirm', username=username))
			else:
				error = "Your passwords aren't the same. Try again…"
		else:
			error = "You've got the wrong password, mate. Try again…"
	return render_template(
		'useless_number_game/player_changepassword.html',
		title_ext='Change {}\'s Password – '.format(username),
		error=error,
		username=username
	)


@blueprint.route('/player/<username>/change-password/confirm')
@blueprint.route('/player/<username>/change-password/confirm/')
def player_change_password_confirm(username):
	return render_template(
		'useless_number_game/player_changepassword_confirm.html',
		title_ext=''
	)


@blueprint.route('/player/<username>/delete', methods=['GET', 'POST'])
@blueprint.route('/player/<username>/delete/', methods=['GET', 'POST'])
def player_delete(username):
	if request.method == 'POST':
		if session['username'] == username:
			players.remove({'username': username})
			session.clear()
		return redirect(url_for('.home'))
	return render_template('useless_number_game/player_delete.html', title_ext='Delete a Player – ')


@blueprint.route('/about')
@blueprint.route('/about/')
def about():
	return render_template(
		'useless_number_game/about.html',
		title_ext='About – ',
		player_status=get_player_status()
	)
