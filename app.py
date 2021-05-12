import os
from flask import Flask,redirect,url_for,render_template,request,flash
from werkzeug.utils import secure_filename
from ocr_ import *


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.secret_key="keerikadan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    return (f'home')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print("h1")
            return render_template('upload.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            print("h2")
            return render_template('upload.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #answer=ocr_fun(filename).replace('\n','<b>')
            answer = ocr_fun(filename).split('\n')
            #print(answer)
            #os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('result.html',answer=answer)
        else:
            flash('select image format')
            return render_template('upload.html')
    else:
        return render_template('upload.html')
    return 






if __name__ == '__main__':
    app.run(debug=True)
