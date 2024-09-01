# User controller goes here
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app import bcrypt
from flask import render_template, redirect, request, session, flash

@app.route('/')
def login_registration():
    return render_template('login_and_reg.html')

@app.post('/process')
def create():
    if not User.register_validator(request.form):
        return redirect('/')
    
    potential_user = User.get_by_email(request.form['email'])

    if potential_user != None:
        flash("Account already exists with this email", 'register')
        return redirect('/')
        
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect('/dash')

@app.post('/login')
def login():
    if not User.login_validator(request.form):
        return redirect('/')
    potential_user = User.get_by_email(request.form['email'])

    if potential_user == None:
        flash("Invalid credentials", "login")
    
    user = potential_user
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dash')

@app.get('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dash')
def success():
    if "user_id" not in session:
        return redirect('/')
    
    user=User.get_by_id(session["user_id"])
    users=User.get_all()
    movies=Movie.get_all()

    return render_template('success.html', user=user, users=users, movies=movies)