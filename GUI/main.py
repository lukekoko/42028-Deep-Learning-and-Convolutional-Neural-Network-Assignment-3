from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
import os
import model
from pathlib import Path

UPLOAD_FOLDER = './static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "meme" 

Path('./model').mkdir(parents=True, exist_ok=True)
Path('./static/images/uploads').mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    if (request.args):
        return render_template("index.html", image=request.args.get('image'), error=request.args.get('error'), result=request.args.get('result'))
    else:
        return render_template("index.html", image='/static/images/placeholder.png', error='', result='Please upload an image to be classified')

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
                # save image to access later
                file.save(imagePath)
                # predict on image
                result = model.predict(imagePath)
                return redirect(url_for('index', image=imagePath, error="", result=result))  
    return redirect(url_for('index', image='/static/images/placeholder.png', error="Error occurred", result=''))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
