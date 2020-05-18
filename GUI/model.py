import main
from flask import Flask, render_template, request, redirect, url_for
import time

def predict(filepath):
    print('do some predictions here')
    time.sleep(5)
    print('predictions done')
    print(main.predictionDone)
    main.predictionDone = True
    print(main.predictionDone)