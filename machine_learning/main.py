from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from datetime import datetime 

class MachineLearning:
    
    def __init__(self, learning_file='', suffix=None):
        tmp = pd.read_csv(learning_file)
        self.data = tmp.query('length > 2 & length <= 10')
        print(len(self.data))
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.params = {
            'mae': [],
            'mse': []
        }
        self.shape = None
        self.suffix = suffix
        
    def data_preparation(self):
        data = self.data
        data       = data.sample(frac=1., axis=0)
        data_train = data.sample(frac=0.7, axis=0)
        data_test  = data.drop(data_train.index)
        data_train = data_train.drop(['klass'], axis=1)
        data_test = data_test.drop(['klass'], axis=1)
        x_train = data_train.drop(['score'], axis=1)
        y_train = data_train['score']
        x_test  = data_test.drop(['score'], axis=1)
        y_test  = data_test['score']
        self.shape = x_train.shape[1]
        print(self.shape)
        self.x_train, self.y_train = np.array(x_train), np.array(y_train)
        self.x_test, self.y_test  = np.array(x_test),  np.array(y_test)
    
    def plot_graph(self, y={}):
        legends = list(y.keys())
        for key in legends :
            plt.plot(y[key])
        plt.legend(legends)
        plt.savefig('./learning_curve/learning_accuracy_'+ self.suffix + '.png')
        
    def get_model_v1(self, shape=4):
        model = keras.models.Sequential()
        model.add(keras.layers.Input((shape,), name="InputLayer"))
        model.add(keras.layers.Dense(9*32, activation='relu', name='Dense_n1'))
        model.add(keras.layers.Dense(9*64, activation='relu', name='Dense_n2'))
        model.add(keras.layers.Dense(9*32, activation='relu', name='Dense_n3'))
        model.add(keras.layers.Dense(1, name='Output'))
        model.compile(optimizer = 'adam',
                    loss      = 'mse',
                    metrics   = ['mae', 'mse'] )
        return model

    def learn(self):
        model = self.get_model_v1(shape=self.shape)
        model.summary()
        history = model.fit(self.x_train,
                            self.y_train,
                            epochs          = 120,
                            batch_size      = 10,
                            verbose         = 0,
                            validation_data = (self.x_test, self.y_test))
        self.params['mae'] = history.history["val_mae"]
        self.params['mse'] = history.history["val_mse"]
        self.plot_graph(y=self.params)
        model.save("../outputs/models/model_anno_"+self.suffix+".h5")
        return model
    
    def orchestrator(self):
        self.data_preparation()
        _ = self.learn()

for i in [0] :
    start_time = datetime.now() 
    filename = '../outputs/training_datasets/training_data_'+str(i)+'.csv'
    my_file = Path(filename)
    if my_file.is_file():
        print('Model : ', str(i))
        ml = MachineLearning(learning_file=filename, suffix=str(i)).orchestrator()
    time_elapsed = datetime.now() - start_time 
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))