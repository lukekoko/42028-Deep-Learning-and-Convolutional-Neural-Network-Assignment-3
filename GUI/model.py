import main
from flask import Flask, render_template, request, redirect, url_for
import time
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image
import numpy as np
import pathlib

# load model from weights
model = models.load_model('./model/weights_09-0.99.hdf5')
# labels
labelArr = {0: 'covid19', 1: 'normal'}

def predict(filepath):
    # load image
    img = image.load_img(filepath, target_size=(150, 150))
    # rescale image (this was done with training model. So it has to be done on predict images)
    x = image.img_to_array(img) / 255
    x = np.expand_dims(x, axis=0)
    # predict using loaded model
    prediction = (model.predict(x) > 0.5).astype("int32")
    # return result
    result = prediction[0][0]
    # pathlib.Path(filepath).unlink()
    return result