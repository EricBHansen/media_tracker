from flask_app import app
from flask import (
    redirect,
    session,
    request,
    flash,
    render_template,
)

from flask_app.models.movie import Movie
from flask_app.models.user import User
from flask_app.models.comment import Comments
#from flask_app.models.favorite import Favorites


# session["id_user"] = user_in_db.id
# dashboard for /movie = belt exam

@app.route("/add_movie")
def movie_form():
    user = User.get_by_id(session["user_id"])
    
    return render_template("add_movie.html", user=user)

@app.post("/process_movie")
def add_movie():
    if not "user_id" in session:
        flash("try again")
        return redirect("/")

    if not Movie.is_valid(request.form):
        return redirect("/add_movie")
    data = {
        "title": request.form["title"],
        "release_date": request.form["release_date"],
        "director": request.form["director"],
        "details": request.form["details"],
        "owner_id": session["user_id"],
    }
    Movie.create(data)
    return redirect("/dash")


@app.route("/update/<int:movie_id>")
def update(movie_id):
    if not "user_id" in session:
        flash("Please log in or register")
        return redirect("/")
    movie=Movie.get_by_id(movie_id)

    return render_template("update_movie.html", movie=movie)


@app.route("/movie/show_movie/<int:movie_id>")
def details_movie(movie_id):
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")
    user = User.get_by_id(session["user_id"])

    movie = Movie.get_by_id(movie_id)

    # comments = Comments.get_comments_by_movie(movie_id)

    return render_template("details_movies.html", user=user, movie=movie)

@app.route("/movie/edit/<int:movie_id>", methods=["POST"])
def edit(movie_id):
    print(request.form)
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")
    #if Movie.is_valid(request.form):
    #    flash("Updated!")
    data = {
        "id": movie_id,
        "title": request.form["title"],
        "release_date": request.form["release_date"],
        "director": request.form["director"],
        "details": request.form["details"],
    }
    Movie.update(data)
    return redirect(f"/movie/show_movie/{movie_id}")


# add post route to handle edit form submission
# post will have the movie_id
# use movie validator to validate form input
# make a regular dictionary out the request.form
# add movie_id to the regular dictionary
# in my query the movie_id will be for the where clause.
#  always redirect after a post route
@app.route("/movie/update/<int:movie_id>", methods=["POST"])
def update_edit(movie_id):
    if not "user_id" in session:
        flash("try again")
        return redirect("/")
    if Movie.is_valid(request.form):
        flash("Updated!")
    data = {
        "movie_title": request.form["movie_title"],
        "release_year": request.form["release_year"],
        "description": request.form["description"],
        "id": movie_id,
        "user_id": session["user_id"],
    }
    Movie.update(data)
    print(request.form)
    return redirect("/dash")


@app.route("/movie/delete/<int:movie_id>")
def delete(movie_id):
    if "user_id" not in session:
        return redirect("/")
    Movie.delete(movie_id)

    return redirect("/dash")
