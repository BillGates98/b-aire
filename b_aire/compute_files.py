import os

class ComputeFile: 

    def __init__(self, input_path='', extensions=[]):
        self.input_path = input_path
        self.input_files = []
        self.extensions = extensions
    
    def accept_extension(self, file='') :
        for ext in self.extensions :
            if file.endswith(ext) :
                return True
        return False
    
    def build_list_files(self):
        """
            building the list of input files
        """
        for current_path, folders, files in os.walk(self.input_path): # os.walk(self.input_path)
            for file in files:
                if self.accept_extension(file=file):
                    tmp_current_path = os.path.join(current_path, file)
                    self.input_files.append(tmp_current_path)
        return self.input_files

# ComputeFile(input_path='./data/').build_list_files()