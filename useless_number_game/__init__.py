"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

import useless_number_game.views
import useless_number_game.views_ung
import useless_number_game.views_uobt
import useless_number_game.views_um1
