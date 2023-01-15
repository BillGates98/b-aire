# from packages.migrator import Migrator
from parser import Parser
from migrator import Migrator
from vector import Vector
import pandas as pd
from nltk.corpus import stopwords
import re
import multiprocessing
from datetime import datetime 

cachedStopWords = stopwords.words("english")

def split_arrays(a=[], n=16):
    k, m = divmod(len(a), n)
    return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

class TextAnnotation:
    
    def __init__(self, data=[]):
        # print('Text Annotation')
        self.data = data
        self.migrator = Migrator()
        self.types = {}
    
    def cleanText(self, value=''):
        output = ' '.join([word for word in value.split() if word not in cachedStopWords])
        # ponctuation
        output = output.replace(',', ' ')
        output = output.replace('.', '')
        output = output.replace('(', ' ')
        output = output.replace(')', ' ')
        output = output.replace('\n', ' ')
        output = re.sub('\W+',' ', value )
        return output
    
    def getType(self, value=""):
        res = self.migrator.fetchBy(table="annotation", field="name", _value=value, result_value="type")
        return res

    def getTypeIds(self):
        res = self.migrator.fetch(query="SELECT DISTINCT value,id FROM type")
        for value, id in res:
            self.types[value] = id
        return self.types
    
    def _generateLearningData(self, limit_sample_by_class=-1):
        data = {
                'index': [],
                'round': [],
                'length': [],
                'depth': [],
                'size': [],
                'klass': [],
                'score': [],
            }
        _types = self.getTypeIds()
        ids = []
        for key in _types:
            ids.append(_types[key])
        for id in ids :
            query = "SELECT `index`, round, `length`, depth, size, `klass`, `bit` AS score FROM vectors WHERE klass = ':klass'"
            query = query.replace(':klass', str(id))
            if limit_sample_by_class > 0 :
                query = query +  " LIMIT :limit"
                query = query.replace(':limit', str(limit_sample_by_class))
            res = self.migrator.fetch(query=query)
            
            for index, round, length, depth, size, _class, bit in res :
                data['index'].append(index)
                data['round'].append(round)
                data['length'].append(length)
                data['depth'].append(depth)
                data['size'].append(size)
                data['klass'].append(_class)
                data['score'].append(bit)
                
        dataFrame = pd.DataFrame(data)
        dataFrame.to_csv('../outputs/training_datasets/training_data_0.csv', index=False)
        return None

    def build_vector(self, index=None, round=None, length=None, depth=None, size=None, bit=None, types=[]):
        hp_params = {}
        for _class in types :
            if _class in self.types : 
                hp_params = { "index": index, "round": round, "length": length, "depth": depth, "size": size, "bit": bit, "class": self.types[_class]}
                Vector(data=hp_params, migrator=self.migrator).save()
        return hp_params
        
    def saveAlgo(self, token='', type=[], output={}):
        if len(type) > 0 :
            if not token in output :    
                output[token] = []
            for _type in type :
                if not _type in output[token] :
                    output[token].append(_type)
        return output
      
    def algorithm(self, text=[], m=0, round=0, depth=0, output=[]):
        _output = [] if not output else output
        t = text
        n = len(text)
        if n - 1 >= m and t[m] != None:
            _xtype = self.getType(value=t[m])
            if len(_xtype) > 0 and m == round :
                _vector = self.build_vector(index=m, round=round, size=len(t[m].split(" ")), depth=depth, length=len(t[m]), bit=1, types=_xtype)
                _output.append(_vector)
                _output = self.algorithm(text=text, m=m, round=round + 1, depth=depth+1, output=_output)
            else:
                i = m
                if len(_xtype) > 0 :
                    _vector = self.build_vector(index=i, round=round, size=len(t[i].split(" ")), depth=depth, length=len(t[i]), bit=1, types=_xtype)
                    _output.append(_vector)
                else:
                    _vector = self.build_vector(index=i, round=round, size=len(t[i].split(" ")), depth=depth, length=len(t[i]), bit=0, types=['None'])
                    _output.append(_vector)
                tmp = t[i]
                while i < len(t) - 1 and len(tmp.split(' ')) <= 3:
                    i = i + 1
                    tmp = tmp + ' ' + t[i] 
                    _xtype = self.getType(value=tmp)
                    if len(_xtype) > 0 :
                        _vector = self.build_vector(index=m, round=round, size=i-m, depth=depth, length=len(t[i]), bit=1, types=_xtype)  # i-m
                        _output.append(_vector)
                    else:
                        _vector = self.build_vector(index=m, round=round, size=i-m, depth=depth, length=len(t[i]), bit=0, types=['None'])  # i-m
                        _output.append(_vector)
                if m < n-1 :
                    _output = self.algorithm(text=text, m=m+1, depth=depth+1, output=_output)
        return _output
    
    def curation(self, text='', value=[]):
        output = {}
        treated = []
        for token, status in value:
            if not token in treated :
                if not token in output :
                    output[token] = [*set(status)]
                    treated.append(token)
        return output
    
    def run(self):
        self.migrator.truncate(table="vectors")
        self.getTypeIds()
        data = self.data
        index = 0
        _output = {}
        for txt in data : 
            _output = self.algorithm(text=self.cleanText(value=txt).split(" "), m=0, output=_output)
            index = index + 1
        self._generateLearningData(-1)
        return _output
# get Data 
texts = []
start_time = datetime.now() 
source, data_parseds = Parser(input_path='../data/genia/biogenia/', extensions=['.txt'], source='genia').samplesData() # return the sentences
_data = split_arrays(a=data_parseds, n=16)

def parallel_running(data=[], index=0):
    texts = []
    print('Process number : ', index)
    for value in data :
        texts = texts + value.split('.')
    result = TextAnnotation(data=texts).run()
    return len(result)

total_received = 0
pool = multiprocessing.Pool()
cpu = multiprocessing.cpu_count()
result_async = [pool.apply_async(parallel_running, args =(_data[index], index)) for index in range(len(_data))]
for result in result_async :
    total_received = total_received + result.get()
print('Total vectors : ', total_received)
time_elapsed = datetime.now() - start_time 
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
