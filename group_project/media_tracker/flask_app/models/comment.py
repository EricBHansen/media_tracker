from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models import movie
from flask_app.models import user
from flask_app.models import comment
# from flask_app.models import favorites


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# import the function that will return an instance of a connection


# model the class after the comments table from our database
class Comments:

    # model the class after the comments table from our database

    my_db = "media_tracker_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.movie_id = data["movie_id"]
        self.users_id = data["users_id"]
        self.created_at = data["created_at"]
        self.review = None


    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO movie_comments
            (comment, movie_id, users_id)
            VALUES (%(comment)s, %(movie_id)s, %(users_id)s);

            """

        # this line returns the id of the new user.
        return connectToMySQL(cls.my_db).query_db(query, data)

    # @classmethod
    # def get_movie_by_comments(cls, data):
    #     query = """
    #     SELECT * 
    #     FROM movie_comments
    #     WHERE id = %(movie_id)s;
    #     """
    #     results = connectToMySQL(cls.my_db).query_db(query, data)
    #     movie_with_comments = []
    #     for comment in results:
    #         movie_with_comments.append(cls(comment))
    #     return movie_with_comments


    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM movie_comments
        JOIN user
        ON user.id = comments.movie_id.user_id;

        """

        # (comments,movie_id,user_id,likes);
        # VALUES (%(comments)s,%(movie_id)s,%(user_id)s);
        results = connectToMySQL(Comments.my_db).query_db(query)
        all_comments = []
        for dict in results:
            comments = cls(dict)
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
            comments.user = user_obj
            all_comments.append(comments)
            # debugging print query
            # print("query results:", results)
        return all_comments


    @classmethod
    def join_tables_for_one_id(cls, comments_id):
        query = """
        SELECT *
        FROM comments
        JOIN user
        ON user.id = comments.movie_id.user_id
        WHERE comments.id=%(id)s;
        """
        data = {"id": comments_id}
        results = connectToMySQL(Comments.my_db).query_db(query, data)
        single_comments = cls(results[0])
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
            single_comments.review = publisher
        return comments_id


    @classmethod
    def get_by_id(cls, data_id):
        query = """
        SELECT *
        FROM comments
        WHERE id = %(comments_id)s;
        """
        data = {"comments_id": data_id}
        results = connectToMySQL(Comments.my_db).query_db(query, data)
        print(results)
        # if results is empty return none
        if len(results) == 0:
            return None
        return cls(results[0])


    @classmethod
    def update(cls, comments_data):
        query = """
        UPDATE comments
        SET 
        comments=%(comments)s,
        movie_id=%(movie_id)s,
        user_id=%(user_id)s,
        WHERE id =%(comments_id)s;
        """

        comments = connectToMySQL(Comments.my_db).query_db(query, comments_data)
        print(comments)
        return comments
    

    @classmethod
    def delete(cls, comments_id):
        query = """
        DELETE FROM comments
        WHERE id = %(id)s;
        """
        data = {"id": comments_id}
        connectToMySQL(Comments.my_db).query_db(query, data)


    @staticmethod
    def is_valid(form_data):
        is_valid = True
        # presence validation aka. make sure they type something.
        if len(form_data["comments"].strip()) == 0:
            is_valid = False
            flash("Name Required", "comments")
        elif len(form_data["comments"]) < 2:
            is_valid = False
            flash("3 Character min", "comments")
            # decription validation

        print(is_valid)
        return is_valid
