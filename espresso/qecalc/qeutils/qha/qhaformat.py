import pickle

class QHAFormat():
    def __init__(self, filename = None):
        self._filename = filename
        
        if self._filename != None:
            self.read()
    
    def read(self, filename = None):
        if filename != None:
            self._filename = filename
        
        self._data =  pickle.load( open(self._filename, 'r') )
        
        from qecalc.qetask.qeparser import QEStructure
        
        self._structures = []
        
        for config in self_data['config']:
            stru = QEStructure()
            stru.readStr(config)
            self._structures.append( stru )