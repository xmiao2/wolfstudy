from contextlib import closing
from flask import Flask, render_template, request

import config

# Create and configure Flask object
app = Flask(__name__)
app.config.from_object(config)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            schema_script = f.read()
            db.cursor().executescript(schema_script)
        db.commit()

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
    return render_template('question.html')

@app.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    return 'Posting new answer for question %d.' % question_id

@app.route('/ask/', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'GET':
        return render_template('ask.html')
    elif request.method == 'POST':
        return 'Submitting a new answer.'

if __name__ == '__main__':
    app.run()
