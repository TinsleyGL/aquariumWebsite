from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from app import images

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    userLogin = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateAquariumForm(FlaskForm):
    aquariumName = StringField('Aquarium Name', validators=[DataRequired()])
    targetTemp = StringField('Regular Temperature',validators=[DataRequired()])
    targetPH = StringField('Regular PH', validators=[DataRequired()])
    targetWaterflow = StringField('Filter Flow Rate ', validators=[DataRequired()])
    createAquarium = SubmitField('Create Aquarium')

class CreatePostForm(FlaskForm):
    aquariumTag = StringField('Aquarium')
    postBody = StringField("What's on your mind?", validators=[DataRequired()])
    aquariumImage = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    createPost = SubmitField('Post')

class CreateImagePostForm(FlaskForm):
    aquariumTag = StringField('Aquarium')
    postBody = StringField("What's on your mind?", validators=[DataRequired()])
    createPost = SubmitField('Post Image')


