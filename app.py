from flask import Flask, render_template, request
app = Flask(__name__)

# /, /feed - GET: question feed
# /question/<question_id> - GET: question page
# /question/<question_id>/answer - POST: process answer
# /ask - GET: ask question page
# /ask - POST: process new question

@app.route('/')
@app.route('/feed/')
def feed():
    return render_template("feed.html")

@app.route('/question/<int:question_id>/')
def get_question(question_id):
    return render_template("question.html")

@app.route('/question/<int:question_id>/answer/', methods=['POST'])
def answer_question(question_id):
    return 'Posting new answer for question %d.' % question_id

@app.route('/ask/', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'GET':
        return render_template("ask.html")
    elif request.method == 'POST':
        return 'Submitting a new answer.'

if __name__ == '__main__':
    app.debug = True
    app.run()
