from app import app, db, images
from app.models import User, Post, Aquarium, AquariumData
from app.forms import LoginForm,RegistrationForm, CreateAquariumForm, CreatePostForm, UpdateAquariumImageForm, UpdateProfilePictureForm
from flask import request, render_template, flash, redirect,url_for, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from random import random
from time import sleep
from threading import Thread, Event
from app import socketio
from flask_socketio import send,emit
import json
from sqlalchemy import desc

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))

    form = LoginForm()
    regForm = RegistrationForm()
    if form.validate_on_submit() and form.userLogin.data:
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid username or password', 'loginError')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    elif regForm.validate_on_submit() and regForm.register.data:
        if regForm.validate_username(regForm.username) == False:
            flash(u'Please use a different username.', 'regError')
            return redirect(url_for('index'))
        elif regForm.validate_email(regForm.email) == False:
            flash(u'Please use a different email address.', 'regError')
            return redirect(url_for('index'))
        else:
            user = User(username=regForm.username.data, email=regForm.email.data)
            user.set_password(regForm.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('user', username=current_user.username))
    return render_template('index.html', title='Home', form=form, regForm=regForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#test data incoming from raspberry pi, wont affect database
@app.route('/testData', methods=['GET','POST'])
def testdata():
    print (
        request.form.get('UserID'),
        request.form.get('Aquarium'),
        request.form.get('Temperature'),
        request.form.get('pH'),
        request.form.get('Flow'),
        request.form.get('Turbidity')
    )
    return ('success')


@app.route('/data', methods=['GET','POST'])
def receive_data():
    print (
        request.form.get('UserID'),
        request.form.get('Aquarium'),
        request.form.get('Temperature'),
        request.form.get('pH'),
        request.form.get('Flow'),
        request.form.get('Turbidity')
    )
    user = User.query.filter(User.username == request.form.get('UserID')).first()
    aqua = Aquarium.query.filter(Aquarium.userAquarium == user).filter(Aquarium.name == request.form.get('Aquarium')).first()
    
    data = AquariumData (
        linkedAquarium = aqua,
        temperature = request.form.get('Temperature'),
        ph = request.form.get('pH'),
        filterFlow = request.form.get('Flow'),
        waterClarity = request.form.get('Turbidity')
    )
    db.session.add(data)
    db.session.commit()
    return ('success')

@app.route('/createAquarium', methods=['POST', 'GET'])
@login_required
def createAquarium():
    aquariumForm = CreateAquariumForm()
    #if the aquarium name already exists
    if not Aquarium.query.filter_by(userAquarium=current_user).filter_by(name=aquariumForm.aquariumName.data).first():
        a = Aquarium (
            name=aquariumForm.aquariumName.data, 
            userAquarium=current_user,
            targetTemperature = aquariumForm.targetTemp.data,
            targetPH = aquariumForm.targetPH.data,
            targetWaterflow = aquariumForm.targetWaterflow.data,
            targetClarity = aquariumForm.targetClarity.data
        )
        tempData = AquariumData (
            linkedAquarium = a,
            temperature = 0,
            ph = 0,
            filterFlow = 0,
            waterClarity = 0
        )
        db.session.add(a)
        db.session.add(tempData)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    elif Aquarium.query.filter_by(userAquarium=current_user).filter_by(name=aquariumForm.aquariumName.data).first(): 
        flash(u'Aquarium already exists, please try another name', 'createError')
        return redirect(url_for('addAquarium', username = current_user.username))        


@app.route('/createPost', methods = ['POST', 'GET'])
@login_required
def createPost():
    postForm = CreatePostForm()
    if request.files['aquariumImage']:
        filename = images.save(request.files['aquariumImage'], folder='postImages/')
        url = images.url(filename)
        a = Post (
            author = current_user,
            body = postForm.postBody.data,
            image_url = url,
            image_filename = filename
        )
    else:
        a = Post (
            author = current_user,
            body = postForm.postBody.data
        )
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('newsfeed', username = current_user.username))

@app.route('/updateAquariumImage', methods = ['POST', 'GET'])
@login_required
def updateAquariumImage():
    imageForm = UpdateAquariumImageForm()
    filename = images.save(request.files['aquariumImage'], folder='aquariumImages/')
    url = images.url(filename)
    aquariumToChange = Aquarium.query.filter(Aquarium.name == imageForm.aquariumName.data ).filter(Aquarium.user_id == current_user.id).first()
    aquariumToChange.image_filename = filename
    aquariumToChange.image_url = url
    db.session.commit()

    #chnage this redirect to correct aquarium
    return redirect(url_for('user', username = current_user.username))

@app.route('/updateProfileImage', methods = ['POST', 'GET'])
@login_required
def updateProfileImage():
    imageForm = UpdateProfilePictureForm()
    filename = images.save(request.files['profileImage'], folder='avatarImages/')
    url = images.url(filename)
    current_user.image_filename = filename
    current_user.image_url = url
    db.session.commit()
    #chnage this redirect to correct aquarium
    return redirect(url_for('user', username = current_user.username))


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
        imageForm = UpdateAquariumImageForm()
        profileImageForm = UpdateProfilePictureForm()
        return render_template('user.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
            defaultAquariumDataOrdered=defaultAquariumDataOrdered, imageForm=imageForm, profileImageForm = profileImageForm)

