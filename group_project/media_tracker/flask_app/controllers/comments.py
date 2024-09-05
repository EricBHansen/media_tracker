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

@app.route('/comment/add', methods=['POST'])
def add_comment():
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")    
    user = User.get_by_id(session["user_id"])
    data = {
        "users_id": session["user_id"],
        "comment": request.form['comment'],
        "movie_id": request.form['movie_id']
    }
    movie_id = request.form['movie_id']
    Comments.create(data)
    return redirect(f'/movie/show_movie/{movie_id}')

@app.route('/comment/delete/<int:id>')
def delete_comment(id):
    if "user_id" not in session:
        return redirect("/")
    Comments.delete(id)
    # get_movie_id = Comments.get_by_id(id)
    # movie_id = get_movie_id.movie_id
    # print(movie_id)
    return redirect('/dash')