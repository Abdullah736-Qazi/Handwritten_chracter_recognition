from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import os

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            
            img = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(img)

            return render_template('index.html', extracted_text=extracted_text, image_file=file.filename)

    return render_template('index.html', extracted_text=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
