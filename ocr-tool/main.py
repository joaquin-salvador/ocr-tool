from flask import Flask, request, render_template, redirect, url_for, send_from_directory, send_file
import pandas as pd
from werkzeug.utils import secure_filename
import cv2
import pytesseract
import joblib
import shutil
import zipfile
import tempfile
import os
import sys
from joblib import load

# Function to get the correct file path whether the script is bundled or not
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Specify the path to the Tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Update this path to where Tesseract is installed on Fedora
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def process_file(file_path):
    image = cv2.imread(file_path)
    ocr_result = pytesseract.image_to_string(image)

    print(ocr_result)

    return ocr_result


def handle_files(files, batch_processing=False):
    results = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            ocr_result = process_file(file_path)
            results.append({
                'filename': filename,
                'ocr_result': ocr_result,
            })
    if batch_processing:
        return results, file_path
    return results


def save_results_to_csv(results, csv_path):
    df = pd.DataFrame(results)
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode='a', header=False, index=False)


def get_existing_results(csv_path):
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        try:
            df = pd.read_csv(csv_path)
            return df.to_dict(orient='records')
        except pd.errors.EmptyDataError:
            return []
    return []


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        results = handle_files(files)
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
        save_results_to_csv(results, csv_path)
        return redirect(url_for('upload_file'))
    else:
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
        results = get_existing_results(csv_path)
        sort_option = request.args.get('sort')
        if sort_option == 'alphabetical':
            results.sort(key=lambda x: x['filename'])
        return render_template('index.html', results=results)

@app.route('/download')
def download_file():
    uploads_path = resource_path(app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads_path, 'results.csv', as_attachment=True)

@app.route('/delete', methods=['POST'])
def delete_files():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    return redirect(url_for('upload_file'))


@app.route('/batch-upload', methods=['POST'])
def batch_upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename, ['zip']):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, secure_filename(file.filename))
            file.save(zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            results, _ = handle_files([open(os.path.join(temp_dir, f), 'rb') for f in os.listdir(temp_dir) if
                                       allowed_file(f, ['jpg', 'jpeg', 'png'])], batch_processing=True)
            csv_path = os.path.join(temp_dir, 'results.csv')
            save_results_to_csv(results, csv_path)
            return send_file(csv_path, as_attachment=True, attachment_filename='batch_results.csv')


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def main():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)


if __name__ == '__main__':
    main()
