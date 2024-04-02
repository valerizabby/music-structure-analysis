import logging
import os
from flask import Flask, flash, request, redirect, url_for, render_template
import logging as log

from utils.secure_filename import secure_filename
from utils.is_file_allowed import is_file_allowed
from utils.read_file_as_string import read_file_as_string

from service.apply_figure import apply_figure_ssm, apply_figure

log.basicConfig(level=logging.INFO)


UPLOAD_FOLDER = 'app/data/upload_files_from_localhost'
HTML_PAGE_FOR_UPLOADING_FILE = 'app/resources/html/uploadFilePage.html'
HTML_PAGE_WITH_RESULT_IMAGE = 'ssmPic.html'
SSM_FIGURES = 'figures-produced-by-figure-ssm'

app = Flask(__name__)

img = os.path.join('app/static', 'Image')

app.config['HTML_PAGE_FOR_UPLOADING_FILE'] = HTML_PAGE_FOR_UPLOADING_FILE
app.config['HTML_PAGE_WITH_RESULT_IMAGE'] = HTML_PAGE_WITH_RESULT_IMAGE
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SSM_FIGURES'] = SSM_FIGURES


@app.route('/')
def index():
    return os.getcwd()
    #return sys.path



# @app.route('/')
# @app.route('/figure')
# def show_figure():
#     full_filename = url_for('static', filename='Image/JPG-File.jpg')
#     return render_template(app.config['HTML_PAGE_WITH_RESULT_IMAGE'], image=full_filename)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and is_file_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            log.info(f"File {filename} saved to {app.config['UPLOAD_FOLDER']}!")

            # TODO сделать тумблер между картинками
            result_filename = apply_figure_ssm(app.config['UPLOAD_FOLDER'] + "/" + filename)
            #result_filename = apply_figure(app.config['UPLOAD_FOLDER'] + "/" + filename)

            return render_template(app.config['HTML_PAGE_WITH_RESULT_IMAGE'], image=result_filename)

    return read_file_as_string(app.config['HTML_PAGE_FOR_UPLOADING_FILE'])


if __name__ == '__main__':
    app.run(port=5002, debug=True)
