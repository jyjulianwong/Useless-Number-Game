"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

from useless_number_game.views import home, asi, ub, um1, um2, ung, uobt

app.register_blueprint(home.blueprint)
app.register_blueprint(asi.blueprint)
app.register_blueprint(ub.blueprint)
app.register_blueprint(um1.blueprint)
app.register_blueprint(um2.blueprint)
app.register_blueprint(ung.blueprint)
app.register_blueprint(uobt.blueprint)
