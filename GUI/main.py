from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import model
from threading import Thread
import time

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "meme" 

predictionDone = False

@app.route('/')
def index():
    if (request.args):
        return render_template("index.html", image=request.args.get('image'), error=request.args.get('error'), hidden=request.args.get('hidden'), result=request.args.get('result'))
    else:
        return render_template("index.html", image='/static/images/placeholder.png', hidden=False, error='', result='')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'GET'])
def uploadImage():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(imagePath)
                job = Thread(target=predict, args=(imagePath,))
                global predictionDone
                predictionDone = False
                job.start()
                return redirect(url_for('index', image=imagePath, hidden=True, error='', result=''))
    return redirect(url_for('index', image='/static/images/placeholder.png', error="Error occurred", hidden=False, result=''))

@app.route('/status')
def status():
    return jsonify(dict(status=predictionDone))

def predict(filepath):
    global predictionDone
    print('do some predictions here')
    time.sleep(5)
    print('predictions done')
    predictionDone = True

if __name__ == '__main__':
    app.run(debug=True)
