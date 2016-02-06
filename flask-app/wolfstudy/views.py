from flask import redirect, render_template, request, url_for
from wolfstudy import app, db

# /, /feed - GET: question feed
# /question/<question_id> - GET: question page
# /question/<question_id>/answer - POST: process answer
# /ask - GET: ask question page
# /ask - POST: process new question

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
