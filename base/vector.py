from migrator import Migrator

class Vector:
    
    # def __init__(self, index=None, round=None, length=None, depth=None, _class=None, migrator: Migrator=None):
    def __init__(self, data={}, migrator: Migrator=None):
        # self.index = index
        # self.round = round
        # self.length = length
        # self.depth = depth
        # self._class = _class
        self.data = data
        self.migrator = migrator
        
    def save(self):
        data = self.data
        query = """
            INSERT INTO vectors 
            ('id', 'index', 'round', 'length', 'depth', 'size', 'bit', 'klass') 
            VALUES (NULL, "_index", "_round", "_length", "_depth", "_size", "_bit", "_class")
        """
        query = query.replace("'", '`')
        keys = list(self.data.keys())
        for key in keys:
            if '_' + key in query :
                query = query.replace('_' + key, str(data[key]))
        res = self.migrator.create(query=query)
        return res

       
        