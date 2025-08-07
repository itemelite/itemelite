import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Basic configuration
UPLOAD_FOLDER = 'static/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB upload limit

@app.route('/')
def index():
    video_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    videos = []
    if os.path.exists(video_folder):
        # Sort videos by modification time, newest first
        video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]
        video_files.sort(key=lambda x: os.path.getmtime(os.path.join(video_folder, x)), reverse=True)
        videos = video_files
    return render_template('index.html', videos=videos)

@app.route('/upload-form')
def upload_form():
    return render_template('upload.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        # Correct the path to be relative to the app's root
        file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Make sure the upload folder exists
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    app.run(debug=True, host='0.0.0.0', port=8080)
