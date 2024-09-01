from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app.models.movie import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


# model the class after the users table from our database
class User:
    my_db = "media_tracker_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = """

        INSERT INTO users
        (first_name,last_name,email,password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);

        """
        user_id = connectToMySQL(cls.my_db).query_db(query, data)
        # this line returns the id of the new user.
        return user_id

    # login in class info, not registration
    @classmethod
    def get_by_email(cls, email):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s;
        """
        result = connectToMySQL(cls.my_db).query_db(query, {"email":email})
        # if results is empty return none
        if len(result) == 0:
            return None

        # if results are not empty return a  user object.

        user = cls(result[0])
        return user

    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM users;

        """
        results=connectToMySQL(cls.my_db).query_db(query)
        users=[]
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_id(cls, user_id):
        query = """
        SELECT *
        FROM users
        WHERE id = %(user_id)s;
        """
        result = connectToMySQL(cls.my_db).query_db(query, {"user_id":user_id})
        # if results is empty return none
        if len(result) == 0:
            return None

        # if results are not empty return a  user object.

        user = cls(result[0])
        return user

    # code Validation! write for loop in html for this validation.
    @staticmethod
    def register_validator(form_data):
        is_valid = True
        #  First name validation
        if len(form_data["first_name"].strip()) == 0:
            is_valid = False
            flash("First Name required for registration", "registration")
        elif len(form_data["first_name"].strip()) < 2:
            is_valid = False
            flash("2 character min", "registration")

        #  Last name validation
        if len(form_data["last_name"].strip()) == 0:
            is_valid = False
            flash("Last Name required for registration", "registration")
        elif len(form_data["last_name"].strip()) < 2:
            is_valid = False
            flash("2 character min", "registration")

        # email name validation
        if len(form_data["email"].strip()) == 0:
            is_valid = False
            flash("Email required for registration", "registration")
        elif not EMAIL_REGEX.match(form_data["email"].strip()):
            is_valid = False
            flash("invalid email", "registration")

        # password validation
        if len(form_data["password"].strip()) == 0:
            is_valid = False
            flash("Password required for registration", "registration")
        elif len(form_data["password"].strip()) < 8:
            is_valid = False
            flash("8 character min", "registration")
        elif form_data["password"].strip() != form_data["confirm_pw"].strip():
            is_valid = False
            flash("passwords must match, to register", "registration")

        return is_valid

    @staticmethod
    def login_validator(form_data):
        is_valid = True
        # email name validation
        if len(form_data["email"].strip()) == 0:
            is_valid = False
            flash("Existing email required for login", "login")
        elif not EMAIL_REGEX.match(form_data["email"]):
            is_valid = False
            flash("invalid email", "login")

        # password validation
        if len(form_data["password"].strip()) == 0:
            is_valid = False
            flash(" Existing password required for valid login", "login")
        elif len(form_data["password"]) < 8:
            is_valid = False
            flash("8 character min", "login")
        return is_valid
