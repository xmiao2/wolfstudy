from flask import flash, redirect, render_template, request, session, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user
from . import auth
from .. import db
from .forms import LoginForm, RegisterForm
from ..email import send_email
from ..models import User

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm/')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your WolfStudy account',
            'auth/mail/confirm_email', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        token = new_user.generate_confirmation_token()
        send_email(new_user.email, 'Confirm your WolfStudy account',
                'auth/mail/confirm_email', user=new_user, token=token)

        login_user(new_user)

        return redirect(url_for('auth.unconfirmed'))
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

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link you provided is either invalid or expired. Please try again.')
    return redirect(url_for('main.index'))
