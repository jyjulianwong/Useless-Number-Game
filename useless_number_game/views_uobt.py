"""
Routes and views for the flask application.
"""

import flask, ssl, datetime
from flask import Flask, Config, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app

cluster_username = 'admin'
cluster_password = 'admin'
cluster_dbname = 'useless-offshore-binary-tree'

app.config['MONGO_DBNAME'] = cluster_dbname
app.config['MONGO_URI'] = 'mongodb+srv://{}:{}@useless-number-game.idxzf.azure.mongodb.net/{}?retryWrites=false&w=majority'.format(
	cluster_username,
	cluster_password,
	cluster_dbname
)

nodes = PyMongo(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE).db.nodes


@app.route('/uobt')
@app.route('/uobt/')
def uobt_home():
	return render_template('uobt/home.html')


@app.route('/uobt/tree/add', methods=['GET', 'POST'])
@app.route('/uobt/tree/add/', methods=['GET', 'POST'])
def uobt_tree_add():
	return render_template('uobt/tree_add.html')
