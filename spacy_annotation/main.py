import scispacy
import spacy
import json

nlp = spacy.load("en_ner_bionlp13cg_md")


class SpacyNER:
    
    def __init__(self, input_file=''):
        self.input_file = input_file
    
    def load_data(self, input_file=''):
        f = open(input_file)
        data = json.load(f)
        f.close()
        return data

    def extract_entities_with_label(self, data={}):
        output = data
        for index in data :
            doc = nlp(data[index]['sentence'])
            output[index]['spacy_annotation'] = {}
            for entity in doc.ents : 
                # print(entity, " >> " ,entity.label_)
                if entity.label_ in ['GENE_OR_GENE_PRODUCT']:
                    output[index]['spacy_annotation'][str(entity)] = "[('Protein', 1)]"
        return output
    
    def save_data(self, input={}, output_file=''):
        with open(output_file, 'w') as convert_file:
            convert_file.write(json.dumps(input))
        return None

    def run(self):
        output_file = self.input_file
        data = self.load_data(input_file=output_file)
        output = self.extract_entities_with_label(data=data)
        self.save_data(input=output, output_file=output_file)
        print('\n \n')
        print('End with success !')
        return None

SpacyNER(input_file='../outputs/data/data.json').run()
