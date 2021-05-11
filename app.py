import os
from flask import Flask,redirect,url_for,render_template,request,flash
from werkzeug.utils import secure_filename
from ocr_ import *


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
answer=None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    return (f'home')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global answer
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            print("h1")
            return render_template('upload.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            print("h2")
            return render_template('upload.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            answer=ocr_fun(filename)
            #print(answer)
            return redirect(url_for('result',
                                    ))
        else:
            return render_template('upload.html')
    else:
        return render_template('upload.html')
    return 

@app.route('/result')
def result():
    return (answer)




if __name__ == '__main__':
    app.run(debug=True)
