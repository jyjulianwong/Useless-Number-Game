"""
Routes and views for the flask application.
"""

import flask, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app

app.config['MONGO_DBNAME'] = 'uselessnumbergame_players'
app.config['MONGO_URI'] = 'mongodb://uselessNumberGame:0000@ds012198.mlab.com:12198/uselessnumbergame_players'
useless_number_game_players = PyMongo(app)
players = useless_number_game_players.db.users


def get_player_status():
	if 'username' in session:
		player_status = 'Welcome, ' + session['username'] + '!'
	elif 'username' not in session:
		player_status = 'Oh, hi loser! Want to sign in?'
	return player_status


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', player_status=get_player_status())


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
	error = None
	is_username_inval = False
	inval_chars = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '[', '{', ']', '}', '|', ';',
				   ':', '"', ',', '<', '>', '/', '?', ' ']
	if request.method == 'POST':
		player = players.find_one({'username': request.form['username']})
		for n in inval_chars:
			if not is_username_inval:
				if n in request.form['username']:
					is_username_inval = True
		if player is not None:
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
				{'username': request.form['username'], 'password': generate_password_hash(request.form['password']),
				 'signUpDate': str(sign_up_date.strftime("%Y-%m-%d"))})
			session['username'] = request.form['username']
			return redirect(url_for('home'))
	return render_template('signup.html', error=error)


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
	error = None
	if request.method == 'POST':
		player = players.find_one({'username': request.form['username']})
		if player:
			if check_password_hash(player['password'], request.form['password']):
				session['username'] = request.form['username']
				return redirect(url_for('home'))
			else:
				error = "You've got the wrong username or password, mate."
		else:
			error = "You've got the wrong username, mate."
	return render_template('signin.html', error=error)


@app.route('/signout')
def sign_out():
	session.clear()
	return render_template('signout.html')


@app.route('/main')
def main():
	return render_template('main.html', player_status=get_player_status())


@app.route('/profile')
def profile():
	if 'username' in session:
		sign_up_date = players.distinct('signUpDate', {'username': session['username']})[0]
	elif 'username' not in session:
		sign_up_date = None
	return render_template('profile.html', player_status=get_player_status(), sign_up_date=sign_up_date)


@app.route('/profile/change-password', methods=['GET', 'POST'])
def profile_change_password():
	error = None
	current_username = session['username']
	if request.method == 'POST':
		player = players.find_one({'username': session['username']})
		if request.form['oldPassword'] == "" or request.form['newPassword'] == "" or request.form[
			'newPasswordConfirm'] == "":
			error = "Actually enter a password, please..."
		elif check_password_hash(player['password'], request.form['oldPassword']):
			if request.form['newPassword'] == request.form['newPasswordConfirm']:
				players.update({'username': session['username']},
							   {'$set': {'password': generate_password_hash(request.form['newPassword'])}})
				return redirect(url_for('profile_change_password_confirm'))
			else:
				error = "Your passwords aren't the same. Try again…"
		else:
			error = "You've got the wrong password, mate. Try again…"
	return render_template('profile_change-password.html', error=error, current_username=current_username)


@app.route('/profile/change-password/confirm')
def profile_change_password_confirm():
	return render_template('profile_change-password_confirm.html')


@app.route('/profile/delete', methods=['GET', 'POST'])
def profile_delete():
	if request.method == 'POST':
		players.remove({'username': session['username']})
		session.clear()
		return redirect(url_for('home'))
	return render_template('profile_delete.html')


@app.route('/about')
def about():
	return render_template('about.html', player_status=get_player_status())
