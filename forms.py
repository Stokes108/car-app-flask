from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from models import User


class UserRegistrationForm(FlaskForm):
    f_name = StringField('First Name', validators = [DataRequired(), Length(min=2, max=20)])
    l_name = StringField('Last Name', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. PLease choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. PLease choose another one')


class UserLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

