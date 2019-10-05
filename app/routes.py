from app import app, db
from app.models import User, Post, Aquarium, AquariumData
from app.forms import LoginForm,RegistrationForm, CreateAquariumForm, CreatePostForm, CreateImagePostForm
from flask import request, render_template, flash, redirect,url_for, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from random import random
from time import sleep
from threading import Thread, Event
from app import socketio
from flask_socketio import send,emit
import json

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    form = LoginForm()
    regForm = RegistrationForm()

    if form.validate_on_submit() and form.userLogin.data:
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    elif regForm.validate_on_submit() and regForm.register.data:
        user = User(username=regForm.username.data, email=regForm.email.data)
        user.set_password(regForm.password.data)
        db.session.add(user)
        db.session.commit()

    return render_template('index.html', title='Home', form=form, regForm=regForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/data', methods=['GET','POST'])
def receive_data():
    print (
        request.form.get('UserID'),
        request.form.get('Aquarium'),
        request.form.get('Temperature'),
        request.form.get('PH'),
    )
    user = User.query.filter(User.username == request.form.get('UserID')).first()
    aqua = Aquarium.query.filter(Aquarium.userAquarium == user).filter(Aquarium.name == request.form.get('Aquarium')).first()
    
    data = AquariumData (
        linkedAquarium = aqua,
        temperature = request.form.get('Temperature'),
        ph = request.form.get('PH')
    )
    db.session.add(data)
    db.session.commit()
    return ('hello')

@app.route('/createAquarium', methods=['POST', 'GET'])
@login_required
def createAquarium():
    aquariumForm = CreateAquariumForm()
    a = Aquarium (
        name=aquariumForm.aquariumName.data, 
        userAquarium=current_user
    )
    tempData = AquariumData (
        linkedAquarium = a,
        temperature = 0,
        ph = 0
    )
    db.session.add(a)
    db.session.add(tempData)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))

@app.route('/createPost', methods = ['POST', 'GET'])
@login_required
def createPost():
    postForm = CreatePostForm()
    a = Post (
        author = current_user,
        body = postForm.postBody.data
    )
    print('hello')
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('newsfeed', username = current_user.username))

@app.route('/createImagePost', methods = ['POST', 'GET'])
@login_required
def createImagePost():
    postForm = CreateImagePostForm()
    a = Post (
        author = current_user,
        body = postForm.postBody.data
    )
    print('hello')
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('newsfeed', username = current_user.username))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    aquariumForm = CreateAquariumForm()
    aquariumList = user.aquariums.all()
    if len(aquariumList) == 0:
        return render_template('user.html', user=user, posts=posts, aquariumForm=aquariumForm)
    else:    
        defaultAquarium = aquariumList[0]
        defaultAquariumDataFile = defaultAquarium.data
        defaultAquariumDataOrdered = defaultAquariumDataFile.order_by(AquariumData.timestamp.desc()).first()
        return render_template('user.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
            defaultAquariumDataOrdered=defaultAquariumDataOrdered)

@app.route('/user/<username>/<aquarium>')
@login_required
def user1(username, aquarium):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    aquariumList = user.aquariums.all()
    defaultAquarium = Aquarium.query.filter(Aquarium.name == aquarium ).filter(Aquarium.user_id == user.id).first()
    defaultAquariumDataFile = defaultAquarium.data
    defaultAquariumDataOrdered = defaultAquariumDataFile.order_by(AquariumData.timestamp.desc()).first()
    return render_template('user.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
        defaultAquariumDataOrdered=defaultAquariumDataOrdered)
    
@app.route('/user/<username>/<aquarium>/analysis')
@login_required
def analysis(username, aquarium):
    user = User.query.filter_by(username=username).first_or_404()
    aquariumList = user.aquariums.all()
    defaultAquarium = Aquarium.query.filter(Aquarium.name == aquarium ).filter(Aquarium.user_id == user.id).first()
    return render_template('analysis.html', user=user, aquariumList=aquariumList, defaultAquarium=defaultAquarium)

@app.route('/user/<username>/newsfeed')
@login_required
def newsfeed(username):
    form = CreatePostForm()
    imageForm = CreateImagePostForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.all()
    aquariumForm = CreateAquariumForm()
    aquariumList = user.aquariums.all()
    if len(aquariumList) == 0:
        return render_template('user.html', user=user, posts=posts, aquariumForm=aquariumForm)
    else:    
        defaultAquarium = aquariumList[0]
        defaultAquariumDataFile = defaultAquarium.data
        defaultAquariumDataOrdered = defaultAquariumDataFile.order_by(AquariumData.timestamp.desc()).first()
        return render_template('newsfeed.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
            defaultAquariumDataOrdered=defaultAquariumDataOrdered, form=form, imageForm=imageForm)

@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))

@socketio.on('sendData')
def handle(json):
    jsonFile = {}
    for aquariums in current_user.aquariums:
        a = aquariums.data.order_by(AquariumData.timestamp.desc())
        dict = {
            'temp': a.first().temperature,
            'ph': a.first().ph
        }
        jsonFile[aquariums.name] = dict
    print (jsonFile)
    emit('data', jsonFile
    )

@socketio.on('analysisConnect')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))

@socketio.on('requestAnalysisData')
def handleRequest(json):
    print('received json: {0}'.format(str(json)))
    jsonFile = {}
    for aquariums in current_user.aquariums:
        a = aquariums.data.order_by(AquariumData.timestamp.desc())
        dict = {
            'temp': a.first().temperature,
            'ph': a.first().ph
        }
        jsonFile[aquariums.name] = dict
    print (jsonFile)
    emit('returnAnalysisData', jsonFile
    )
