from parser import Parser
from migrator import Migrator
from predictor import Predictor
from nltk.corpus import stopwords
import enchant
import json
import multiprocessing
from datetime import datetime

cachedStopWords = stopwords.words("english")
bagOfWords = enchant.Dict("en_US")

def split_arrays(a=[], n=16):
    k, m = divmod(len(a), n)
    return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

class TextAnnotation:

    def __init__(self, data=[]):
        self.data = data
        self.migrator = Migrator()
        self.predictor = Predictor(classes=[0])
        self.types = {}
        self.inverted_types = {0: 'None'}
        self.annotations = {}

    def clean_text(self, value=''):
        output = ' '.join([word for word in value.split() if word not in cachedStopWords])
        output = output.replace(',', ' ')
        output = output.replace('.', ' ')
        output = output.replace('(', ' ')
        output = output.replace(')', ' ')
        output = output.replace(':', '')
        output = output.replace('/', ' ')
        output = output.replace('\n', ' ')
        return output
    
    def clean_entity(self, value=''):
        _value = value.lstrip()
        if len(_value) == 0 : 
            return False
        numbercount = sum(1 for c in _value if c.isdigit())
        if numbercount == 0 or numbercount == len(_value) or _value[0].isdigit() or _value[0] in ['-', '+']:
            return False
        
        exclude = ['pd', 'dq', 's1', 't2', 't3', 't4', 'sb', 'wl', 'r2', 'b4', 'rc', 'sn', 'tg', 'g1', 'sri', 'gc', 'tg', 'dp', 'sl', 'mn', 'nb', 'c12', 'cz', 'ml', 'fr', 'dr', 'lice', 'ssi', 'ocs', 'cc', 'ber', 'gc', 'erb', 'cap', 'tk', 'max', 'ard', 'mad', 'mm', 'xq', 'qx', 'ru', 'sf', 'swi', 'tmd', 'uf', 'rs', 'tg', 'eto', '2f', 'cc', 'kt', 'tes', 'dp', 'ff', 'aca', 'md', 'mc', 'gf', 'rr', 'pk', 'k5', 'mn', 'cem', 'q2', 'cv', 'ratio', 'avp', 'raw', 'us', 'cb', 'fv', 'k5', 'can', 'mo', 'lf', 'pg', 'ex', 'dd', 'qp', 'pc', 'zt', 'gr', 'y4', 'gl', 'u9', 'tt', 'now', 'nup', 'bp', 'bs', 'as', 'lb', '2d', 'na', '&', "'", ']', '[' ';', '*', '>', '<', 'waf', 'cip', 'ea', 'ae', 'age', 'ty', 'aud', 'mac', 'lc', 'gd', 'mar', 'aa', 'man', 'ig', 'sp', 'po', 'nal', 'lus', 'pi', 'ten', 'tor', 'ton', 'pl', 'kl', 'nq', 'tc', 'sc', 'ni', 'ul', 'rk', 'tp', 'mol', 'tl', 'elu', 'tion', 'vd', 'my', 'bi', 'dna', 'pcr', 'gen', 'path', 's6', 'cr', 'pr', 'rg', 'll', 'cm', 'st', 'tr', 'vr', 'lig', 'eo', 'oe', 'tor', 'tu', 'fdc', 'nit', 'ps', 'ms', 'cr', '%', 'thy', 'lp', 'beta', 'rna', 'se', 'gy', 'pm', 'mp', 'bm', 'h', 'id', 'ib', 'com', 'cos', 'col', 'epi', 'alto', 'j','ly', 'yl', 'iu', 'iso', 'ab', 'im', 'ao', 'ae', 'sca', 'ox', 'vo', 'vi', 'cy', 'ry', 'in', 'rin']
        for v in exclude:
            if v in value.lower():
                return False
        return True

    def getAnnotationAssocs(self):
        res = self.migrator.fetch(query="SELECT DISTINCT value,id FROM type")
        for value, id in res:
            self.types[value] = id
            self.inverted_types[id] = value
        return self.types

    def save(self, token='', output={}):
        output[token] = [('Protein', 1.0)]
        return output

    def recognition(self, text=[], m=0, round=0, depth=0, output={}):
        _output = output
        t = text
        n = len(text)
        if n - 1 >= m and t[m] != None :
            if m == round:
                vector = [m, round, len(t[m]), depth, 1]
                predicted = self.predictor.single_prediction(data=vector)
                if predicted :
                    _output = self.save(token=t[m], output=_output)
                _output = (self.recognition(text=text, m=m, round=round + 1, depth=depth+1, output=_output))
                return _output
            else:
                i = m
                if round > 0:
                    vector = [m, round, len(t[m]), depth, 1]
                    predicted = self.predictor.single_prediction(data=vector)
                    if predicted : 
                        _output = self.save(token=t[m], output=_output)
                tmp = t[i]
                while i < len(t) - 1 and len(tmp.split(' ')) <= 3 :
                    i = i + 1
                    tmp = tmp + ' ' + t[i]
                    vector = [m, round, len(t[m]), depth, i-m]
                    predicted = self.predictor.single_prediction(data=vector)
                    if predicted :
                        _output = self.save(token=tmp, output=_output)
                if m < n-1:
                    _output = self.recognition(text=text, m=m+1, depth=depth+1, output=_output)
        return _output

    def _curation(self, input={}):
        _output = {}
        for key in input:
            _key = key.lstrip()
            if len(_key) > 0 and len(input[key]) > 0:
                sub_keys = _key.lstrip().split(' ')
                for s_key in sub_keys:
                    tmp = s_key.lstrip()
                    if len(tmp) > 0 :
                        if self.clean_entity(value=tmp) :
                            _output[tmp] = str(input[key])
        return _output

    def load_data(self, input_file=''):
        f = open(input_file)
        data = json.load(f)
        f.close()
        return data

    def run(self):
        # self.getAnnotationAssocs()
        index = 0
        _output = {}
        text_data = self.data
        for txt in text_data:
            tmp = {}
            for _txt in txt.split('.'):
                _text = self.clean_text(value=_txt).split(" ")
                tmp = self.recognition(text=_text, m=0, output=tmp)
            _cured_data = self._curation(input=tmp)
            if not str(index) in _output:
                _output[str(index)] = {}
            _output[str(index)]['sentence'] = txt
            _output[str(index)]['annotation'] = _cured_data
            index = index + 1
        return _output


def parallel_running(data=[], index=0):
    texts = []
    print('Process number : ', index)
    for value in data[0:1]:
        texts = texts + value.split('.')
    result = TextAnnotation(data=texts).run()
    return result

def save_output(output_file='', output={}):
    with open(output_file, 'w') as convert_file:
        convert_file.write(json.dumps(output))
        print('saved')


# get Data
texts = []
start_time = datetime.now()
source, data_parseds = Parser(input_path='../data/genia/biogenia-test/', extensions=['.txt'], source='genia').samplesData()

_data = split_arrays(a=data_parseds, n=16)

_output = []
output_file = '../outputs/data/data.json'
pool = multiprocessing.Pool()
cpu = multiprocessing.cpu_count()
result_async = [pool.apply_async(parallel_running, args=(
    _data[index], index)) for index in range(len(_data))]
for result in result_async:
    _output = _output + [result.get()]

output = {}
index = 0
for data in _output:
    for item in data:
        output[str(index)] = data[item]
        index = index + 1

save_output(output_file=output_file, output=output)
print('Operation ended with success !')
time_elapsed = datetime.now() - start_time
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
