from flask import g

#####################
##    Questions    ##
#####################

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

###################
##    Answers    ##
###################

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
    return answers

#################
##    Users    ##
#################

def db_add_user(username, email, iterations, salt, pass_hash):
    """Add a user to the database including email, username, hash iterations, salt, and password hash."""
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO users (username, email, iterations, salt, pass_hash) VALUES (?, ?, ?, ?, ?)',
                                      [username, email, iterations, salt, pass_hash])
    g.db.commit()

def db_email_exists(email):
    """Return whether the specified email address is in the users table."""
    cursor = g.db.cursor()
    cursor.execute('SELECT (email) FROM users WHERE email == ? LIMIT 1', [email])
    return cursor.fetchone() != None

def db_username_exists(username):
    """Return whether the specified username is in the users table."""
    cursor = g.db.cursor()
    cursor.execute('SELECT (username) FROM users WHERE username == ? LIMIT 1', [username])
    return cursor.fetchone() != None
