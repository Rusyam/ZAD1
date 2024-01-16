import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foregin_keys = on''')
    

    do('''CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY,
        name VARCHAR)'''
    )


    do('''CREATE TABLE IF NOT EXISTS question(
                id INTEGER PRIMARY KEY,
                question VARCHAR,
                answer VARCHAR,
                wrong1 VARCHAR,
                wrong2 VARCHAR,
                wrong3 VARCHAR)''')        


    do('''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREGIN KEY (quiz_id) REFERENCES quiz (id),
        FOREGIN KEY (question_id) REFERENCES question (id) )''')
    close()


def add_questions():
    questions = [
        ('Сколь месяцев в году имеют 28 дней?', 'все','один','ни одного','два')
        ('Каким станит зеленвц утес, если упадет в красное море?','Мокрым','Красным','Не измениятся','Зеленым')
        ('Какой рукой лучше размешивать чай?', 'Ложкой','Правой','Левой','Ногой')
        ('Что не имеет длинны, глубины, ширины, высоты, а можно измерить?', 'Время','Глупость','Сапоги','Площадь')    
    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?))''', question)
    conn.sommit()
    close()
    

def add_quiz():
    quizes = [
        ('своя игра', ),
        ('кто хочет стать миллионером',),
        ('самый умный',)
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.comit()
    close()


def add_Links():
    open()
    cursor.execute('''PRAGMA foregin_keys = on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input('Добавить связь (y / n)?')
    while answer != 'n':
        quiz_id = int(input('id викторины: '))
        question_id = int(input('id вопроса: '))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input('Добавить связь (y/ n)?')
    close()


def show(table):
    query = 'SELECT * FROM' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')


def get_question_after(question_id = 0, quiz_id = 1):
    '''возвращает следующий вопрос после вопроса с переданным id
    для первоговопроса передается значение по умолчанию '''
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    ND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id'''
    cursor.execute(query, [question_id, quiz_id] )
    result = cursor.fetchone()
    close()
    return result


def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()


if __name__ == '__main__':
    main()