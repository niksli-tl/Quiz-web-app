from flask import session, Flask, redirect, url_for, request
from db_scripts import get_question_after

app = Flask(__name__)

quiz_id = 0
question_id = 0
question = 0


def index():
    global quiz_id, question_id
    if request.method == 'GET':
        return '''<form action="/" method="POST">
                <select name="quiz">
                    <option value="1">quiz 1</option>
                    <option value="2">quiz 2</option>
                    <option value="3">quiz 3</option>
                </select>
                <input type="submit" value="submit">
                <a href="/test">test</a>
                </form>'''
    if request.method == 'POST':
        session['counter'] = 0
        session['quiz'] = request.form.get('quiz')
        question_id = 0
        session['answer'] = 0
        return redirect(url_for('test'))


app.add_url_rule('/', 'index', index, methods=['POST', 'GET'])


def test():
    global question_id, question
    if request.method == 'GET':
        if not session['quiz']:
            return redirect(url_for('index'))
        question = get_question_after(question_id, session['quiz'])
        if not question:
            return redirect(url_for('result'))
        session['counter'] += 1
        question_id += 1
        return f'''<form action="/test" method="POST">
            <p>число вопросов:{session['counter']}</p>
            <p>{question}</p>
            <input type="text" name="answer">
            <a href="/test">следующий вопрос</a>
            </form>'''
    if request.method == 'POST':
        if request.form.get('answer') == question[2]:
            session['answer'] += 1
        return redirect(url_for('test'))


app.add_url_rule('/test', 'test', test, methods=['POST', 'GET'])


def result():
    global quiz_id
    return f"""
        <h1>Викторина завершена!</h1>
        <p>Поздравляем, вы ответили на все вопросы!</p>
        <p>Количесвто правильных ответов:{session['answer']}</p>
        <p><a href="/">Начать новую викторину</a></p>
    """


app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'quiZZZZZ'
if __name__ == "__main__":
    app.run()
