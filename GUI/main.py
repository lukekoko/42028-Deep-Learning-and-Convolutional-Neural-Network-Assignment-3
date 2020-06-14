from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import model
from threading import Thread
import time
from pathlib import Path

UPLOAD_FOLDER = './static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "meme" 

predictionDone = False
image = None
result = ''
hidden = False

Path('./model').mkdir(parents=True, exist_ok=True)
Path('./static/images/uploads').mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    global predictionDone
    predictionDone = False
    if (request.args):
        return render_template("index.html", image=request.args.get('image'), error=request.args.get('error'), hidden=(request.args.get('hidden') == 'True'), result=request.args.get('result'), poll=request.args.get('poll'))
    else:
        return render_template("index.html", image='/static/images/placeholder.png', hidden=hidden, error='', result='Please upload an image to be classified', poll=0)

# checks if file is image
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# uploads image
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

                return redirect(url_for('index', image=imagePath, hidden=hidden, error='', result='', poll=1))
    return redirect(url_for('index', image='/static/images/placeholder.png', error="Error occurred", hidden=False, result='', poll=0))

# polls this url to see when prediction is done
@app.route('/status')
def status():
    return jsonify(dict(status=predictionDone))

# this url displays result of prediction
@app.route('/result')
def result():
    global image, result, hidden, predictionDone
    return redirect(url_for('index', image=image, error="", hidden=False, result=result, poll=0))

# performs prediction
def predict(filepath):
    global predictionDone, result, hidden
    result = model.predict(filepath)
    predictionDone = True
    hidden = False

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
