import os
from random import randint
from flask import Flask, session, redirect, url_for
from db_scripts import get_question_after
quiz = 0
last_question = 0

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    q_list = get_quises()
    return render_template('start.html', q_list = q_list)
    
def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form
    else:
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)
        return reirect(url_for('test'))

def save_answer():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if checl_answer(quest_id, answer):
        session['answers'] += 1

def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]

    ]
    shuffle(answers_list)

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        nextquestion = get_question_after(session['last_question'], session['quiz'])
        if next_question if None or len(next_questyion) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

    
def result():
    html = rebder_template('result.html', right = session['answers'], ottal = session['total'])
    end_quiz()
    return html

folder = os.getcwd()
app = Flask(__name__, template_folder = folder, static_folder = folder)
app.add_url_rule('/', 'index', index, methods = ['post', 'get'])
app.add_url_rule('/test', 'test', test, methods = ['post', 'get'])
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretLife'

if __name__ == '__main__':
    app.run()
