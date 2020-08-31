"""
Routes and views for the flask application.
"""

import flask, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app

app.config['MONGO_DBNAME'] = 'uselessnumbergame_players'
app.config['MONGO_URI'] = 'mongodb://uselessNumberGame:0000@ds012198.mlab.com:12198/uselessnumbergame_players?retryWrites=false'
players = PyMongo(app).db.users


def get_player_status():
	return ('Welcome, ' + session['username'] + '!') if ('username' in session) else 'Oh, hi loser! Want to sign in?'


@app.route('/ung')
@app.route('/ung/')
def ung_home():
	return render_template('ung/home.html', player_status=get_player_status())


@app.route('/ung/sign-up', methods=['GET', 'POST'])
@app.route('/ung/sign-up/', methods=['GET', 'POST'])
def ung_sign_up():
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
			return redirect(url_for('ung_home'))
	return render_template('ung/signup.html', error=error)


@app.route('/ung/sign-in', methods=['GET', 'POST'])
@app.route('/ung/sign-in/', methods=['GET', 'POST'])
def ung_sign_in():
	error = None
	if request.method == 'POST':
		player = players.find_one({'username': request.form['username']})
		if player:
			if check_password_hash(player['password'], request.form['password']):
				session['username'] = request.form['username']
				return redirect(url_for('ung_home'))
			else:
				error = "You've got the wrong username or password, mate."
		else:
			error = "You've got the wrong username, mate."
	return render_template('ung/signin.html', error=error)


@app.route('/ung/sign-out')
@app.route('/ung/sign-out/')
def ung_sign_out():
	session.clear()
	return render_template('ung/signout.html')


@app.route('/ung/main')
@app.route('/ung/main/')
def ung_main():
	return render_template('ung/main.html', player_status=get_player_status())


@app.route('/ung/player-error')
@app.route('/ung/player-error/')
def ung_player_error():
	return render_template('ung/playererror.html')


@app.route('/ung/player/<username>')
@app.route('/ung/player/<username>/')
def ung_player_profile(username):
	player = players.find_one({'username': username})
	if player:
		username = player['username']
		sign_up_date = player['signUpDate']
		return render_template(
			'ung/player_profile.html',
			username=username,
			player_status=get_player_status(),
			sign_up_date=sign_up_date
		)
	return redirect(url_for('ung_player_error'))


@app.route('/ung/player/<username>/change-password', methods=['GET', 'POST'])
@app.route('/ung/player/<username>/change-password/', methods=['GET', 'POST'])
def ung_player_change_password(username):
	if session['username'] != username:
		return redirect(url_for('ung_home'))

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
				return redirect(url_for('ung_player_change_password_confirm', username=username))
			else:
				error = "Your passwords aren't the same. Try again…"
		else:
			error = "You've got the wrong password, mate. Try again…"
	return render_template('ung/player_changepassword.html', error=error, username=username)


@app.route('/ung/player/<username>/change-password/confirm')
@app.route('/ung/player/<username>/change-password/confirm/')
def ung_player_change_password_confirm(username):
	return render_template('ung/player_changepassword_confirm.html')


@app.route('/ung/player/<username>/delete', methods=['GET', 'POST'])
@app.route('/ung/player/<username>/delete/', methods=['GET', 'POST'])
def ung_player_delete(username):
	if request.method == 'POST':
		if session['username'] == username:
			players.remove({'username': username})
			session.clear()
		return redirect(url_for('ung_home'))
	return render_template('ung/player_delete.html')


@app.route('/ung/about')
@app.route('/ung/about/')
def ung_about():
	return render_template('ung/about.html', player_status=get_player_status())
