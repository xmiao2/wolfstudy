from flask.ext.wtf import Form
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, Length, Required
from wtforms.fields.html5 import EmailField

class RegisterForm(Form):
    username = StringField('Username', validators=[Required(), Length(min=4, max=30)])
    email = EmailField('Email address', validators=[Required(), Length(min=6, max=320)])
    password = PasswordField('Password', validators=[Required()])
    password_retype = PasswordField('Re-type your password', validators=[Required(), EqualTo('password_retype', message='Passwords must match.')])

    register = SubmitField('Register')

class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(min=4, max=30)])
    password = PasswordField('Password', validators=[Required()])

    log_in = SubmitField('Log In')
