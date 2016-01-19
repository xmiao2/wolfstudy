from flask import g

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
