from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

from flask_app.models import user


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# import the function that will return an instance of a connection


# model the class after the movie table from our database
class Movie:

    # model the class after the movie table from our database

    my_db = "media_tracker_schema"

# details to input
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.release_date = data["release_date"]
        self.director = data["director"]
        self.details = data["details"]
        # self.created_at = data["created_at"]
        # self.updated_at = data["updated_at"]
        self.owner_id = data["owner_id"]

# CRUD Create method
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO movies
        (title,release_date,details,director,owner_id)
        VALUES (%(title)s,%(release_date)s,%(details)s,%(director)s,%(owner_id)s);

        """
        # data = data.copy()
        # data["owner_id"] = session["owner_id"]

        # this line returns the id of the new user.
        return connectToMySQL("media_tracker_schema").query_db(query, data)

# CRUD Read All method
    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM movies

        """

        results = connectToMySQL(cls.my_db).query_db(query)
        movies = []
        for movie in results:
            movies.append(cls(movie))
        return movies

# ???? Not working v need to look further
    @classmethod
    def movie_and_owner_details(cls, movie_id):
        query = """
        SELECT * FROM movies
        LEFT JOIN users
        ON movies.owner_id = users.id
        WHERE movie.id=%(movie_id)s;
        """
        result = connectToMySQL(cls.my_db).query_db(query, {"movie_id": movie_id})

        return result

# CRUD Read One method
    @classmethod
    def get_by_id(cls, movie_id):
        query = """ SELECT * FROM movies WHERE id = %(movie_id)s;"""
        result = connectToMySQL(cls.my_db).query_db(query, {"movie_id": movie_id})
        if len(result) == 0:
            return None
        movie = cls(result[0])
        return movie

    @classmethod
    def update(cls, data):
        query = """ UPDATE movies SET title=%(title)s, release_date=%(release_date)s, director=%(director)s, details=%(details)s WHERE id =%(id)s;"""

        connectToMySQL(cls.my_db).query_db(query, data)
        return

    @classmethod
    def delete(cls, movie_id):
        query = """
        DELETE FROM movies
        WHERE id = %(id)s;
        """
        data = {"id": movie_id}
        connectToMySQL(cls.my_db).query_db(query, data)
        return

    @staticmethod
    def is_valid(form_data):
        is_valid = True

        # Title validation
        if len(form_data["title"].strip()) == 0:
            is_valid = False
            flash("Name Required", "add_movie")
        elif len(form_data["title"]) < 2:
            is_valid = False
            flash("3 Character min", "add_movie")

        # Details validation
        if len(form_data["details"].strip()) == 0:
            is_valid = False
            flash("Details Required", "add_movie")
        elif len(form_data["details"]) < 10:
            is_valid = False
            flash("10 Character min", "add_movie")

        #Director Validation
        if len(form_data["director"].strip()) == 0:
            is_valid = False
            flash("Director Required", "add_movie")
        elif len(form_data["director"]) < 2:
            is_valid = False
            flash("Director names are short but not that short", "add_movie")

        # Release Date validation
        if form_data["release_date"] == None:
            is_valid = False
            flash("Release Date Required", "add_movie")
            # date validation

        print(is_valid)
        return is_valid 
