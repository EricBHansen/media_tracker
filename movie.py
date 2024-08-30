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

    my_db = "media_tracker.movie"

    def __init__(self, data):
        self.id = data["id"]
        self.movie_title = data["movie_title"]
        self.release_year = data["release_year"]
        self.description = data["description"]
        self.likes = data["likes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.owner_id = data["owner_id"]
        self.critic = None

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO movie
        (movie_title,release_year,description,likes,owner_id)
        VALUES (%(movie_title)s,%(release_year)s,%(description)s,%(likes)s,%(owner_id)s);

        """
        # data = data.copy()
        # data["owner_id"] = session["owner_id"]

        # this line returns the id of the new user.
        return connectToMySQL("media_tracker").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM movie
        JOIN users
        ON user.id = movie.owner_id;

        """

        # (movie_title,release_year,description,likes,owner_id);
        # VALUES (%(movie_title)s,%(release_year)s,%(description)s,%(likes)s,%)s,%(user_id)s);
        results = connectToMySQL(Movie.my_db).query_db(query)
        all_movie = []
        for dict in results:
            movie = cls(dict)
            user_data = {
                "id": dict["user_id"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": dict["password"],
                "created_at": dict["created_at"],
                "updated_at": dict["updated_at"],
            }

            user_obj = user.User(user_data)
            movie.user = user_obj
            all_movie.append(movie)
            # debugging print query
            # print("query results:", results)
        return all_movie

    @classmethod
    def join_tables_for_one_id(cls, movie_id):
        query = """
        SELECT *
        FROM movie
        JOIN users
        ON users.id = movie.owner_id
        WHERE movie.id=%(id)s;
        """
        data = {"id": movie_id}
        results = connectToMySQL(Movie.my_db).query_db(query, data)
        single_movie = cls(results[0])
        for dict in results:
            user_data = {
                "id": dict["users.id"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": None,
                "created_at": dict["users.created_at"],
                "updated_at": dict["users.updated_at"],
            }
            publisher = user.User(user_data)
            single_movie.chef = publisher
        return single_movie

    @classmethod
    def get_by_id(cls, data_id):
        query = """
        SELECT *
        FROM movie
        WHERE id = %(movie_id)s;
        """
        data = {"movie_id": data_id}
        results = connectToMySQL(Movie.my_db).query_db(query, data)
        print(results)
        # if results is empty return none
        if len(results) == 0:
            return None
        return cls(results[0])

    @classmethod
    def update(cls, movie_data):
        query = """
        UPDATE movie
        SET 
        movie_title=%(movie_title)s,
        release_year=%(release_year)s,
        description=%(description)s,
        likes=%(likes)s,
        WHERE id =%(movie_id)s;
        """

        movie = connectToMySQL(Movie.my_db).query_db(query, movie_data)
        print(movie)
        return movie

    @classmethod
    def delete(cls, movie_id):
        query = """
        DELETE FROM movie
        WHERE id = %(id)s;
        """
        data = {"id": movie_id}
        connectToMySQL(Movie.my_db).query_db(query, data)

    @staticmethod
    def is_valid(form_data):
        is_valid = True
        # presence validation aka. make sure they type something.
        if len(form_data["movie_title"].strip()) == 0:
            is_valid = False
            flash("Name Required", "movie_title")
        elif len(form_data["movie_title"]) < 2:
            is_valid = False
            flash("3 Character min", "movie_title")
            # decription validation
        if len(form_data["description"].strip()) == 0:
            is_valid = False
            flash("Description Required", "description")
        elif len(form_data["description"]) < 10:
            is_valid = False
            flash("10 Character min", "description")
            # Instruction validation
        if len(form_data["likes"].strip()) == 0:
            is_valid = False
            flash("Instructions Required", "likes")
        elif len(form_data["likes"]) < 10:
            is_valid = False
            flash("More details please! 10 char min!", "likes")
            # date validation

        if form_data.get("release_year") is None:
            is_valid = False
            flash("Input! Required", "release_year")
            # radio button validation

        print(is_valid)
        return is_valid
