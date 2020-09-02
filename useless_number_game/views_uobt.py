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


def is_node_full(node):
	return node['left'] != '' and node['right'] != ''


@app.route('/uobt')
@app.route('/uobt/')
def uobt_home():
	return render_template('uobt/home.html')


@app.route('/uobt/tree/navigate/<key>')
@app.route('/uobt/tree/navigate/<key>/')
# Pre: All values of key exist within the tree
def uobt_tree_navigate(key):
	node = nodes.find_one({'key': key})
	child_left = nodes.find_one({'key': node['left']})
	child_right = nodes.find_one({'key': node['right']})
	return render_template('uobt/tree_navigate.html', node=node, child_left=child_left, child_right=child_right)


@app.route('/uobt/tree/add', methods=['GET', 'POST'])
@app.route('/uobt/tree/add/', methods=['GET', 'POST'])
def uobt_tree_add():
	error = None

	if request.method == 'POST':
		new_node_exists = nodes.find_one({'key': request.form['key']})
		parent = nodes.find_one({'key': request.form['parent']})

		if new_node_exists:
			error = 'A node with that name already exists. Sorry.'
		elif request.form['key'] == '' or request.form['item'] == '' or request.form['parent'] == '':
			error = 'Dude, fill in the goddamn form, come on…'
		elif parent is None:
			error = 'That parent node does not exist. Oops!'
		elif is_node_full(parent):
			error = 'That parent node is already full!'
		else:
			author = session['username'] if 'username' in session else 'Unknown'
			new_node = {
				'key': request.form['key'],
				'author': author,
				'dateAdded': str(datetime.datetime.now().strftime("%Y-%m-%d")),
				'item': request.form['item'],
				'left': '',
				'right': ''
			}

			if parent['left'] == '':
				nodes.update(
					{'key': request.form['parent']},
					{'$set': {'left': request.form['key']}}
				)
			else:
				nodes.update(
					{'key': request.form['parent']},
					{'$set': {'right': request.form['key']}}
				)
			nodes.insert(new_node)
			# TODO: Clear form after submission
	return render_template('uobt/tree_add.html', error=error)


@app.route('/uobt/about')
@app.route('/uobt/about/')
def uobt_about():
	return render_template('uobt/about.html')
