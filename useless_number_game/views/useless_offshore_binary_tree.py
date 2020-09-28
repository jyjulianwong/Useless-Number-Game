"""
Routes and views for the flask application.
"""

import flask, ssl, datetime
from flask import Flask, Config, Blueprint, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from useless_number_game import app

blueprint = Blueprint('useless_offshore_binary_tree', __name__, url_prefix='/uselessoffshorebinarytree')

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


@blueprint.route('/')
def home():
	return render_template('useless_offshore_binary_tree/home.html', title_ext='')


@blueprint.route('/tree/navigate/<key>')
@blueprint.route('/tree/navigate/<key>/')
# Pre: All values of key exist within the tree
def tree_navigate(key):
	node = nodes.find_one({'key': key})
	child_left = nodes.find_one({'key': node['left']})
	child_right = nodes.find_one({'key': node['right']})
	return render_template(
		'useless_offshore_binary_tree/tree_navigate.html',
		title_ext='Navigate {} – '.format(node['key']),
		node=node,
		child_left=child_left,
		child_right=child_right
	)


@blueprint.route('/tree/add', methods=['GET', 'POST'])
@blueprint.route('/tree/add/', methods=['GET', 'POST'])
def tree_add():
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
	return render_template(
		'useless_offshore_binary_tree/tree_add.html',
		title_ext='Add a Node – ',
		error=error
	)


@blueprint.route('/about')
@blueprint.route('/about/')
def about():
	return render_template(
		'useless_offshore_binary_tree/about.html',
		title_ext='About – '
	)
