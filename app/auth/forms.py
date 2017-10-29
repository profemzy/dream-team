from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Member


class RegistrationForm(FlaskForm):
    """
     Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self,email):
        if Member.query.filter_by(email=email.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, username):
        if Member.query.filter_by(username=username.data).first():
            raise ValidationError('Username is already in use')


class LoginForm(FlaskForm):
    """
    Form to login users
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
