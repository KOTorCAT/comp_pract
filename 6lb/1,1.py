from flask import Flask
from datetime import datetime
import pytz  

app = Flask(__name__)

@app.route('/')
def index():
    tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(tz).strftime('%d.%m.%y %H:%M:%S')
    return f'149886, {current_time}' 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)