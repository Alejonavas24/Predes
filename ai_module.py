import numpy as np
from tensorflow.keras.models import load_model

smoke_detector = load_model('models/smoke_cnn.h5')
fire_predictor = load_model('models/spread_lstm.h5')

def detect_smoke(image_array):
    
    img = np.expand_dims(image_array, axis=0) / 255.0
    pred = smoke_detector.predict(img)[0,0]
    return pred > 0.5

def predict_spread(history_sequence):
     seq = np.expand_dims(history_sequence, axis=0)
     return fire_predictor.predict(seq)[0,0]
