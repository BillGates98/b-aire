from cmath import nan
from dataclasses import field
from html import entities
import pickle as cPickle
import multiprocessing
import pandas as pd
from compute_files import ComputeFile
# from compute_files import ComputeFile


class Parser:

    def __init__(self, input_path='', extensions=[], source=''):
        print('Parser')
        self.uplets = []
        self.extensions = extensions
        print(input_path)
        self.source = source
        self.files = ComputeFile(input_path=input_path, extensions=extensions).build_list_files()
        # print(self.files)
    
    def loadTextFile(self, file=None):
        output = []
        f  = open(file, 'r')
        output = f.read()
        f.close()
        return output
    
    def samplesData(self, columns=[]):
        files = self.files
        data = []
        if '.txt' in self.extensions :
            for input_file in files:
                tmp = self.loadTextFile(file=input_file)
                data.append(tmp)
            return 'hunflair', data
        
        if '.tsv' in self.extensions :
            for input_file in files:
                tmp = self.loadHunflairFileTsv(file=input_file, columns=columns)
                for _tmp in tmp :
                    for item in _tmp:
                        data.append(item)
                # data.append(_tmp[0] for _tmp in tmp if len(_tmp)>0)
            return 'hunflair', data

        return self.source, None
    ###
    """
        Hunflair Data Integration
    """
    ###
    def loadHunflairFileTsv(self, file='', columns=[]):
        result = []
        dataFrame = pd.read_csv(file, sep='\t')
        
        print('************************ ', file)
        # _entities = dataFrame['Entity']
        # _types = dataFrame['Type']
        # for _type, entity in zip(_types, _entities):
        #     if not isinstance(entity, float) and entity != None :
        #         result.append((_type, entity.lstrip()))
        
        if len(columns) > 0 :
            size = len(dataFrame[columns[0]])
            for i in range(size):
                tmp = []
                for column in columns:
                    if not isinstance(dataFrame[column][i], float) and not dataFrame[column][i] in [None, 'None'] :
                        tmp.append(dataFrame[column][i].lstrip())
                result.append(tmp)
        # print(dataFrame['score'])
        # output = {
        #     'c1': 0,
        #     'c2': 0,
        #     'c3': 0,
        #     'c4': 0,
        # }
        # for k in dataFrame['score'] :
        #     if 0.0 <= k and k <= 0.25 :
        #         output['c1'] = output['c1'] + 1
        #     if 0.25 < k and k <= 0.50 :
        #         output['c2'] = output['c2'] + 1
        #     if 0.50 < k and k <= 0.9 :
        #         output['c3'] = output['c3'] + 1
        #     if 0.98 < k and k <= 1.0 :
        #         output['c4'] = output['c4'] + 1
        # print(output)
        # for column in _fields:
        #     for name in dataFrame[column] :
        #         if not isinstance(name, float) and name != None:
        #             result.append((column, name))
        print('File : ', file, ' - Length : ', len(result))
        return result
    
    def loadHunflairFilePkl(self, file=''):
        result = []
        with open(file, "rb") as input_file:
            tuples = cPickle.load(input_file)
            print('************************ ', file)
            fields = list(tuples.keys())
            _fields = [e for e in fields if 'gene' in e.lower()]
            print(_fields)
            for column in _fields:
                for name in tuples[column] :
                    if not isinstance(name, float) and name != None:
                        if isinstance(name, list):
                            for value in name :
                                result.append((column, value))
                        else:
                            result.append((column, name))
        print('File : ', file, ' - Length : ', len(result))
        return result

    def hunflairDatasets(self):
        files = self.files
        data = []
        if '.pkl' in self.extensions :
            for input_file in files:
                tmp = self.loadHunflairFilePkl(file=input_file)
                data.append(tmp)
            return 'hunflair', data
        
        if '.tsv' in self.extensions :
            for input_file in files:
                tmp = self.loadHunflairFileTsv(file=input_file, columns=['Type', 'Entity'])
                data.append(tmp)
            return 'hunflair', data

        return self.source, None
    
    ###
    """
        Alvisnlp Data Integration
    """
    ###
    def loadAlvisFile(self, file=''):
        f = open(file, "r")
        lines = f.readlines()
        result = []
        for x in lines:
            tmp = x.replace('\n', '').split('\t')
            tmp[1] = tmp[1].lstrip().split(' ')[0]
            if len(tmp) == 3:
                result.append((tmp[1], tmp[2]))
        f.close()
        return result

    def alvisnlpdatasets(self):
        files = self.files
        for input_file in files:
            tmp = self.loadAlvisFile(file=input_file)
            self.uplets.append(tmp)
        return self.source, self.uplets

    ###
    """ 
        Useful functions
    """
    ###
    def split_arrays(self, a=[], n=16):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

    def convert(self):
        return self.split_arrays(a=self.uplets)


# Parser(input_path='../../data/').run()
