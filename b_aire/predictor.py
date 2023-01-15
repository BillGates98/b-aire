import tensorflow as tf
from tensorflow import keras
import numpy as np
from IPython.display import display
from numpy import loadtxt
from tensorflow.keras.models import load_model
from pathlib import Path

class Predictor:
    
    def __init__(self, input_path='../outputs/models/', classes=[]):
        self.models = {}
        self.classes = classes
        for i in classes :
            filename = input_path + 'model_anno_' + str(i) + '.h5'
            my_file = Path(filename)
            if my_file.is_file():
                self.models[i] = load_model(filename)
                # summarize model.
                self.models[i].summary()
    
    def single_prediction(self, data=[]):
        models = self.models
        predictions = []
        score = 0.0
        alpha = 0.0001
        for _class in self.classes :
            if _class in models :
                tmp = data
                real = np.array(tmp).reshape(1,len(tmp))
                tmp_prediction = models[_class].predict( real )[0][0]
                if tmp_prediction >= alpha and tmp_prediction <= 1.0 : 
                    score = tmp_prediction
                predictions.append((_class, score))
        return score >= 0.0            
