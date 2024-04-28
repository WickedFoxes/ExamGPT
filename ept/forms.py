from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('subject', validators=[DataRequired()])
    fileContent = FileField('fileContent')

class UserCreateForm(FlaskForm):
    username = StringField('Nickname Error', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('Password Error', validators=[
        DataRequired(), EqualTo('password2', 'Passwords do not match.')])
    password2 = PasswordField('Password Error', validators=[DataRequired()])
    email = EmailField('Email Error', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField("Nickname Error", validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password Error', validators=[DataRequired()])
