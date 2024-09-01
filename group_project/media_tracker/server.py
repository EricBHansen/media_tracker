from flask_app import app
from flask_app.controllers import users, movies

# need to import: movies, favorites from flask_app.controllers


if __name__ == '__main__':

    app.run(debug=True)