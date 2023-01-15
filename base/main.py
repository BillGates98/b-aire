import json

from migrator import Migrator
from parser import Parser
from analysis import Analysis    

source, data_parseds = Parser(input_path='../data/genia/biogenia/', extensions=['.a1'], source='genia', truncate=False).run()
print('Genia .a1 ended 100 %')

