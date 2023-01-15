import matplotlib.pyplot as plt
import pandas as pd

from migrator import Migrator

class Analysis:
    
    def __init__(self):
        self.migrator = Migrator()
    
    def getEntities(self):
        data = []
        res = self.migrator.fetch(query="SELECT DISTINCT type, name FROM annotation")
        for type, name in res:
            data.append((type, name))
        return data
    
    def length_aggregation(self, data=[]):
        output = {}
        for _, _value in data : 
            token_length = len(_value)
            if not token_length in output :
                output[token_length] = 0
            output[token_length] = output[token_length] + 1
            # break
        return output
    
    def probabilities_computation(self, data=[]):
        output = data
        summarize = sum(list(data.values()))
        for index in output :
            output[index] = output[index] / summarize
        return output

    def save_probabilities(self, data={}):
        data.sort(key=lambda tup: tup[1], reverse=True)
        classes = []
        values = []
        for index, value in data :
            classes.append(index)
            values.append(value)
        output = {}
        output['token_size'] = classes 
        output['probabilities'] = values    
        dataFrame = pd.DataFrame(output)
        dataFrame.to_csv('./data/repartition_of_entities_by_length.csv', index=False, sep ='\t')
        return None

    def draw_graph(self, data=[]):
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
        plt.title('Repartition of Entities by length', fontsize = 12)
        plt.legend()
        plt.savefig('./curves/repartition_of_entity_by_length.png')
        self.save_probabilities(data=items) 
        return None
    
    def run(self):
        data = self.getEntities()
        agg_data = self.length_aggregation(data=data)
        probabs_data = self.probabilities_computation(data=agg_data)
        self.draw_graph(data=probabs_data)
        print('Analysis Task done with success ! ')
        return None

_ = Analysis().run()
        
