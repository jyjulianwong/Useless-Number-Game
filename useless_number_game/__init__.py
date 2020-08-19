"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

import useless_number_game.views
