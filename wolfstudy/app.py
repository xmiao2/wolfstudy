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
    return render_template('feed.html')

@app.route('/question/<int:question_id>/')
def get_question(question_id):
    title, content = db_get_question(question_id)
    return render_template('question.html', title=title, content=content)

@app.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    return 'Posting new answer for question %d.' % question_id

@app.route('/ask/', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'GET':
        return render_template('ask.html')

    elif request.method == 'POST':
        new_question_id = db_add_question(request.form['title'], request.form['content'])
        return redirect(url_for('get_question', question_id=new_question_id))

if __name__ == '__main__':
    app.run()
