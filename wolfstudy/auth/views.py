from flask import flash, redirect, render_template, request, session, url_for
from flask.ext.login import login_required, login_user, logout_user
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
            flash(error)
            return render_template('auth/register.html', form=form)

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

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
        
        if user != None and user.verify_password(password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Login failed. Please try again.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')

    return redirect(url_for('main.index'))
