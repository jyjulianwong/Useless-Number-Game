"""
This script runs the useless_number_game application using a development server.
"""

from os import environ
from useless_number_game import app

app.secret_key = 'useless_number_game'

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
