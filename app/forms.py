from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
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
            return False
        else:
            return True

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            return False
        else:
            return True

class CreateAquariumForm(FlaskForm):
    aquariumName = StringField('Aquarium Name', validators=[DataRequired()])
    targetTemp = StringField('Regular Temperature',validators=[DataRequired()])
    targetPH = StringField('Regular PH', validators=[DataRequired()])
    targetWaterflow = StringField('Filter Flow Rate ', validators=[DataRequired()])
    targetClarity = StringField('Water clarity ', validators=[DataRequired()])
    createAquarium = SubmitField('Create Aquarium')

class UpdateAquariumImageForm(FlaskForm):
    aquariumName = StringField('Aquarium Name', validators=[DataRequired()])
    aquariumImage = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    uploadImage = SubmitField('Upload')

class UpdateProfilePictureForm(FlaskForm):
    profileImage = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    uploadImage = SubmitField('Upload')

class CreatePostForm(FlaskForm):
    postBody = StringField("What's on your mind?", validators=[DataRequired()])
    aquariumImage = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    createPost = SubmitField('Post')



