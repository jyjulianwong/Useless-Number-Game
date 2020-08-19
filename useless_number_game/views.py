"""
Routes and views for the flask application.
"""

import flask, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app

app.config['MONGO_DBNAME'] = 'uselessnumbergame_players'
app.config['MONGO_URI'] = 'mongodb://useless_number_game:0000@ds012198.mlab.com:12198/uselessnumbergame_players'
uselessNumberGame_players = PyMongo(app)

@app.route('/')
@app.route('/start')
def home():
    if 'username' in session:
        playerStatus = 'Welcome, ' + session['username'] + '!'
    elif 'username' not in session: 
        playerStatus = 'Welcome, mate! Want to sign in?'
    return render_template('start.html', playerStatus=playerStatus)

@app.route('/signup', methods=['GET', 'POST'])
def signUp(): 
    error = None
    usernameInval = False
    usernameChar = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '[', '{', ']', '}', '|',';', ':', '"', ',', '<', '>', '/', '?', ' ']
    if request.method == 'POST': 
        players = uselessNumberGame_players.db.users
        existPlayer = players.find_one({'username' : request.form['username']})
        for n in usernameChar:
            if usernameInval == False: 
                if n in request.form['username']:
                    usernameInval = True
        if existPlayer is not None:
            error = "Someone's taken that username. Sorry."
        elif request.form['username'] == '': 
            error = 'Actually enter a username, please…'
        elif request.form['password'] == '':
            error = 'Actually enter a password, please…'
        elif (request.form['passwordRe'] == '') or (request.form['passwordRe'] != request.form['password']):
            error = "Your passwords aren't the same. Try again…"
        elif usernameInval == True:
            error = "You can't put special symbols or spaces in your username. Try again…"
        else:
            signUpDate = datetime.datetime.now()
            players.insert({'username' : request.form['username'], 'password' : generate_password_hash(request.form['password']), 'signUpDate' : str(signUpDate.strftime("%Y-%m-%d"))})
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('signup.html', error=error)

@app.route('/signin', methods=['GET', 'POST'])
def signIn():
    error = None
    if request.method == 'POST':
        players = uselessNumberGame_players.db.users
        signInPlayer = players.find_one({'username' : request.form['username']})
        if signInPlayer:
            if check_password_hash(signInPlayer['password'], request.form['password']) == True:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                error = "You've got the wrong username or password, mate."
        else:
            error = "You've got the wrong username, mate."
    return render_template('signin.html', error=error)

@app.route('/signout')
def signOut():
    session.clear()
    return render_template('signout.html')

@app.route('/main')
def main():
    if 'username' in session:
        playerStatus = 'Welcome, ' + session['username'] + '!'
    elif 'username' not in session: 
        playerStatus = 'Welcome, mate! Want to sign in?'
    return render_template('main.html', playerStatus=playerStatus)

@app.route('/profile')
def profile():
    if 'username' in session:
        playerStatus = 'Welcome, ' + session['username'] + '!'
        players = uselessNumberGame_players.db.users
        signUpDate = players.distinct('signUpDate', {'username' : session['username']})[0]
    elif 'username' not in session: 
        playerStatus = 'Welcome, mate! Want to sign in?'
        signUpDate = None
    return render_template('profile.html', playerStatus=playerStatus, signUpDate=signUpDate)

@app.route('/profile/change-password', methods=['GET', 'POST'])
def profile_changePassword():
    error = None
    currentUsername = session['username']
    if request.method == 'POST':
        players = uselessNumberGame_players.db.users
        currentPlayer = players.find_one({'username' : session['username']})
        if request.form['oldPassword'] == "" or request.form['newPassword'] == "" or request.form['newPassword2'] == "":
            error = "Actually enter a password, please..."
        elif check_password_hash(currentPlayer['password'], request.form['oldPassword']) == True:
            if request.form['newPassword'] == request.form['newPassword2']:
                players.update({'username' : session['username']}, {'$set' : {'password' : generate_password_hash(request.form['newPassword'])}})
                return redirect(url_for('profile_changePassword_confirm'))
            else:
                error = "Your passwords aren't the same. Try again…"
        else: 
            error = "You've got the wrong password, mate. Try again…"
    return render_template('profile_change-password.html', error=error, currentUsername=currentUsername)

@app.route('/profile/change-password/confirm')
def profile_changePassword_confirm():
    return render_template('profile_change-password_confirm.html')

@app.route('/profile/delete', methods=['GET', 'POST'])
def profile_delete():
    if request.method == 'POST':
        players = uselessNumberGame_players.db.users
        players.remove({'username' : session['username']})
        session.clear()
        return redirect(url_for('home'))
    return render_template('profile_delete.html')

@app.route('/about')
def about():
    if 'username' in session:
        playerStatus = 'Welcome, ' + session['username'] + '!'
    elif 'username' not in session: 
        playerStatus = 'Welcome, mate! Want to sign in?'
    return render_template('about.html', playerStatus=playerStatus)