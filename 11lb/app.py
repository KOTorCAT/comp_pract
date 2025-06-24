from flask import Flask, request, jsonify, render_template_string
from cryptography.fernet import Fernet
import base64
import sys

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Decryption Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        textarea {
            width: 100%;
            min-height: 100px;
            margin: 10px 0;
        }
        button {
            padding: 10px 15px;
            background: #0066cc;
            color: white;
            border: none;
            cursor: pointer;
        }
        #result {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>Decryption Tool</h1>
    <form id="decryptForm">
        <div>
            <label>Private Key:</label><br>
            <textarea name="key" required></textarea>
        </div>
        <div>
            <label>Encrypted Message:</label><br>
            <textarea name="secret" required></textarea>
        </div>
        <button type="submit">Decrypt</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('decryptForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/decypher', {
                    method: 'POST',
                    body: formData
                });
                
                const resultDiv = document.getElementById('result');
                if (response.ok) {
                    resultDiv.innerHTML = `<strong>Decrypted:</strong><br>${await response.text()}`;
                } else {
                    resultDiv.innerHTML = `<strong>Error:</strong><br>${await response.text()}`;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `<strong>Network Error:</strong><br>${error.message}`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/login')
def login():
    return jsonify({"author": "1149886"})

@app.route('/decypher', methods=['POST'])
def decypher():
    try:
        key = request.form['key'].encode()
        secret = request.form['secret'].encode()
        
        # Prepare key (32 bytes required)
        key = base64.urlsafe_b64encode(key.ljust(32)[:32])
        fernet = Fernet(key)
        
        return fernet.decrypt(secret).decode()
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
        print(f"Starting server on http://localhost:{port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"Failed to start server: {e}")