# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import random

import numpy as np

from audio import read_mfcc
from batcher import sample_from_mfcc
from constants import SAMPLE_RATE, NUM_FRAMES
from conv_models import DeepSpeakerModel
from test import batch_cosine_similarity

# Sample some inputs for WAV/FLAC files for the same speaker.
# To have reproducible results every time you call this function, set the seed every time before calling it.
# np.random.seed(123)
# random.seed(123)
mfcc_001 = sample_from_mfcc(read_mfcc('samples/PhilippeRemy/PhilippeRemy_001.wav', SAMPLE_RATE), NUM_FRAMES)
mfcc_002 = sample_from_mfcc(read_mfcc('samples/PhilippeRemy/PhilippeRemy_002.wav', SAMPLE_RATE), NUM_FRAMES)

# Call the model to get the embeddings of shape (1, 512) for each file.
predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

# Do it again with a different speaker.
mfcc_003 = sample_from_mfcc(read_mfcc('samples/1255-90413-0001.flac', SAMPLE_RATE), NUM_FRAMES)
predict_003 = model.m.predict(np.expand_dims(mfcc_003, axis=0))

# Compute the cosine similarity and check that it is higher for the same speaker.
print('SAME SPEAKER', batch_cosine_similarity(predict_001, predict_002)) # SAME SPEAKER [0.81564593]
print('DIFF SPEAKER', batch_cosine_similarity(predict_001, predict_003)) # DIFF SPEAKER [0.1419204]
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from flask import Flask, request

app = Flask(__name__)

@app.route('/query-example')
def query_example():
    return 'Query String Example'

@app.route("/result", methods = ["POST"])
def result():
    print(request.files)
    data = request.files['audio_data'].read()
    print(data)
    
    return 'https://avatars.dicebear.com/api/bottts/:seed.svg'

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

    
    
