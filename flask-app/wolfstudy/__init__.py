from contextlib import closing
from flask import Flask, g, redirect, render_template, request, url_for

import config
import sqlite3

# Create and configure Flask object
app = Flask(__name__)
app.config.from_object(config)

# +------------+
# |  DATABASE  |
# +------------+

def connect_db():
    """Connect to the database specified in app.config."""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """Create and set up the database specified in app.config."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            schema_script = f.read()
            db.cursor().executescript(schema_script)
        db.commit()

@app.before_request
def before_request():
    # Open a connection to the database and store it in g.
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    # Close the database connection.
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def db_add_question(title, content):
    """Add a question with the specified title and content to the database."""
    cursor = g.db.cursor()

    cursor.execute('INSERT INTO questions (title, content) VALUES (?, ?)', [title, content])
    cursor.execute('SELECT last_insert_rowid()')

    new_question_id = cursor.fetchone()[0]
    g.db.commit()

    return new_question_id

def db_get_question(question_id):
    """Retrieve and return a question with the specified question id from the database."""
    cursor = g.db.cursor()
    cursor.execute('SELECT title, content FROM questions WHERE id == ?', [question_id])
    return cursor.fetchone()

def db_get_all_questions():
    """Retrieve and return a list of all questions from the database."""
    cursor = g.db.cursor()
    cursor.execute('SELECT title, content, id FROM questions')
    questions = [{'title': row[0], 'content': row[1], 'id': row[2]} for row in cursor.fetchall()]
    return questions

def db_add_answer(question_id, content):
    """Add an answer to the database with an associated question id and text content."""
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO answers (question_id, content) VALUES (?, ?)', [question_id, content])
    g.db.commit()

def db_get_answers(question_id):
    """Return a list of answers associated with the specified question id."""
    cursor = g.db.cursor()
    cursor.execute('SELECT (content) FROM answers WHERE question_id == ?', [question_id])
    answers = [answer[0] for answer in cursor.fetchall()]
    print(answers)
    return answers

# +----------+
# |  ROUTES  |
# +----------+
#
# /, /feed - GET: question feed
# /question/<question_id> - GET: question page
# /question/<question_id>/answer - POST: process answer
# /ask - GET: ask question page
# /ask - POST: process new question

@app.route('/')
@app.route('/feed/')
def feed():
    questions = db_get_all_questions()
    return render_template('feed.html', questions=questions)

@app.route('/question/<int:question_id>/')
def get_question(question_id):
    title, content = db_get_question(question_id)
    answers = db_get_answers(question_id)
    return render_template('question.html', title=title, content=content, question_id=question_id, answers=answers)

@app.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    db_add_answer(question_id, request.form['content'])
    return redirect(url_for('get_question', question_id=question_id))
    #return 'Posting new answer. question_id: %d, content: %s' % (question_id, request.form['content'])


@app.route('/ask/', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'GET':
        return render_template('ask.html')

    elif request.method == 'POST':
        new_question_id = db_add_question(request.form['title'], request.form['content'])
        return redirect(url_for('get_question', question_id=new_question_id))

