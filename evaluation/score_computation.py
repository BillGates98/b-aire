from migrator import Migrator
from decimal import *
import time
import argparse
import json
import ast
import pandas as pd

output = {}
class ScoreComputation:

    def __init__(self, input_file='', tool='annotation', size=0):
        self.input_file = input_file
        self.tool = tool
        self.size = size
        self.recaps = {
            '00': 0,
            '01': 0,
            '10': 0,
            '11': 0,
            'precision': 0,
            'recall': 0,
            'fmeasure': 0
        }
        self.migrator = Migrator()
        self.start_time = time.time()
        print('###   Score Analysis started   ###')
        print('\n \n')
    
    def load_json_file(self):
        f = open(self.input_file)
        data = json.load(f)
        f.close()
        for index in data:
            if int(index) <= self.size  and self.tool in data[index]:
                annotation_tmp = data[index][self.tool]
                for entity in annotation_tmp:
                    _entity = entity.lstrip().replace(';','').replace('[', '').replace(']', '')
                    score = ast.literal_eval(annotation_tmp[entity])[0][1]
                    n = len(_entity) 
                    if self.tool == 'annotation' :
                        if n > 2 and n <= 10 : # n == 10: # 
                            _res = self.getType(value=_entity, score=score)
                            self.recaps[_res] += 1
                            
                    if self.tool != 'annotation' :
                        if  n > 2  and n <= 10 : # n == 10: #
                            _res = self.getType(value=entity)
                            self.recaps[_res] += 1 
            else:
                break

    def getType(self, value="", score=0):
        res = self.migrator.fetchBy(table="annotation", field="name", _value='%'+value+'%', result_value="type")
        if len(res) > 0 :
            if 'Protein' or 'GP' in res :
                return '11'
            else:
                if not ('Protein' or 'GP') in res :
                    return '01'
        else:
            output[value] = 0
        return '10'
        

    def _recapitulating(self, recaps={}):
        # n_r_n = recap['00']
        print("****************** Score ********************")
        print("------------------", self.tool, "-------------------")
        n_r_p = recaps['01']
        p_r_n = recaps['10']
        p_r_p = recaps['11'] if recaps['11'] > 0 else 1
        precision = (p_r_p) / (p_r_p + p_r_n)
        recall = (p_r_p) / (p_r_p + n_r_p)
        fmeasure = (2*precision*recall) / (precision + recall)
        self.recaps['precision'] = precision
        self.recaps['recall'] = recall
        self.recaps['fmeasure'] = fmeasure
        print(self.recaps)
        print('------------------------')
        print('Precision : ', precision)
        print('Recall : ', recall)
        print('Fmeasure : ', fmeasure)
        print(precision, '&', recall, '&', fmeasure)
        return precision, recall, fmeasure

    def run(self):
        start_time = time.time()
        self.load_json_file()
        precision, recall, fmeasure = self._recapitulating(recaps=self.recaps)
        print('Process ended')
        print("--- %s seconds ---" % (time.time() - start_time))
        return precision, recall, fmeasure

def saveEvaluation(data=[], file=''):
    df = pd.DataFrame(data)
    df.to_csv(index=False)
    df.to_csv('./visualization/data_' + file + '.csv', sep='\t')
    
if __name__ == '__main__':
    def arg_manager():
        parser = argparse.ArgumentParser()
        parser.add_argument("--checking", type=str, default="../outputs/data/data_cineca.json")
        return parser.parse_args()
    args = arg_manager()
    valid = args.checking
    if args.checking.split('.')[-1] == 'json':
        valid = args.checking
    tool_indexs = ['annotation', 'spacy_annotation', 'hunflair_annotation']
    tools = {'annotation': 'B-aire', 'spacy_annotation': 'SciSpacy', 'hunflair_annotation': 'Hunflair'}
    data_precision = {}
    data_fmeasure = {}
    data_precision['Sample-size'] = []
    data_fmeasure['Sample-size'] = []
    for i in range(10, 700, 10):
        data_precision['Sample-size'].append(i)
        data_fmeasure['Sample-size'].append(i)
        for tool in tool_indexs :
            if not tools[tool] in data_fmeasure :
                data_fmeasure[tools[tool]] = []
                
            if not tools[tool] in data_precision :
                data_precision[tools[tool]] = []
                
            precision, recall, fmeasure = ScoreComputation(input_file=valid, tool=tool, size=i).run()
            data_fmeasure[tools[tool]].append(fmeasure)
            data_precision[tools[tool]].append(precision)
    print('Sample : ', len(data_precision['Sample-size']))
    print('Precision : ', len(data_precision['B-aire']))
    saveEvaluation(data=data_precision, file='precision')     
    saveEvaluation(data=data_fmeasure, file='fmeasure')
