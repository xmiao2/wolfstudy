from flask import abort, flash, redirect, render_template, request, session, url_for
from . import main
from .. import db
from .forms import AnswerQuestionForm, AskQuestionForm, LoginForm, RegisterForm
from ..models import Answer, Question, User

@main.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@main.route('/question/<int:question_id>/')
def get_question(question_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    answers = question.answers
    form = AnswerQuestionForm()
    return render_template('question.html', question=question, answers=answers, form=form)

@main.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    if not session.get('logged_in', False):
        print "not logged in"
        flash('You must be logged in to answer a question.')
        return redirect(url_for('.login'))

    form = AnswerQuestionForm()
    if form.validate_on_submit():
        question = Question.query.filter_by(id=question_id).first_or_404()
        content = form.content.data
        new_answer = Answer(content, question)

        db.session.add(new_answer)
        db.session.commit()

        return redirect(url_for('.get_question', question_id=question.id))
    else:
        question = Question.query.filter_by(id=question_id).first_or_404()
        answers = question.answers
        return render_template('question.html', question=question, answers = answers, form=form)

@main.route('/ask/', methods=['GET', 'POST'])
def ask_question():
    if not session.get('logged_in', False):
        flash('You must be logged in to ask a question.')
        return redirect(url_for('.login'))

    form = AskQuestionForm()
    if form.validate_on_submit():
        new_question = Question(form.title.data, form.content.data)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('.get_question', question_id=new_question.id))
    else:
        return render_template('ask.html', form=form)

@main.route('/register/', methods=['GET', 'POST'])
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
            return render_template('register.html', error=error)

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('.index'))
    else:
        return render_template('register.html', form=form)

@main.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        
        if user == None or not user.verify_password(password):
            error = 'Login failed. Please try again.'
            return render_template('login.html', form=form, error=error)

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('.index'))
    else:
        return render_template('login.html', form=form)

@main.route('/logout/')
def logout():
    session['logged_in'] = False
    session.pop('username')

    return redirect(url_for('.index'))

@main.route('/user/<username>/')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
