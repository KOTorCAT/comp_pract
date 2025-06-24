from flask import Flask, request, jsonify, render_template_string, make_response
from PIL import Image, ImageDraw, ImageFont
import io
import os
import uuid

app = Flask(__name__)

# Конфигурация
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        .error { color: red; }
        #imagePreview { max-width: 100%; margin-top: 20px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Image Generator</h1>
    <form id="imageForm">
        <div>
            <label>Width (px): <input type="number" name="width" min="1" max="2000" value="300" required></label>
        </div>
        <div>
            <label>Height (px): <input type="number" name="height" min="1" max="2000" value="200" required></label>
        </div>
        <div>
            <label>Text: <input type="text" name="text" value="Hello"></label>
        </div>
        <button type="submit">Generate</button>
    </form>
    
    <div id="result">
        <img id="imagePreview" style="display: none;">
    </div>

    <script>
        document.getElementById('imageForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new URLSearchParams(new FormData(e.target));
            
            try {
                const response = await fetch('/makeimage', {
                    method: 'POST',
                    body: formData,
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const img = document.getElementById('imagePreview');
                    img.src = URL.createObjectURL(blob);
                    img.style.display = 'block';
                } else {
                    const error = await response.text();
                    alert(`Error: ${error}`);
                }
            } catch (err) {
                alert(`Network error: ${err.message}`);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login')
def login():
    return jsonify({"author": "1149886"})

@app.route('/makeimage', methods=['POST'])
def make_image():
    try:
        # Получаем параметры
        width = int(request.form['width'])
        height = int(request.form['height'])
        text = request.form.get('text', 'Hello')
        
        # Валидация
        if not (1 <= width <= 2000 and 1 <= height <= 2000):
            return "Invalid size (1-2000px)", 400
        
        # Создаём изображение
        img = Image.new('RGB', (width, height), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", size=min(width, height)//5)
        except:
            font = ImageFont.load_default()
        
        # Совместимость с Pillow 9.0.0+
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Рисуем текст по центру (ИСПРАВЛЕННАЯ СТРОКА)
        draw.text(
            ((width - text_width)/2, (height - text_height)/2),
            text, 
            font=font, 
            fill=(255, 255, 255))
        
        # Сохраняем в буфер
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG', quality=90)
        img_io.seek(0)
        
        # Отправляем изображение
        response = make_response(img_io.read())
        response.headers.set('Content-Type', 'image/jpeg')
        return response
        
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)