from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import statistics
from datetime import datetime, timedelta


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    aquariums = db.relationship('Aquarium', backref='userAquarium', lazy='dynamic')
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)

    def readDate(self):
        return self.timestamp.strftime('%x')
    
    def readTime(self):
        return self.timestamp.strftime('%X')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment {}>, Linked Post {}'.format(self.body, self.post_id)

class Aquarium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    data = db.relationship('AquariumData', backref='linkedAquarium', lazy='dynamic')
    targetTemperature = db.Column(db.Integer)
    targetPH = db.Column(db.Integer)
    targetWaterflow = db.Column(db.Integer)
    targetClarity = db.Column(db.Integer)

    #
    #functions for returning averages for analysis
    #
    def dayAverage(self, value, param):
        list = []
        try:
            for d in self.data:
                if d.timestamp.strftime('%x') == value and param == 'ph':
                    list.append(int(d.ph))
                elif d.timestamp.strftime('%x') == value and param == 'temp':
                    list.append(int(d.temperature))
                elif d.timestamp.strftime('%x') == value and param == 'flow':
                    list.append(int(d.filterFlow))
                elif d.timestamp.strftime('%x') == value and param == 'clarity':
                    list.append(int(d.waterClarity))
            mean = (statistics.mean(list))
            return mean
        except:
            pass
            return 0

    def monthAverage(self, value, param):
        list = []
        try:
            for d in self.data:
                if d.timestamp.month == value and param == 'ph':
                    list.append(int(d.ph))
                elif d.timestamp.month == value and param == 'temp':
                    list.append(int(d.temperature))
                elif d.timestamp.month == value and param == 'flow':
                    list.append(int(d.filterFlow))
                elif d.timestamp.month == value and param == 'clarity':
                    list.append(int(d.waterClarity))
            mean = (statistics.mean(list))
            return mean
        except:
            pass
            #print("An exception occurred")
            return 0

    #dataType should be temp,ph,waterflow,clarity 
    def weekChartData(self, *args):
        jsonFile = {"ph":{"Sunday":0,"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0},
            "temp":{"Sunday":0,"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0},
            "flow":{"Sunday":0,"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0},
            "clarity":{"Sunday":0,"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0}}
        for dataType in args:
            x = 0
            day = datetime.now()
            if day.strftime('%w') == '1':
                jsonFile[dataType][day.strftime('%A')] = self.dayAverage(day.strftime('%x'), dataType)
            else:
                while day.strftime('%w') != '1':
                    day = datetime.now() - timedelta(x)
                    jsonFile[dataType][day.strftime('%A')] = self.dayAverage(day.strftime('%x'), dataType)
                    x += 1
        return(jsonFile)

    def monthChartData(self, *args):
        jsonFile = {
            "ph": {},
            "temp": {},
            "flow": {},
            "clarity": {}
            }
        for dataType in args:
            x = 0
            day = datetime.now()
            if day.strftime('%d') == '01':
                jsonFile[dataType][int(day.strftime('%d'))] = self.dayAverage(day.strftime('%x'), dataType)
            else:
                while day.strftime('%d') != '01':
                    day = datetime.now() - timedelta(x)
                    jsonFile[dataType][int(day.strftime('%d'))] = self.dayAverage(day.strftime('%x'), dataType)
                    x += 1
        return(jsonFile)

    def yearChartData(self, *args):
        jsonFile = {"ph":{"January":0,"February":0,"March":0,"April":0,"May":0,"June":0,"July":0,"August":0,"September":0,"October":0,"November":0,"December":0},
            "temp":{"January":0,"February":0,"March":0,"April":0,"May":0,"June":0,"July":0,"August":0,"September":0,"October":0,"November":0,"December":0},
            "flow":{"January":0,"February":0,"March":0,"April":0,"May":0,"June":0,"July":0,"August":0,"September":0,"October":0,"November":0,"December":0},
            "clarity":{"January":0,"February":0,"March":0,"April":0,"May":0,"June":0,"July":0,"August":0,"September":0,"October":0,"November":0,"December":0}}
        for dataType in args:
            for x in range(1,13):
                date = datetime(2020, x, 1)
                jsonFile[dataType][date.strftime('%B')] = self.monthAverage(x, dataType)
        return(jsonFile)

    def __repr__(self):
        return '<Aquarium {}, Owner {}>'.format(self.name, self.userAquarium.username)

class AquariumData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    temperature = db.Column(db.Integer)
    ph = db.Column(db.Integer)
    filterFlow = db.Column(db.Integer)
    waterClarity = db.Column(db.Integer)
    aquarium_id = db.Column(db.Integer, db.ForeignKey('aquarium.id'))

    def filterFlowPercentage(self):
        manuFlowRate = self.linkedAquarium.targetWaterflow
        percentage = (self.filterFlow/manuFlowRate)*100
        return "{0:.0%}".format(percentage)

    def waterClarityPercentage(self):
        waterList = [2.79,2.71,2.51,2.54,2.7,2.64]
        clearwater = 4.27
        dirtyWaterMean = statistics.mean(waterList)
        if self.waterClarity >=4.27:
            return 100
        else:
            differencePercentage = ((clearwater-self.waterClarity)/((clearwater+self.waterClarity)/2))
            return differencePercentage

    def time(self):
        return self.timestamp

    def __repr__(self):
        return '<aquarium {}>'.format(self.linkedAquarium.name)
        #return '<aquarium {}>'.format(self.timestamp)
