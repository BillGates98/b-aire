import requests    
import json
import multiprocessing
from datetime import datetime
import time

def split_arrays(a=[], n=16):
    k, m = divmod(len(a), n)
    return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

class BernNER:
    
    def __init__(self, input_file=''):
        self.input_file = input_file
        self.counter = 0
    
    def load_data(self, input_file=''):
        f = open(input_file)
        data = json.load(f)
        f.close()
        return data
    
    def query_plain(self, text='', url="http://bern2.korea.ac.kr/plain"):
        # time.sleep(0.35)
        print('Next pool In progress ...%', self.counter)
        self.counter = self.counter + 1
        try:
            result = None
            try:
                result = requests.post(url, json={'text': text}).json()
            except requests.ConnectionError as _:
                return None
            return result
        except json.decoder.JSONDecodeError:
            pass
        return { "annotations": [] }
                
    def parallel_running(self, data=[], index=0):
        output = []
        print('Process number : ', index)
        for value in data:
            if not 'bern_annotation' in value : 
                docs = self.query_plain(text=value['sentence'])
                if docs != None :
                    value['bern_annotation'] = {}
                    for entity in docs['annotations'] : 
                        if entity['obj'] in ['gene']:
                            value['bern_annotation'][str(entity['mention'])] = "[('Protein', 1)]"
            output.append(value)
        return output

    def extract_entities_with_label(self, data={}):
        start_time = datetime.now()
        pool = multiprocessing.Pool()
        cpu = multiprocessing.cpu_count()
        _data = split_arrays(a=list(data.values()), n=16)
        _output = []
        result_async = [pool.apply_async(self.parallel_running, args=(
            _data[index], index)) for index in range(len(_data))]
        for result in result_async:
            _output = _output + [result.get()]
        output = {}
        index = 0
        for data in _output:
            for item in data : 
                output[str(index)] = item
                index = index + 1
        print('Operation ended with success !')
        time_elapsed = datetime.now() - start_time
        print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
        return output
        
    # def extract_entities_with_label(self, data={}):
    #     output = data
    #     for index in data :
    #         docs = self.query_plain(text=data[index]['sentence'])
    #         output[index]['bern_annotation'] = {}
    #         for entity in docs['annotations'] : 
    #             if entity['obj'] in ['gene']:
    #                 output[index]['bern_annotation'][str(entity['mention'])] = "[('Protein', 1)]"
    #     return output
    
    def save_data(self, input={}, output_file=''):
        with open(output_file, 'w') as convert_file:
            convert_file.write(json.dumps(input))
        return None

    def run(self):
        output_file = self.input_file
        print('Process will start ...')
        data = self.load_data(input_file=output_file)
        output = self.extract_entities_with_label(data=data)
        self.save_data(input=output, output_file=output_file)
        print('\n \n')
        print('End with success !')
        return None

BernNER(input_file='../outputs/data/data.json').run()
