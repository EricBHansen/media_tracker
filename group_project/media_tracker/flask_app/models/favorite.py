from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models import movie
from flask_app.models import user


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# import the function that will return an instance of a connection


# model the class after the favorites table from our database
class Favorites:

    my_db = "media_tracker_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.movie_id = data["movie_id"]
        self.like = None


@classmethod
def create(cls, data):
    query = """
        INSERT INTO favorites
        (favorites,movie_id,user_id,created_at)
        VALUES (%(favorites)s,%(movie_id)s,%(user_id)s,%(created_at)s);

        """

    # this line returns the id of the new user.
    return connectToMySQL("media_tracker").query_db(query, data)


@classmethod
def get_all(cls):
    query = """
    SELECT *
    FROM favorites
    JOIN user
    ON user.id = favorites.movie_id.user_id;

    """

    # (favorites,movie_id,user_id,likes);
    # VALUES (%(favorites)s,%(movie_id)s,%(user_id)s);
    results = connectToMySQL(Favorites.my_db).query_db(query)
    all_favorites = []
    for dict in results:
        favorites = cls(dict)
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
        favorites.user = user_obj
        all_favorites.append(favorites)
        # debugging print query
        # print("query results:", results)
    return all_favorites


@classmethod
def join_tables_for_one_id(cls, favorites_id):
    query = """
    SELECT *
    FROM favorites
    JOIN user
    ON user.id = favorites.movie_id.user_id
    WHERE favorites.id=%(id)s;
    """
    data = {"id": favorites_id}
    results = connectToMySQL(Favorites.my_db).query_db(query, data)
    single_favorites = cls(results[0])
    for dict in results:
        user_data = {
            "id": dict["user.id"],
            "first_name": dict["first_name"],
            "last_name": dict["last_name"],
            "email": dict["email"],
            "password": None,
            "created_at": dict["user.created_at"],
            "updated_at": dict["user.updated_at"],
        }
        publisher = user.User(user_data)
        single_favorites.like = publisher
    return favorites_id


@classmethod
def get_by_id(cls, data_id):
    query = """
    SELECT *
    FROM favorites
    WHERE id = %(favorites_id)s;
    """
    data = {"favorites_id": data_id}
    results = connectToMySQL(Favorites.my_db).query_db(query, data)
    print(results)
    # if results is empty return none
    if len(results) == 0:
        return None
    return cls(results[0])


@classmethod
def update(cls, favorites_data):
    query = """
    UPDATE favorites
    SET 
    favorites=%(favorites)s,
    movie_id=%(movie_id)s,
    user_id=%(user_id)s,
    WHERE id =%(favorites_id)s;
    """

    favorites = connectToMySQL(Favorites.my_db).query_db(query, favorites_data)
    print(favorites)
    return favorites


@classmethod
def delete(cls, favorites_id):
    query = """
    DELETE FROM favorites
    WHERE id = %(id)s;
    """
    data = {"id": favorites_id}
    connectToMySQL(Favorites.my_db).query_db(query, data)
