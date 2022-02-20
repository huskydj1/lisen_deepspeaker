import os, subprocess

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Load Flask-Related Libraries
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

import random

import numpy as np

from audio import read_mfcc
from batcher import sample_from_mfcc
from constants import SAMPLE_RATE, NUM_FRAMES
from conv_models import DeepSpeakerModel
from test import batch_cosine_similarity

def generateFace(a):

    colorBank = ['amber', 'blue', 'blueGrey', 'brown', 'cyan', 'deepOrange', 'deepPurple', 'green', 'grey', 'indigo', 'lightBlue', 'lightGreen', 'lime', 'orange', 'pink', 'purple', 'red', 'teal', 'yellow']
    colorLevelBank = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]

    return 'https://avatars.dicebear.com/api/bottts/12314.svg?colors[]={}&colors[]={}&colorful=true&primaryColorLevel={}&secondaryColorLevel={}&textureChance={}&mouthChance={}&sidesChance={}&topChance={}'.format(
        colorBank[np.argmax(a[0:20])],
        colorBank[np.argmax(a[20:40])],
        colorLevelBank[np.argmax(a[69:79])],
        colorLevelBank[np.argmax(a[89:99])],
        99 if np.argmax(a[100:200]) >= 50 else 1,
        99 if np.argmax(a[200:300]) >= 50 else 1,
        99 if np.argmax(a[300:400]) >= 50 else 1,
        99 if np.argmax(a[400:500]) >= 50 else 1
    )
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def main_method():
    return render_template('index.html')

@app.route('/query-example')
def query_example():
    return 'Query String Example'


counter = 0
@app.route("/result", methods = ["POST"])
def result():
    global counter
    counter+=1
    print(counter)
    request.files['audio_data'].save('static/{}.ogg'.format(counter))

    a = int((counter - 1) // 12);
    b = int((counter - 1) % 12) * 5;
    #if b < 0:
    #    b = 0
    subprocess.run(["ffmpeg", '-y', "-i", 'static/{}.ogg'.format(counter), '-ss', str(a) + ':' + str(b), 'static/{}.wav'.format(counter)])

    mfcc_000 = sample_from_mfcc(read_mfcc('static/{}.wav'.format(counter), SAMPLE_RATE), NUM_FRAMES)

    predict_000 = model.m.predict(np.expand_dims(mfcc_000, axis=0))

    return generateFace(predict_000.flatten())
    

    # return "https://avatars.dicebear.com/api/bottts/12314.svg?colors[]=brown&colors[]=red&colorful=true&topChance=99"
    
if __name__ == '__main__':

    # Reproducible results.
    np.random.seed(123)
    random.seed(123)

    # Define the model here.
    global model
    model = DeepSpeakerModel()

    # Load the checkpoint. https://drive.google.com/file/d/1F9NvdrarWZNktdX9KlRYWWHDwRkip_aP.
    # Also available here: https://share.weiyun.com/V2suEUVh (Chinese users).
    model.m.load_weights('ResCNN_triplet_training_checkpoint_265.h5', by_name=True)

    # run app in debug mode on port 5000
    # app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=80)

    
    
