"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

from useless_number_game.views import home, anjuls_sleep_indicator, useless_blog, useless_meme_1, useless_meme_2, useless_number_game, useless_offshore_binary_tree

app.register_blueprint(home.blueprint)
app.register_blueprint(anjuls_sleep_indicator.blueprint)
app.register_blueprint(useless_blog.blueprint)
app.register_blueprint(useless_meme_1.blueprint)
app.register_blueprint(useless_meme_2.blueprint)
app.register_blueprint(useless_number_game.blueprint)
app.register_blueprint(useless_offshore_binary_tree.blueprint)
