from flask import redirect, render_template, session, url_for
from . import auth
from .. import db
from .forms import LoginForm, RegisterForm
from ..models import User

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        password_retype = form.password_retype.data

        error = None
        if User.query.filter_by(username=username).first() != None:
            error = 'Username already in use.'
        elif User.query.filter_by(email=email).first() != None:
            error = 'Email address already in use.'
        elif password != password_retype:
            error = 'The passwords you typed did not match.'

        if error:
            return render_template('auth/register.html', error=error)

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('main.index'))
    else:
        return render_template('auth/register.html', form=form)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        
        if user == None or not user.verify_password(password):
            error = 'Login failed. Please try again.'
            return render_template('auth/login.html', form=form, error=error)

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('main.index'))
    else:
        return render_template('auth/login.html', form=form)

@auth.route('/logout/')
def logout():
    session['logged_in'] = False
    session.pop('username')

    return redirect(url_for('main.index'))
