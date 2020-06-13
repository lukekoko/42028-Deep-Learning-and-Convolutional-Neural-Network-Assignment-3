import main
from flask import Flask, render_template, request, redirect, url_for
import time
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

model = models.load_model('./model/modelweight.hdf5')
labelArr = {0: 'covid19', 1: 'normal'}

def predict(filepath):
    result = ''
    print('do some predictions here')
    print(filepath)
    img = image.load_img(filepath, target_size=(150, 150))
    plt.imshow(img)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    prediction = model.predict_classes(x)
    # result = labelArr[prediction[0][0]]
    result = str(prediction[0][0])
    print(result)
    return result