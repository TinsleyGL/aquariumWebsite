from app import app, db
from app.models import User,Post,Aquarium
from app.forms import LoginForm,RegistrationForm
from flask import request, render_template, flash, redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from random import random
from time import sleep
from threading import Thread, Event
from app import socketio
from flask_socketio import send,emit

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/data', methods=['GET','POST'])
def receive_data():
    print (
        request.form.get('UserID'),
        request.form.get('Aquarium'),
        request.form.get('Temperature'),
        request.form.get('PH'),
        User.query.get(int(request.form.get('UserID')))
    )
    
    data = Aquarium (
        userAquarium = User.query.get(int(request.form.get('UserID'))),
        name = request.form.get('Aquarium'),
        temperature = request.form.get('Temperature'),
        ph = request.form.get('PH')
    )
    db.session.add(data)
    db.session.commit()
    
    return (request.form.get('PH'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = user.posts.all()
    aquariums = user.aquariums.all()
    return render_template('user.html', user=user, posts=posts, aquariums=aquariums)

@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))

@socketio.on('sendData')
def handle(json):
    #print('received json: {0}'.format(str(json)))
    for aquariums in current_user.aquariums:
        emit('data', {
            'temp': aquariums.temperature,
            'ph': aquariums.ph
            }
        )