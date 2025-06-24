from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import pytz

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(tz).strftime('%d.%m.%y %H:%M:%S')
        response = f"149886, {current_time}"
        self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
    print('Сервер запущен на порту 8080')
    httpd.serve_forever()