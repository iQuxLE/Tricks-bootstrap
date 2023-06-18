# Dieser Code erstellt eine Webseite mit Flask, die es Usern ermöglicht, Dateien hochzuladen.

# Zuerst importiert er einige Funktionen von Flask und Werkzeug, die benötigt werden, um die Website zu erstellen und Dateien hochzuladen.

# Dann wird ein neues Flask-Objekt erstellt und ein Upload-Ordner festgelegt.

# Dann gibt es drei Routen:

# Die Index-Seite: Hier wird "index.html" gerendert, was bedeutet, dass sie auf der Seite angezeigt wird.
# Die Upload-Seite: Hier kann der User die Datei auswählen, die er hochladen möchte. Wenn keine Datei zum Hochladen ausgewählt wurde, wird eine Fehlermeldung ausgegeben. Wenn alles in Ordnung ist, wird die Datei gespeichert.
# Die Uploaded File-Seite: Auf dieser Seite kann der User die hochgeladene Datei ansehen.
# Schließlich gibt es eine Route, die alle hochgeladenen Dateinamen zurückgibt, so dass der User sehen kann, welche Dateien er hochgeladen hat.

from flask import Flask, request, send_from_directory, render_template, redirect
from werkzeug.utils import secure_filename
import logging
import json

logging.basicConfig(level=logging.INFO)


# initialisiere Flask und den Upload-Ordner als globale Variablen (d.h. sind in jeder Funktion verfügbar, ohne sie explizit als Parameter übergeben zu müssen)
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask import render_template
import glob

import os

def get_latest_file():
    logging.info('Getting latest file...')
    # Get a list of all files in the upload folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    logging.info(f'All files: {files}')
    # Filter out any non-video files (this assumes all videos will have .mp4 extension)
    videos = [f for f in files if f.endswith('.mp4')]
    logging.info(f'Video files: {videos}')
    # If there are no videos, return None
    if not videos:
        logging.warning('No video files found.')
        return None
    # Sort the videos by creation time (newest first)
    videos.sort(key=lambda x: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    # Return the newest video
    logging.info(f'Latest video file: {videos[0]}')
    return videos[0]

@app.route('/')
def home():
    latest_file = get_latest_file()
    return render_template('base.html', latest_file=latest_file)


# # erstellt die Route ('/') für die Index-Seite
# @app.route('/')
# def base():
#     video_folder = os.path.join('static', 'uploads')
#     video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]
#     video_files = [os.path.join(video_folder, f) for f in video_files]  # add the full path
#     return render_template('base.html')

# erstellt die Route ('/upload') für die Upload-Seite
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file has been uploaded
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # Check if a file was selected
        if file.filename == '':
            return 'No selected file'
        # Save the file in the upload folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    else:
        # This handles the GET request, which could render a template or return some text.
        return "Upload page"

# erstellt die Route ('/uploads/<filename>') für die Uploaded File-Seite
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# erstellt die Route ('/uploads') für die Liste der hochgeladenen Dateien
@app.route('/uploads')
def get_uploaded_files():
    # listet alle Dateien im Upload-Ordner auf
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return json.dumps(filenames)

# startet die App
if __name__ == "__main__":
    app.run(debug=True)
