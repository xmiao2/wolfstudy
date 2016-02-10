from flask import redirect, render_template, request, url_for

from wolfstudy import app
import auth
import db

@app.route('/')
@app.route('/feed/')
def feed():
    questions = db.db_get_all_questions()
    return render_template('feed.html', questions=questions)

@app.route('/question/<int:question_id>/')
def get_question(question_id):
    title, content = db.db_get_question(question_id)
    answers = db.db_get_answers(question_id)
    return render_template('question.html', title=title, content=content, question_id=question_id, answers=answers)

@app.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    db.db_add_answer(question_id, request.form['content'])
    return redirect(url_for('get_question', question_id=question_id))

@app.route('/ask/', methods=['GET', 'POST'])
def ask_question():
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
        # Get email, username, and password from form. Convert from Unicode to UTF-8.
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

        # Redirect to homepage
        return redirect(url_for('feed'))

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

        return redirect(url_for('feed'))
