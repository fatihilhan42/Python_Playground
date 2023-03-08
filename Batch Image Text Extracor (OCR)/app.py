from flask import Flask, request, send_file, redirect, url_for
import os
import tesserocr
import zipfile
from PIL import Image

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'zip'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path, lang='tur'):
    with Image.open(image_path) as image:
        return tesserocr.image_to_text(image, lang=lang)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'folder' not in request.files:
            return redirect(request.url)
        uploaded_folder = request.files['folder']
        if not allowed_file(uploaded_folder.filename):
            return redirect(request.url)
        try:
            os.makedirs('temp', exist_ok=True)
            uploaded_folder.save(os.path.join('temp', 'uploaded_folder.zip'))
            with zipfile.ZipFile(os.path.join('temp', 'uploaded_folder.zip'), 'r') as zip_ref:
                extracted_text = {}
                for file_name in zip_ref.namelist():
                    if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        continue
                    with zip_ref.open(file_name) as image_file:
                        with Image.open(image_file) as image:
                            if image.mode not in ('L', 'RGB'):
                                image = image.convert('RGB')
                            text = tesserocr.image_to_text(image, lang='tur')
                            extracted_text[os.path.basename(file_name)] = text
            if extracted_text:
                with zipfile.ZipFile('extracted_text.zip', 'w') as zip_file:
                    for file_name, text in extracted_text.items():
                        zip_file.writestr(f'{file_name}.txt', text)
                return send_file('extracted_text.zip', as_attachment=True)
            return 'No images with text found.'
        except Exception as e:
            return f'Error: {str(e)}'
        finally:
            for file in os.listdir('temp'):
                os.remove(os.path.join('temp', file))
    else:
        return '''
        <style>
        .exit-button {
            background-color: red;
            color: white;
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        </style>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="folder" accept=".zip" />
            <input type="submit" value="Upload and download extracted text" />
        </form>
        <br>
        <button class="exit-button" onclick="window.close()">Exit</button>
        '''

if __name__ == '__main__':
    app.run()
