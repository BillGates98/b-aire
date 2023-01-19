import json

class BuildGoldStandard:
    
    def __init__(self, input_file=''):
        self.input_file = input_file
    
    def load_data(self, input_file=''):
        f = open(input_file)
        data = json.load(f)
        f.close()
        return data

    def build_documents(self, data={}):
        output = {}
        limit = 10
        for pmc in data :
            annotations = data[pmc]['annotations']
            for annotation in annotations : 
                sentence = annotation['sent']
                tmp = []
                if annotation['ner'] and len(annotation['ner']) > 0: 
                    for start, end, name, label in annotation['ner']:
                        if label == 'GP' :
                            tmp = tmp + ['\t'.join(['T1', label, str(start), str(end), name])]
                    self.save(text=sentence, file_name=pmc, extension='.txt')
                    self.save(text='\n'.join(tmp), file_name=pmc, extension='.a1')
                    # if limit == 0 :
                    #     break
                    # else:
                    #     limit = limit - 1
        return output
    
    def save(self, text='', file_name='', extension=''):
        with open('./data/'+file_name+extension, 'w') as f:
            f.write(text)
    
    def run(self):
        output_file = self.input_file
        data = self.load_data(input_file=output_file)
        self.build_documents(data=data)
        print('\n \n')
        print('Conversion end with success !')
        return None

BuildGoldStandard(input_file='./cineca.json').run()
