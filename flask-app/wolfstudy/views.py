from flask import flash, redirect, render_template, request, session, url_for

from wolfstudy import app
import auth
import db

@app.route('/')
def index():
    questions = db.db_get_all_questions()
    return render_template('index.html', questions=questions)

@app.route('/question/<int:question_id>/')
def get_question(question_id):
    title, content = db.db_get_question(question_id)
    answers = db.db_get_answers(question_id)
    return render_template('question.html', title=title, content=content, question_id=question_id, answers=answers)

@app.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    if not session['logged_in']:
        flash('You must be logged in to answer a question.')
        return redirect(url_for('login'))

    db.db_add_answer(question_id, request.form['content'])
    return redirect(url_for('get_question', question_id=question_id))

@app.route('/ask/', methods=['GET', 'POST'])
def ask_question():
    if not session['logged_in']:
        flash('You must be logged in to ask a question.')
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('ask.html')

    elif request.method == 'POST':
        new_question_id = db.db_add_question(request.form['title'], request.form['content'])
        return redirect(url_for('get_question', question_id=new_question_id))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        email    = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_retype = request.form['password-retype']

        error = None
        if db.db_username_exists(username):
            error = 'Username already in use.'
        elif db.db_email_exists(email):
            error = 'Email address already in use.'
        elif password != password_retype:
            error = 'The passwords you typed did not match.'

        if error:
            return render_template('register.html', error=error)

        auth.register_user(email, username, password)

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('index'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not auth.is_valid_login(username, password):
            error = 'Login failed. Please try again.'
            return render_template('login.html', error=error)

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('index'))

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    session.pop('username')

    return redirect(url_for('index'))
