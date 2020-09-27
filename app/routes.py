from flask import render_template, flash, redirect, url_for,request
import json
from werkzeug.urls import url_parse
from app import app
from app import db
from flask_login import current_user, login_user,logout_user,login_required
from app.models import Admin,Movie
from app.forms import LoginForm,RegistrationForm

#index route for admin user
@app.route('/index')
@login_required
def index():
    try:
        movie_list = []
        m = Movie.query.all()
        for i in m:
            mydict = {}
            mydict['name'] = i.name
            mydict['imdb_score'] = i.score
            mydict['genre'] = i.genre
            mydict['director'] = i.director
            mydict['99popularity'] = i.popularity
            mydict['author'] = i.author.username
            movie_list.append(mydict)
        return render_template('index.html', title='Home', movies=movie_list)
    except Exception as e:
        raise e

#login route for admin user
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = Admin.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)
    except Exception as e:
        raise e

#add to db operation route for admin user
@login_required
@app.route('/movies/add', methods=['POST'])
def add():
    try:
        print("request",request)
        all_args = request.form.to_dict(flat=True)
        all_args['username'] = current_user.username
        # Now add all_args to create snooze db.
        u = Admin.query.filter_by(username=current_user.username).first()
        m = Movie(name= all_args['name'],score = all_args['score'],director = all_args['director'],
                  popularity = all_args['popularity'],genre = all_args['genre'],author = u)
        db.session.add(m)
        db.session.commit()
        return "Success"
    except Exception as e:
        raise e

#Edit db operation route for admin user
@login_required
@app.route('/movies/edit', methods=['POST'])
def edit():
    try:
        all_args = request.form.to_dict(flat=True)
        actual_dict = {}
        for key,val in all_args.items():
            if val != '':
                actual_dict[key] = val
        m = Movie.query.filter_by(name = actual_dict['mnamechng']).first()
        if 'name' in actual_dict.keys():
            m.name = actual_dict['name']
        if 'score' in actual_dict.keys():
            m.score = actual_dict['score']
        if 'director' in actual_dict.keys():
            m.director = actual_dict['director']
        if 'genre' in actual_dict.keys():
            m.genre = actual_dict['genre']
        if 'popularity' in actual_dict.keys():
            m.popularity = actual_dict['popularity']

        db.session.commit()

        return "Success"
    except Exception as e:
        raise e

#del from db operation route for admin user
@login_required
@app.route('/movies/delete', methods=['POST'])
def delete():
    try:
        all_args = request.form.to_dict(flat=True)
        m = Movie.query.filter_by(name = all_args['movie_name']).first()
        db.session.delete(m)
        db.session.commit()
        return "success"
    except Exception as e:
        raise e

#Search operation route for all users
@app.route('/movies/search', methods=['POST'])
def search():
    try:
        all_args = request.form.to_dict(flat=True)
        result_list = []
        search = "%{}%".format(all_args['movie_name'])
        print("search",search)
        m = Movie.query.filter(Movie.name.like(search)).all()
        print("search_result",m)
        if m is None:
            return json.dumps([])
        for i in m:
            result_dict = {}
            result_dict['name'] = i.name
            result_dict['score'] = i.score
            result_dict['director'] = i.director
            result_dict['popularity'] = i.popularity
            result_dict['genre'] = i.genre
            result_dict['notfound'] = 'found'
            result_list.append(result_dict)
        print("result_list",result_list)
        return json.dumps(result_list)
    except Exception as e:
        raise e

#get movie name route for admin user
@login_required
@app.route('/movies/names', methods=['GET'])
def get_movie_name():
    try:
        movie_list = []
        m = Movie.query.all()
        for i in m:
            movie_list.append(i.name)
        return json.dumps(movie_list)
    except Exception as e:
        raise e

#logout from application route for admin user
@app.route('/logout')
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except Exception as e:
        raise e

#INdex or main route for any user
@app.route('/')
def user():
    try:
        movie_list = []
        m = Movie.query.all()
        for i in m:
            mydict = {}
            mydict['name'] = i.name
            mydict['imdb_score'] = i.score
            mydict['genre'] = i.genre
            mydict['director'] = i.director
            mydict['99popularity'] = i.popularity
            mydict['author'] = i.author.username
            movie_list.append(mydict)
        return render_template('user.html', title='Home', movies=movie_list)
    except Exception as e:
        raise e

#register new user as admin route
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = Admin(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)
    except Exception as e:
        raise e




