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
#from flask_app.models.comment import Comments
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
    user = User.get_by_id(session["user_id"])

    return render_template("update_movie.html", movie=movie, user=user)


@app.route("/movie/show_movie/<int:movie_id>")
def details_movie(movie_id):
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")

    # create variable to use to call on this html page in Jinja

    return render_template(
        "details_movie.html", movie=Movie.join_tables_for_one_id(movie_id)
    )


@app.route("/movie/details/<int:movie_id>")
def details(movie_id):
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")
    #    # get_all method

    # user = User.get_by_id("user_id")
    query_results = Movie.get_by_id(movie_id)
    # call the Movie class details = Movie.join_tables_for_one_id()
    return render_template("details_movie.html", all_movies=query_results)


@app.route("/movie/edit/<int:movie_id>", methods=["POST"])
def edit(movie_id):
    print(request.form)
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")
    if Movie.is_valid(request.form):
        flash("Updated!")
        data = {
            "title": request.form["title"],
            "release_date": request.form["release_date"],
            "director": request.form["director"],
            "details": request.form["details"],
            "id": movie_id,
            "user_id": session["user_id"],
        }
        Movie.update(data)
        return redirect("/dashboard")
    return redirect(f"/update/{movie_id}")


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
        "title": request.form["title"],
        "release_date": request.form["release_date"],
        "director": request.form["director"],
        "details": request.form["details"],
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
