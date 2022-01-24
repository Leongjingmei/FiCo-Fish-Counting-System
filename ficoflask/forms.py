from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from ficoflask.models import User

class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators = [DataRequired(), Length(min=3,max=20)])
    email = StringField(label="Email", validators = [DataRequired(), Email()])
    password = PasswordField(label="Password", validators = [DataRequired(), Length(min=6,max=16)])
    confirm_password = PasswordField(label="Confirm Password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Sign Up")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators = [DataRequired(), Length(min=3,max=50)])
    password = PasswordField(label="Password", validators = [DataRequired(), Length(min=6,max=16)])
    submit = SubmitField(label="Login")

class AccountUpdateForm(FlaskForm):
    picture = FileField(label="Update Profile Picture: ", validators = [FileAllowed(['jpg','png'])])
    username = StringField(label="Username", validators = [DataRequired(), Length(min=3,max=20)])
    email = StringField(label="Email", validators = [DataRequired(), Email()])
    firstname =StringField(label="First Name", validators = [DataRequired(), Length(min=3,max=20)])
    lastname = StringField(label="Last Name", validators = [DataRequired(), Length(min=3,max=20)])
    submit = SubmitField(label="Update")

class UploadImageForm(FlaskForm):
    upload_image = FileField(label="Upload Image: ", validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField(label="Calculate Now")

class TakePhotoForm(FlaskForm):
    picture = FileField(label="Upload Image: ", validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField(label="Calculate")
