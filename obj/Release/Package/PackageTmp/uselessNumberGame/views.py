"""
Routes and views for the flask application.
"""

from flask import render_template
from uselessNumberGame import app

@app.route('/')
@app.route('/start')
def home():
    return render_template(
        'home.html',
    )

@app.route('/main')
def main():
    return render_template(
        'main.html',
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',        
    )