from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import pytz
import json
import os

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

class FormHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_FORM.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('404 Страница не найдена'.encode('utf-8'))

    def do_POST(self):
        if self.path == '/submit':
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            data = parse_qs(post_data)
            
            login = data['login'][0]
            client_time = data['current_time'][0]

            record = {
                'login': login,
                'client_time': client_time,
                'server_time': datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%y %H:%M:%S')
            }
  
            os.makedirs('data', exist_ok=True)
    
            with open('data/submissions.json', 'a') as f:
                json.dump(record, f, ensure_ascii=False)
                f.write('\n')
 
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response = f"""
                <h1>Данные успешно сохранены!</h1>
                <p>Логин: {login}</p>
                <p>Время: {client_time}</p>
                <a href="/">Вернуться к форме</a>
            """
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('404 Страница не найдена'.encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), FormHandler)
    print('Сервер запущен на http://localhost:8080')
    server.serve_forever()