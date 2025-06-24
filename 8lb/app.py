from flask import Flask, request, jsonify, render_template_string
from PIL import Image
from io import BytesIO

app = Flask(__name__)
last_image_info = {"width": None, "height": None, "image_url": None}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Size Checker</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        #result { margin-top: 20px; }
        #preview { max-width: 100%; margin-top: 10px; display: none; }
    </style>
</head>
<body>
    <h1>Upload PNG Image</h1>
    <form id="uploadForm">
        <input type="file" name="image" accept="image/png" required>
        <button type="submit">Get Size</button>
    </form>
    
    <div id="result"></div>
    <img id="preview" src="" alt="Image preview">
    
    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            formData.append('image', e.target.image.files[0]);
            
            try {
                const response = await fetch('/size2json', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.width && data.height) {
                    document.getElementById('result').innerHTML = `
                        <h3>Image Size:</h3>
                        <p>Width: ${data.width}px</p>
                        <p>Height: ${data.height}px</p>
                    `;
                    
                    // Show preview
                    const preview = document.getElementById('preview');
                    preview.src = URL.createObjectURL(e.target.image.files[0]);
                    preview.style.display = 'block';
                    
                    // Get last uploaded image info
                    fetch('/last_image').then(r => r.json()).then(console.log);
                } else {
                    document.getElementById('result').innerHTML = `
                        <p style="color: red;">Error: ${data.result || 'Unknown error'}</p>
                    `;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `
                    <p style="color: red;">Error: ${error.message}</p>
                `;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['GET'])
def login():
    return jsonify({"author": "1149886"})

@app.route('/size2json', methods=['POST'])
def size2json():
    if 'image' not in request.files:
        return jsonify({"result": "no file uploaded"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"result": "no selected file"}), 400
    
    try:
        img = Image.open(BytesIO(file.read()))
        if img.format != 'PNG':
            return jsonify({"result": "invalid filetype"}), 400
        
        # Save last image info
        last_image_info.update({
            "width": img.width,
            "height": img.height,
            "image_url": f"data:image/png;base64,{file.stream.read().hex()}"
        })
        
        return jsonify({
            "width": img.width,
            "height": img.height
        })
    except Exception as e:
        return jsonify({"result": "invalid filetype"}), 400

@app.route('/last_image', methods=['GET'])
def last_image():
    return jsonify(last_image_info)

if __name__ == '__main__':
    app.run(debug=True)