@app.route('/user/<username>/<aquarium>')
@login_required
def user1(username, aquarium):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    aquariumList = user.aquariums.all()
    defaultAquarium = Aquarium.query.filter(Aquarium.name == aquarium ).filter(Aquarium.user_id == user.id).first()
    defaultAquariumDataFile = defaultAquarium.data
    defaultAquariumDataOrdered = defaultAquariumDataFile.order_by(AquariumData.timestamp.desc()).first()
    imageForm = UpdateAquariumImageForm()
    profileImageForm = UpdateProfilePictureForm()
    return render_template('user.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
        defaultAquariumDataOrdered=defaultAquariumDataOrdered, imageForm=imageForm, profileImageForm = profileImageForm)
    
@app.route('/user/<username>/<aquarium>/analysis')
@login_required
def analysis(username, aquarium):
    profileImageForm = UpdateProfilePictureForm()
    user = User.query.filter_by(username=username).first_or_404()
    aquariumList = user.aquariums.all()
    defaultAquarium = Aquarium.query.filter(Aquarium.name == aquarium ).filter(Aquarium.user_id == user.id).first()
    weeklyChartData = defaultAquarium.weekChartData('ph','temp','flow','clarity')
    monthlyChartData = defaultAquarium.monthChartData('ph','temp','flow','clarity')
    yearlyChartData = defaultAquarium.yearChartData('ph','temp','flow','clarity')
    return render_template('analysis.html', user=user, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
    weeklyChartData=weeklyChartData, monthlyChartData=monthlyChartData, yearlyChartData=yearlyChartData, profileImageForm = profileImageForm)

@app.route('/user/<username>/newsfeed')
@login_required
def newsfeed(username):
    form = CreatePostForm()
    profileImageForm = UpdateProfilePictureForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.timestamp.desc())
    aquariumList = user.aquariums.all()
    defaultAquarium = aquariumList[0]
    return render_template('newsfeed.html', user=user, posts=posts, aquariumList=aquariumList,
        form=form, defaultAquarium=defaultAquarium,profileImageForm=profileImageForm)

@app.route('/user/<username>/yourPosts')
@login_required
def yourPosts(username):
    profileImageForm = UpdateProfilePictureForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc())
    aquariumList = user.aquariums.all()
    if len(aquariumList) == 0:
        return render_template('user.html', user=user, posts=posts, aquariumForm=aquariumForm)
    else:    
        defaultAquarium = aquariumList[0]
        defaultAquariumDataFile = defaultAquarium.data
        defaultAquariumDataOrdered = defaultAquariumDataFile.order_by(AquariumData.timestamp.desc()).first()
        return render_template('yourPosts.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
            defaultAquariumDataOrdered=defaultAquariumDataOrdered,profileImageForm=profileImageForm)

@app.route('/user/<username>/followedUsers')
@login_required
def followedUsers(username):
    profileImageForm = UpdateProfilePictureForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.followed_posts().all()
    aquariumList = user.aquariums.all()
    if len(aquariumList) == 0:
        return render_template('user.html', user=user, posts=posts, aquariumForm=aquariumForm)
    else:    
        defaultAquarium = aquariumList[0]
        defaultAquariumDataFile = defaultAquarium.data
        defaultAquariumDataOrdered = defaultAquariumDataFile.order_by(AquariumData.timestamp.desc()).first()
        return render_template('followedUsers.html', user=user, posts=posts, aquariumList=aquariumList, defaultAquarium=defaultAquarium, 
            defaultAquariumDataOrdered=defaultAquariumDataOrdered,profileImageForm=profileImageForm)

@app.route('/user/<username>/addAquarium')
@login_required
def addAquarium(username):
    profileImageForm = UpdateProfilePictureForm()
    user = User.query.filter_by(username=username).first_or_404()
    aquariumForm = CreateAquariumForm()
    aquariumList = user.aquariums.all()
    addAquariumCheck = True
    return render_template('user.html', user=user, aquariumForm=aquariumForm, 
        addAquariumCheck=addAquariumCheck, aquariumList=aquariumList, profileImageForm=profileImageForm)


@app.route('/followUser/<username>')
@login_required
def followUser(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('newsfeed', username=username))
    if user == current_user:
        return redirect(url_for('newsfeed', username=username))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('newsfeed', username=current_user.username))

@app.route('/unfollowUser/<username>')
@login_required
def unfollowUser(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('newsfeed', username=username))
    if user == current_user:
        return redirect(url_for('newsfeed', username=username))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('newsfeed', username=current_user.username))

@app.route('/deletePost/<post>')
@login_required
def deletePost(post):
    post = Post.query.filter_by(author=current_user).filter_by(id=int(post)).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('newsfeed', username=current_user.username))

@app.route('/deleteAquarium/<aquarium>')
@login_required
def deleteAquarium(aquarium):
    aqua = Aquarium.query.filter_by(userAquarium=current_user).filter_by(id=int(aquarium)).first()
    db.session.delete(aqua)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))

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
            'ph': a.first().ph,
            'filterFlow' : a.first().filterFlow,
            'clarity' : a.first().waterClarity
        }
        jsonFile[aquariums.name] = dict
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
            'ph': a.first().ph,
            'filterFlow' : a.first().filterFlow,
            'clarity' : a.first().waterClarity
        }
        jsonFile[aquariums.name] = dict
    emit('returnAnalysisData', jsonFile
    )
