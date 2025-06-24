from flask import Flask, request, render_template_string
from datetime import datetime
import pytz
import json
import os

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Форма Moodle</title>
    <script>
        function updateTime() {
            const now = new Date();
            const timeStr = now.toLocaleString('ru-RU', {
                timeZone: 'Europe/Moscow',
                day: '2-digit',
                month: '2-digit',
                year: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            document.getElementById('current_time').value = timeStr;
        }
        setInterval(updateTime, 1000);
        window.onload = updateTime;
    </script>
</head>
<body>
    <h1>Форма для отправки данных</h1>
    <form method="POST" action="/submit">
        <label for="login">Логин в Moodle:</label>
        <input type="text" id="login" name="login" required><br><br>
        
        <label for="current_time">Текущее время (МСК):</label>
        <input type="text" id="current_time" name="current_time" readonly><br><br>
        
        <button type="submit">Отправить</button>
    </form>
</body>
</html>
"""

@app.route('/')
def show_form():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def handle_submit():
    login = request.form['login']
    client_time = request.form['current_time']
    
    data = {
        'login': login,
        'client_time': client_time,
        'server_time': datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%y %H:%M:%S')
    }
    
    os.makedirs('data', exist_ok=True)
    
    with open('data/submissions.json', 'a') as f:
        json.dump(data, f, ensure_ascii=False)
        f.write('\n')
    
    return f"""
        <h1>Данные успешно сохранены!</h1>
        <p>Логин: {login}</p>
        <p>Время: {client_time}</p>
        <a href="/">Вернуться к форме</a>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)