# from packages.migrator import Migrator
from migrator import Migrator
import matplotlib.pyplot as plt
import pandas as pd

class Acceptation:
    
    def __init__(self, input_file=''):
        self.input_file = input_file
        self.data = None
        self.migrator = Migrator()
        self.types = {}
    
    def readCsv(self):
        df = pd.read_csv(self.input_file, sep='\t', index_col=False)
        self.data = df
        return df
    
    def getVectorsCount(self):
        count_all = "SELECT count(*) as CTS FROM `vectors` WHERE klass = 2"
        # count all 
        res = self.migrator.fetch(query=count_all)
        return res[0][0]
    
    def getVectorCount(self, value=1):
        count_by_size = "SELECT count(*) as CTS FROM `vectors` WHERE klass=2 AND length = :length"
        # count one 
        res = self.migrator.fetch(query=count_by_size.replace(':length', str(value)))
        return res[0][0]

    def save_probabilities(self, data=[]):
        data.sort(key=lambda tup: tup[1], reverse=True)
        classes = []
        values = []
        for index, value in data :
            classes.append(index)
            values.append(value)
        output = {}
        output['token_size'] = classes 
        output['chances'] = values    
        dataFrame = pd.DataFrame(output)
        dataFrame.to_csv('./data/repartition_of_NFRs_by_length.csv', index=False, sep ='\t')
        return None

    def draw_graph(self, data={}):
        items = list(data.items())
        items.sort(key=lambda tup: tup[0])
        classes = []
        values = []
        for index, value in items :
            classes.append(index)
            values.append(value)
        plt.plot(classes, values, color = 'black', marker = 'o',label = "Probability")
        plt.xlabel('Token length')
        plt.ylabel('Probability')
        plt.title('Repartition of NFRs by length component', fontsize = 12)
        plt.legend()
        plt.savefig('./curves/repartition_of_NFRs_by_length.png')
        self.save_probabilities(data=items) 
        return None
    
    def run(self):
        data = self.readCsv()
        total_vectors_count = self.getVectorsCount()
        output = {}
        for index in range(0, len(data['token_size'])):
            token_size = (data['token_size'][index])
            probability = (data['probabilities'][index])
            tmp = self.getVectorCount(value=token_size)
            prob_recognition = (tmp/total_vectors_count) * probability
            output[data['token_size'][index]] = prob_recognition
        self.draw_graph(data=output)
        print('Analysis Task 2 done with success ! ')
        return data

Acceptation(input_file='./data/repartition_of_entities_by_length.csv').run()