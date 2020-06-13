from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import model
from threading import Thread
import time

UPLOAD_FOLDER = './static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "meme" 

predictionDone = False
image = None
result = ''
hidden = False

@app.route('/')
def index():
    global predictionDone
    predictionDone = False
    if (request.args):
        return render_template("index.html", image=request.args.get('image'), error=request.args.get('error'), hidden=(request.args.get('hidden') == 'True'), result=request.args.get('result'))
    else:
        return render_template("index.html", image='/static/images/placeholder.png', hidden=hidden, error='', result='Please upload an image to be classified')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'GET'])
def uploadImage():
    if request.method == 'POST':
        if request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # save image path in global variable
                global image
                image = imagePath
                file.save(imagePath)
                job = Thread(target=predict, args=(imagePath,))
                global predictionDone, hidden, result
                result = ''
                hidden = True
                predictionDone = False
                job.start()
                return redirect(url_for('index', image=imagePath, hidden=hidden, error='', result=''))
    return redirect(url_for('index', image='/static/images/placeholder.png', error="Error occurred", hidden=False, result=''))

@app.route('/status')
def status():
    return jsonify(dict(status=predictionDone))

@app.route('/result')
def result():
    global image, result, hidden, predictionDone
    predictionDone = False
    return redirect(url_for('index', image=image, error="", hidden=False, result=result))


def predict(filepath):
    global predictionDone, result, hidden
    print('do some predictions here')
    result = model.predict(filepath)
    print('predictions done')
    predictionDone = True
    hidden = False

if __name__ == '__main__':
    app.run(debug=True)
